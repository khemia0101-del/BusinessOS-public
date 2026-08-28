"""Validate a report's structure, readiness gates, and evidence references.

This checks consistency, not the truth of evidence or authority to approve work.
An independent evaluator still reviews the underlying sources and calculations.
"""

import argparse
import json
import math
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


SCHEMAS = Path(__file__).resolve().parents[1] / "schemas"
KINDS = ("underwriting", "scaling-plan")


def walk(value, path="report"):
    yield path, value
    if isinstance(value, dict):
        for key, child in value.items():
            yield from walk(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk(child, f"{path}[{index}]")


def validate_report(kind, report):
    if kind not in KINDS:
        raise ValueError(f"Unknown report kind: {kind}")
    schema = json.loads((SCHEMAS / f"{kind}.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = [f"{error.json_path}: {error.message}" for error in validator.iter_errors(report)]
    if errors:
        return errors

    sources = {source["id"] for source in report.get("sources", [])}
    assumptions = {assumption["id"] for assumption in report.get("assumptions", [])}
    ready = report["status"] in {"final", "decision_ready_with_exceptions", "ready_for_review", "approved", "active"}

    for path, value in walk(report):
        if isinstance(value, float) and not math.isfinite(value):
            errors.append(f"{path}: numbers must be finite")
        if ready and isinstance(value, str) and not value.strip():
            errors.append(f"{path}: must not be blank in a review-ready report")
        if isinstance(value, list) and value and all(isinstance(item, dict) and "id" in item for item in value):
            ids = [item["id"] for item in value]
            if len(ids) != len(set(ids)):
                errors.append(f"{path}: duplicate IDs")
        if not isinstance(value, dict):
            continue
        for key, registry in (("source_ids", sources), ("evidence", sources), ("assumption_ids", assumptions)):
            for reference in value.get(key, []):
                if reference not in registry:
                    errors.append(f"{path}.{key}: unknown reference {reference!r}")
        for key in ("source_a", "source_b"):
            if key in value and value[key] not in sources:
                errors.append(f"{path}.{key}: unknown source {value[key]!r}")

    if kind == "underwriting":
        names = [scenario["name"] for scenario in report.get("scenarios", [])]
        if len(names) != len(set(names)):
            errors.append("scenarios: duplicate scenario names")
        periods = [period["label"] for period in report["financial_baseline"]["periods"]]
        if len(periods) != len(set(periods)):
            errors.append("financial_baseline.periods: duplicate labels")
        for row in report["financial_baseline"]["reconciliations"]:
            if row["source_a"] == row["source_b"]:
                errors.append("reconciliations: must compare two distinct sources")
            if row["status"] == "reconciled" and row["difference"] != 0:
                errors.append("reconciliations: a nonzero difference must be explained, open, or waived")
            if row["status"] == "explained" and not row.get("explanation", "").strip():
                errors.append("reconciliations: explained differences need an explanation")
        for row in report["financial_baseline"]["normalization_adjustments"]:
            if row["classification"] == "unsupported" and row["accepted"]:
                errors.append("normalization_adjustments: unsupported adjustments cannot be accepted")
        if report["status"] == "final":
            waived = {row["request"] for row in report["missing_evidence"] if row["status"] == "waived"}
            for domain in report["evidence_coverage"]:
                for gap in domain["material_gaps"]:
                    if gap not in waived:
                        errors.append(f"evidence_coverage: final material gap {gap!r} needs a matching waived request")
        if report["status"] == "decision_ready_with_exceptions" and not report["recommendation"]["conditions"]:
            errors.append("recommendation.conditions: disclose the exceptions and required follow-up")
    elif ready:
        by_period = {}
        for row in report["projections"]:
            scenarios = by_period.setdefault(row["period"], set())
            if row["scenario"] in scenarios:
                errors.append(f"projections: duplicate {row['scenario']} for {row['period']}")
            scenarios.add(row["scenario"])
        for period, scenarios in by_period.items():
            if scenarios != {"baseline", "base", "downside", "upside"}:
                errors.append(f"projections: {period} needs baseline, base, downside, and upside for comparison")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kind", choices=KINDS)
    parser.add_argument("report", type=Path)
    arguments = parser.parse_args()
    try:
        report = json.loads(arguments.report.read_text(encoding="utf-8"))
        errors = validate_report(arguments.kind, report)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Cannot validate report: {error}\n")
    if errors:
        parser.exit(1, "\n".join(errors) + "\n")
    print("Report validation passed. Independent evidence and approval review is still required.")


if __name__ == "__main__":
    main()
