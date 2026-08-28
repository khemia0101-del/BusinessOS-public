"""Synthetic fixtures only; no company evidence or financial claims."""

from copy import deepcopy
import unittest

from scripts.validate_reports import validate_report


def source(identifier):
    return {"id": identifier, "title": "Synthetic evidence", "location": f"fixture://{identifier}", "retrieved_at": "2026-08-28T10:00:00Z"}


def underwriting(status="final"):
    return {
        "report_id": "test-report", "business_id": "test-business", "as_of_date": "2026-08-28", "status": status,
        "recommendation": {"decision": "pause", "summary": "Synthetic test only", "conditions": ["Independent review"], "confidence": "medium"},
        "evidence_coverage": [{"domain": "finance", "confidence": "medium", "material_gaps": [], "source_ids": ["ledger", "bank"]}],
        "financial_baseline": {
            "currency": "USD", "periods": [{"label": "2025", "revenue": 100, "gross_profit": 50, "reported_earnings": 20, "normalized_earnings": 20, "source_ids": ["ledger"]}],
            "normalization_adjustments": [],
            "reconciliations": [{"label": "Deposits", "source_a": "ledger", "source_b": "bank", "difference": 0, "status": "reconciled"}],
        },
        "scenarios": [{"name": name, "assumptions": ["Synthetic assumption"], "revenue": 100, "normalized_earnings": 20, "cash_need": 0} for name in ("base", "downside", "severe_downside")],
        "risks": [], "missing_evidence": [],
        "sources": [{**source(name), "kind": name, "reliability": "primary"} for name in ("ledger", "bank")],
    }


def scaling(status="approved"):
    return {
        "plan_id": "test-plan", "business_id": "test-business", "as_of_date": "2026-08-28", "status": status,
        "horizons": {name: {"objective": "Synthetic objective", "outcomes": ["Synthetic outcome"]} for name in ("days_0_30", "days_31_100", "months_4_12", "years_2_3")},
        "baseline": [{"id": "revenue", "name": "Revenue", "value": 100, "unit": "USD", "as_of_date": "2026-08-28", "confidence": "medium", "source_ids": ["ledger"]}],
        "initiatives": [{
            "id": "test-initiative", "title": "Synthetic initiative", "problem": "Synthetic problem", "objective": "Test validation", "owner": "test-owner", "state": "proposed",
            "actions": ["Review synthetic plan"], "channels": [],
            "costs": {"currency": "USD", "one_time": 10, "monthly": 1, "internal_hours": 2},
            "expected_impact": {"base": 5, "downside": 0, "upside": 10, "calculation": "Synthetic fixture only"},
            "proof": {"method": "historical_backtest", "plan": "Replay synthetic events", "promotion_gate": "Independent test review"},
            "success_metrics": ["Test passes"], "stop_conditions": ["Test fails"], "rollback": "Discard synthetic output",
        }],
        "projections": [{"scenario": name, "period": "2027", "revenue": 100, "gross_profit": 50, "operating_expense": 30, "cash_balance": 20, "assumption_ids": ["demand"]} for name in ("baseline", "base", "downside", "upside")],
        "assumptions": [{"id": "demand", "statement": "Synthetic demand", "basis": "Fixture only", "confidence": "low", "source_ids": ["ledger"]}],
        "sources": [source("ledger")],
    }


