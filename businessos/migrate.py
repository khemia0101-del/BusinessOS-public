"""Explicit v1 migration: mappings supply dates, basis and source versions."""

from businessos.finance import ValidationError, required


def migrate_legacy(report, mapping):
    if report.get("schema_version") == 2:
        raise ValidationError("Report is already version 2")
    required(mapping, ("report_id", "periods", "adjustments", "reconciliations", "citations", "coverage", "scenarios"))
    # Do not infer actual/forecast, fiscal dates, or source identities from labels.
    return {"schema_version": 2, "report_id": mapping["report_id"], "business_id": report["business_id"],
            "as_of_date": report["as_of_date"], "periods": mapping["periods"], "adjustments": mapping["adjustments"],
            "reconciliations": mapping["reconciliations"], "citations": mapping["citations"],
            "coverage": mapping["coverage"], "scenarios": mapping["scenarios"], "ltm_period_ids": mapping.get("ltm_period_ids", []),
            "recommendation": {"decision": "pause", "summary": "Migrated report requires recalculation and independent evidence review.",
                               "conditions": ["Review original legacy recommendation and every mapped input"]},
            "legacy_report_id": report["report_id"], "risks": report.get("risks", [])}
