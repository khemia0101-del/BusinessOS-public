"""Behavioral regressions using synthetic data only."""

from calendar import monthrange
from copy import deepcopy
import io
import json
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from businessos.finance import (ValidationError, decimal, historical_ltm, normalize_period,
                               project_cash, reconcile, scenario, working_capital)
from businessos.runtime import Runtime, extract
from businessos.server import make_handler


def period(month=1, year=2025):
    return {"id": f"p-{year}-{month}", "start": f"{year}-{month:02d}-01", "end": f"{year}-{month:02d}-{monthrange(year, month)[1]}",
            "basis": "accrual", "status": "actual", "currency": "USD", "earnings_definition": "net_income",
            "reported_earnings": "100.00", "revenue": "500.00", "source_ids": ["ledger"]}


def scenario_input(name="base"):
    return {"name": name, "revenue": "1000", "gross_margin": "0.40", "operating_cost": "100", "replacement_cost": "50",
            "cash_taxes": "20", "capex": "30", "working_capital_increase": "40", "annual_debt_service": "80",
            "opening_cash": "100", "minimum_cash": "50", "multiple": "3", "debt": "200", "excess_cash": "10", "transaction_fees": "20",
            "source_ids": ["ledger"], "assumptions": ["Synthetic explicit cost assumptions"]}


def initiative(source_id="ledger"):
    return {"id": "collections", "title": "Collections pilot", "owner": "test-owner", "baseline": "10", "target": "5",
            "metric": "collection_days", "measurement_end": "2026-12-31", "stop_condition": "Complaints increase", "rollback": "Restore manual process",
            "source_ids": [source_id], "benefit_group": "collections", "setup_cost": "100", "monthly_cost": "20", "monthly_cash_benefit": "100",
            "monthly_hours": "5", "start_month": 1, "ramp_months": 2}