class ReportTests(unittest.TestCase):
    def assertValid(self, kind, report):
        self.assertEqual(validate_report(kind, report), [])

    def assertInvalid(self, kind, report, text=None):
        errors = validate_report(kind, report)
        self.assertTrue(errors)
        if text:
            self.assertIn(text, "\n".join(errors))

    def test_complete_underwriting_passes(self):
        self.assertValid("underwriting", underwriting())

    def test_incomplete_working_underwriting_is_allowed(self):
        report = underwriting("working")
        report["sources"] = []
        report["evidence_coverage"][0]["source_ids"] = []
        report["financial_baseline"]["periods"] = []
        report["financial_baseline"]["reconciliations"] = []
        del report["scenarios"]
        self.assertValid("underwriting", report)
        report["status"] = "final"
        self.assertInvalid("underwriting", report)

    def test_review_ready_underwriting_needs_baseline_sources_and_scenarios(self):
        for status in ("decision_ready_with_exceptions", "final"):
            for field in ("periods", "reconciliations"):
                with self.subTest(status=status, field=field):
                    report = underwriting(status)
                    report["financial_baseline"][field] = []
                    self.assertInvalid("underwriting", report)
            for field in ("sources", "scenarios"):
                with self.subTest(status=status, field=field):
                    report = underwriting(status)
                    report[field] = []
                    self.assertInvalid("underwriting", report)

    def test_final_requires_material_gaps_received_or_waived(self):
        report = underwriting()
        report["missing_evidence"] = [{"request": "Tax return", "reason": "Cross-check", "materiality": "critical", "status": "requested"}]
        self.assertInvalid("underwriting", report)
        report["missing_evidence"][0]["status"] = "waived"
        self.assertInvalid("underwriting", report, "waiver")
        report["missing_evidence"][0]["waiver"] = {"approved_by": "owner", "approved_at": "2026-08-28T10:00:00Z", "reason": "Explicitly accepted limitation"}
        report["evidence_coverage"][0]["material_gaps"] = ["Tax return"]
        self.assertValid("underwriting", report)

    def test_final_cannot_hide_material_gap_outside_requests(self):
        report = underwriting()
        report["evidence_coverage"][0]["material_gaps"] = ["Undisclosed missing evidence"]
        self.assertInvalid("underwriting", report, "matching waived request")

    def test_open_reconciliation_cannot_be_final(self):
        report = underwriting()
        report["financial_baseline"]["reconciliations"][0]["status"] = "open"
        self.assertInvalid("underwriting", report)
        report["status"] = "decision_ready_with_exceptions"
        self.assertValid("underwriting", report)
        report["recommendation"]["conditions"] = []
        self.assertInvalid("underwriting", report, "disclose the exceptions")

    def test_reconciliation_must_compare_distinct_sources_and_explain_difference(self):
        report = underwriting()
        row = report["financial_baseline"]["reconciliations"][0]
        row["source_b"] = "ledger"
        self.assertInvalid("underwriting", report, "distinct sources")
        row["source_b"] = "bank"
        row["difference"] = 5
        self.assertInvalid("underwriting", report, "nonzero difference")
        row["status"] = "explained"
        self.assertInvalid("underwriting", report, "need an explanation")
        row["explanation"] = "Timing difference supported by evidence"
        self.assertValid("underwriting", report)

    def test_unsupported_adjustment_cannot_be_accepted(self):
        report = underwriting()
        report["financial_baseline"]["normalization_adjustments"] = [{"label": "Seller claim", "amount": 10, "classification": "unsupported", "accepted": True, "rationale": "No support", "source_ids": ["ledger"]}]
        self.assertInvalid("underwriting", report, "unsupported adjustments")

    def test_unknown_source_duplicate_ids_and_scenarios_fail(self):
        report = underwriting()
        report["financial_baseline"]["periods"][0]["source_ids"] = ["invented"]
        self.assertInvalid("underwriting", report, "unknown reference")
        report = underwriting()
        report["sources"].append(deepcopy(report["sources"][0]))
        self.assertInvalid("underwriting", report, "duplicate IDs")
        report = underwriting()
        report["scenarios"].append(deepcopy(report["scenarios"][0]))
        self.assertInvalid("underwriting", report, "duplicate scenario")

    def test_dates_and_nonfinite_numbers_are_validated(self):
        report = underwriting()
        report["as_of_date"] = "2026-99-99"
        self.assertInvalid("underwriting", report)
        report = underwriting()
        report["financial_baseline"]["periods"][0]["revenue"] = float("nan")
        self.assertInvalid("underwriting", report, "finite")

    def test_complete_scaling_plan_and_closed_initiative_pass(self):
        report = scaling()
        self.assertValid("scaling-plan", report)
        report["initiatives"][0]["state"] = "closed"
        self.assertValid("scaling-plan", report)

    def test_incomplete_working_plan_is_allowed_but_not_approved(self):
        report = scaling("working")
        for key in ("baseline", "initiatives", "projections", "assumptions", "sources"):
            report[key] = []
        self.assertValid("scaling-plan", report)
        report["status"] = "approved"
        self.assertInvalid("scaling-plan", report)

    def test_review_ready_scaling_needs_evidence_and_actions(self):
        for field in ("baseline", "initiatives", "projections", "sources", "assumptions"):
            with self.subTest(field=field):
                report = scaling("ready_for_review")
                report[field] = []
                self.assertInvalid("scaling-plan", report)
        for field in ("actions", "success_metrics", "stop_conditions"):
            with self.subTest(field=field):
                report = scaling()
                report["initiatives"][0][field] = []
                self.assertInvalid("scaling-plan", report)

    def test_projection_references_and_comparable_scenarios(self):
        report = scaling()
        report["projections"][0]["assumption_ids"] = ["invented"]
        self.assertInvalid("scaling-plan", report, "unknown reference")
        report = scaling()
        report["projections"][0]["period"] = "different-period"
        self.assertInvalid("scaling-plan", report, "for comparison")
        report = scaling()
        report["projections"].append(deepcopy(report["projections"][0]))
        self.assertInvalid("scaling-plan", report, "duplicate baseline")

    def test_blank_ready_report_fields_are_rejected(self):
        report = scaling()
        report["initiatives"][0]["owner"] = "   "
        self.assertInvalid("scaling-plan", report, "must not be blank")


if __name__ == "__main__":
    unittest.main()