class FinanceTests(unittest.TestCase):
    def test_wip_cost_support_and_expected_loss(self):
        from businessos.construction import calculate_wip
        job = {"id": "job-1", "source_ids": ["ledger"], "costs_verified": False, "contract_value": "1000", "approved_change_orders": "0", "cost_incurred": "600", "cost_to_complete": "600", "billings": "400", "collections": "300"}
        result = calculate_wip(job)
        self.assertEqual(result["earned_revenue"], "500.00")
        self.assertEqual(result["underbilling"], "100.00")
        self.assertEqual(result["expected_contract_loss"], "200.00")
        self.assertEqual(result["readiness"], "unverified_cost_to_complete")
        with self.assertRaises(ValidationError): calculate_wip({**job, "cost_to_complete": None})

    def test_migration_does_not_inherit_approval(self):
        from businessos.migrate import migrate_legacy
        old = {"report_id": "old", "business_id": "alpha", "as_of_date": "2026-01-01", "recommendation": {"decision": "proceed"}}
        with self.assertRaises(ValidationError): migrate_legacy(old, {})
        mapping = {"report_id": "new", **{key: [] for key in ("periods", "adjustments", "reconciliations", "citations", "coverage", "scenarios")}}
        self.assertEqual(migrate_legacy(old, mapping)["recommendation"]["decision"], "pause")

    def test_missing_and_nonfinite_are_not_zero(self):
        for value in (None, True, "nan", "Infinity", ""):
            with self.subTest(value=value), self.assertRaises(ValidationError): decimal(value)

    def test_exact_decimal_normalization(self):
        p = period()
        p["reported_earnings"] = "0.10"
        a = {"id": "a", "period_id": p["id"], "classification": "nonrecurring", "accepted": True, "amount": "0.20",
             "source_ids": ["ledger"], "rationale": "Synthetic", "recurrence_test": "passed", "replacement_cost_test": "passed"}
        self.assertEqual(normalize_period(p, [a])["normalized_earnings"], "0.30")
        a["classification"] = "unsupported"
        with self.assertRaises(ValidationError): normalize_period(p, [a])

    def test_replacement_cost_cannot_be_positive_addback(self):
        p = period()
        a = {"id": "a", "period_id": p["id"], "classification": "replacement_cost", "accepted": True, "amount": "20", "source_ids": ["ledger"], "rationale": "Synthetic", "recurrence_test": "passed", "replacement_cost_test": "passed"}
        with self.assertRaises(ValidationError): normalize_period(p, [a])

    def test_adjustment_requires_recurrence_and_replacement_tests(self):
        p = period()
        a = {"id": "a", "period_id": p["id"], "classification": "nonrecurring", "accepted": True, "amount": "20", "source_ids": ["ledger"], "rationale": "Synthetic"}
        with self.assertRaises(ValidationError): normalize_period(p, [a])

    def test_actual_ltm_and_forecast_rejection(self):
        rows = [normalize_period(period(n), []) for n in range(1, 13)]
        self.assertEqual(historical_ltm(rows)["normalized_earnings"], "1200.00")
        rows[-1]["status"] = "forecast"
        with self.assertRaisesRegex(ValidationError, "Forecast"): historical_ltm(rows)

    def test_ltm_rejects_stub_overlap_and_mixed_basis(self):
        rows = [normalize_period(period(n), []) for n in range(1, 13)]
        for mutation in ("stub", "overlap", "basis"):
            bad = deepcopy(rows)
            if mutation == "stub": bad[-1]["end"] = "2025-12-15"
            if mutation == "overlap": bad[-1] = deepcopy(bad[-2])
            if mutation == "basis": bad[-1]["basis"] = "cash"
            with self.subTest(mutation=mutation), self.assertRaises(ValidationError): historical_ltm(bad)

    def test_reconciliation_recalculates_difference(self):
        row = {"id": "r", "source_a": "a", "source_b": "b", "amount_a": "100", "amount_b": "90", "difference": 0, "status": "open"}
        self.assertEqual(reconcile(row)["difference"], "10.00")
        row["status"] = "reconciled"
        with self.assertRaises(ValidationError): reconcile(row)

    def test_scenario_cash_equity_and_debt_service(self):
        result = scenario(scenario_input())
        self.assertEqual(result["normalized_ebitda"], "250.00")
        self.assertEqual(result["cash_available_for_debt_service"], "160.00")
        self.assertEqual(result["debt_service_coverage"], "2.000")
        self.assertEqual(result["ending_cash"], "180.00")
        self.assertEqual(result["enterprise_value"], "750.00")
        self.assertEqual(result["equity_value"], "560.00")

    def test_nonpositive_earnings_not_positive_valuation(self):
        row = scenario_input()
        row["operating_cost"] = "2000"
        self.assertIsNone(scenario(row)["enterprise_value"])
        row["annual_debt_service"] = 0
        self.assertIsNone(scenario(row)["debt_service_coverage"])

    def test_working_capital_inclusions(self):
        self.assertEqual(working_capital({"receivables": "100", "payables": "30"})["net_working_capital"], "70.00")
        with self.assertRaises(ValidationError): working_capital({"cash": 100})
        with self.assertRaises(ValidationError): working_capital({"payables": None})

    def test_initiative_cash_ramp_and_capacity(self):
        months = [{"period": "2026-01", "net_cash_flow": 0}, {"period": "2026-02", "net_cash_flow": 0}]
        result = project_cash(1000, months, [initiative()], {"monthly_hours": 10, "minimum_cash": 500})
        self.assertEqual(next(r for r in result if r["period"] == "2026-01" and r["scenario"] == "base")["ending_cash"], "930.00")
        with self.assertRaisesRegex(ValidationError, "Capacity"): project_cash(1000, months, [initiative()], {"monthly_hours": 2, "minimum_cash": 0})
        duplicate = {**initiative(), "id": "other"}
        with self.assertRaisesRegex(ValidationError, "overlapping"): project_cash(1000, months, [initiative(), duplicate], {"monthly_hours": 20, "minimum_cash": 0})


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.runtime = Runtime(self.temp.name, "alpha")
        self.runtime.configure({"display_name": "Synthetic Company", "industry": "construction", "notebook_url": "https://notebook.google.com/notebook/00000000-0000-0000-0000-000000000001"}, "owner")
        self.source = self.runtime.ingest(b"Revenue: 500\nEarnings: 100", "ledger.txt", "ledger", "primary", "owner")

    def tearDown(self):
        self.temp.cleanup()

    def report(self):
        p = period(); p["source_ids"] = [self.source["id"]]
        return {"schema_version": 2, "report_id": "report-1", "business_id": "alpha", "as_of_date": "2026-01-01", "periods": [p], "adjustments": [], "reconciliations": [], "scenarios": [], "coverage": [],
                "citations": [{"source_id": self.source["id"], "locator": "line:1", "claim": "Synthetic revenue"}],
                "recommendation": {"decision": "pause", "summary": "Synthetic missing evidence", "conditions": ["Obtain missing confirmations"]}}

    def test_duplicate_ingestion_and_versioned_invalidation(self):
        duplicate = self.runtime.ingest(b"Revenue: 500\nEarnings: 100", "ledger.txt", "ledger", "primary", "owner")
        self.assertTrue(duplicate["duplicate"])
        self.runtime.create_report(self.report(), "owner")
        changed = self.runtime.ingest(b"Revenue: 501\nEarnings: 100", "ledger.txt", "ledger", "primary", "owner")
        self.assertEqual(changed["version"], 2)
        self.assertTrue(self.runtime.snapshot()["reports"][0]["stale"])
        self.assertEqual(self.runtime.source_bytes(self.source["id"])[1], b"Revenue: 500\nEarnings: 100")

    def test_notebook_claim_is_exclusive(self):
        job = self.runtime.notebook_job({"action": "read"}, "owner")
        self.assertEqual(self.runtime.claim_notebook_job(job["id"], "worker")["status"], "running")
        with self.assertRaisesRegex(ValidationError, "claimed"):
            self.runtime.claim_notebook_job(job["id"], "worker")

    def test_notebook_origin_cannot_be_laundered_by_renaming(self):
        self.runtime.ingest(b"Derived answer", "answer.txt", "derived", "notebook", "owner")
        with self.assertRaises(ValidationError):
            self.runtime.ingest(b"Derived answer", "bank.txt", "bank", "primary", "owner")

    def test_projection_survives_restart_and_deduplicates(self):
        data = {"opening_cash": "1000", "months": [{"period": "2026-01", "net_cash_flow": "-200"}], "initiatives": [], "capacity": {"monthly_hours": "10", "minimum_cash": "900"}}
        results = self.runtime.save_projection(data, "owner")
        self.runtime.save_projection(data, "owner")
        snapshot = Runtime(self.temp.name, "alpha").snapshot()
        self.assertEqual(len(snapshot["projections"]), 1)
        self.assertEqual(snapshot["projections"][0]["results"], results)
        self.assertEqual(results[0]["funding_gap"], "100.00")

    def test_duplicate_report_returns_cached_and_changed_is_immutable(self):
        self.runtime.create_report(self.report(), "owner")
        self.assertTrue(self.runtime.create_report(self.report(), "owner")["cache_hit"])
        revised = self.report(); revised["recommendation"]["summary"] = "New conclusion"
        with self.assertRaisesRegex(ValidationError, "immutable"): self.runtime.create_report(revised, "owner")

    def test_company_isolation_and_path_traversal(self):
        other = Runtime(self.temp.name, "beta")
        self.assertEqual(other.list("source"), [])
        with self.assertRaises(ValidationError): other.get("source", self.source["id"])
        with self.assertRaises(ValidationError): Runtime(self.temp.name, "../alpha")
        data = self.report(); data["business_id"] = "beta"
        with self.assertRaises(ValidationError): self.runtime.create_report(data, "owner")

    def test_company_industry_is_an_explicit_enum(self):
        with self.assertRaisesRegex(ValidationError, "Industry"):
            self.runtime.configure({"display_name": "Synthetic Company", "industry": "unknown-industry"}, "owner")

    def test_citation_locator_must_exist(self):
        data = self.report(); data["citations"][0]["locator"] = "page:999"
        with self.assertRaisesRegex(ValidationError, "locator"): self.runtime.create_report(data, "owner")

    def test_missing_coverage_cannot_be_unconditional_proceed(self):
        data = self.report(); data["recommendation"]["decision"] = "proceed"
        with self.assertRaisesRegex(ValidationError, "Unconditional"): self.runtime.create_report(data, "owner")

    def test_notebook_cannot_be_independent_evidence(self):
        source = self.runtime.ingest(b"AI answer", "answer.txt", "notebook-answer", "notebook", "owner")
        with self.assertRaisesRegex(ValidationError, "independent"): self.runtime.source_refs([source["id"]], independent=True)

    def test_self_approval_and_undisclosed_exceptions_rejected(self):
        r = self.runtime.create_report(self.report(), "owner")
        with self.assertRaisesRegex(ValidationError, "author"): self.runtime.review_report(r["id"], "approve", r["gaps"], "Test", "owner")
        with self.assertRaisesRegex(ValidationError, "every material"): self.runtime.review_report(r["id"], "approve", [], "Test", "reviewer")
        reviewed = self.runtime.review_report(r["id"], "approve", r["gaps"], "Synthetic exception review", "reviewer")
        self.assertEqual(reviewed["status"], "decision_ready_with_exceptions")

    def test_notebook_pending_is_not_verified_and_publish_is_idempotent(self):
        job = self.runtime.notebook_job({"action": "read"}, "owner")
        self.assertEqual(job["status"], "pending")
        r = self.runtime.create_report(self.report(), "owner")
        with self.assertRaises(ValidationError): self.runtime.notebook_job({"action": "publish", "report_id": r["id"]}, "owner")
        self.runtime.review_report(r["id"], "approve", r["gaps"], "Synthetic review", "reviewer")
        published = self.runtime.notebook_job({"action": "publish", "report_id": r["id"]}, "owner")
        retry = self.runtime.notebook_job({"action": "publish", "report_id": r["id"]}, "owner")
        self.assertEqual(published["id"], retry["id"])
        self.assertTrue(retry["duplicate"])
        self.assertEqual(retry["status"], "pending")

    def test_notebook_identity_processing_and_auth_expiry(self):
        job = self.runtime.notebook_job({"action": "read"}, "owner")
        with self.assertRaisesRegex(ValidationError, "identity"): self.runtime.notebook_result(job["id"], {"status": "verified", "notebook_url": "wrong"}, "worker")
        result = self.runtime.notebook_result(job["id"], {"status": "login_required", "notebook_url": job["notebook_url"]}, "worker")
        self.assertEqual(result["status"], "login_required")

    def test_iniative_preacquisition_cannot_promote(self):
        item = self.runtime.save_initiative(initiative(self.source["id"]), "owner")
        self.runtime.initiative_action(item["id"], {"action": "shadow", "rationale": "Internal test"}, "owner", "pre_acquisition")
        self.runtime.initiative_action(item["id"], {"action": "observe", "value": 9, "source_id": self.source["id"], "as_of_date": "2026-01-01"}, "owner", "pre_acquisition")
        with self.assertRaisesRegex(ValidationError, "authority"): self.runtime.initiative_action(item["id"], {"action": "pilot", "rationale": "Test"}, "reviewer", "pre_acquisition")

    def test_original_blob_integrity(self):
        (self.runtime.blobs / self.source["sha256"]).write_bytes(b"tampered")
        with self.assertRaisesRegex(ValidationError, "integrity"): self.runtime.source_bytes(self.source["id"])

    def test_xlsx_formula_and_cached_value_not_lost(self):
        from openpyxl import Workbook
        workbook = Workbook(); workbook.active["A1"] = "=1+2"
        stream = io.BytesIO(); workbook.save(stream)
        rows = extract(stream.getvalue(), "test.xlsx")
        self.assertEqual(rows[0]["locator"], "sheet:Sheet!A1")
        self.assertTrue(rows[0]["formula"])
        self.assertIsNone(rows[0]["cached_value"])

    def test_http_roles_and_real_roundtrip(self):
        tokens = {role: role + "-" + "x" * 32 for role in ("owner", "reviewer", "worker")}
        server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(self.runtime, tokens))
        thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
        origin = f"http://127.0.0.1:{server.server_port}"
        try:
            for token, path, expected in ((None, "/snapshot", 401), (tokens["worker"], "/snapshot", 403)):
                request = Request(origin + path, headers={"Authorization": "Bearer " + token} if token else {})
                with self.assertRaises(HTTPError) as caught: urlopen(request, timeout=3)
                self.assertEqual(caught.exception.code, expected)
            request = Request(origin + "/snapshot", headers={"Authorization": "Bearer " + tokens["owner"]})
            with urlopen(request, timeout=3) as response:
                self.assertEqual(json.load(response)["business"]["business_id"], "alpha")
            body = json.dumps({"action": "read"}).encode()
            request = Request(origin + "/notebook/jobs", data=body, headers={"Authorization": "Bearer " + tokens["reviewer"], "Content-Type": "application/json"})
            with self.assertRaises(HTTPError) as caught: urlopen(request, timeout=3)
            self.assertEqual(caught.exception.code, 403)
        finally:
            server.shutdown(); server.server_close(); thread.join()


if __name__ == "__main__":
    unittest.main()
