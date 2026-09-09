"""Cost-supported WIP diagnostics; never certify seller estimates."""
from decimal import Decimal
from businessos.finance import ValidationError, decimal, money, required


def calculate_wip(job):
    fields = ("contract_value", "approved_change_orders", "cost_incurred", "cost_to_complete", "billings", "collections")
    required(job, ("id", "source_ids", "costs_verified", *fields))
    values = {field: decimal(job[field], field) for field in fields}
    if any(values[field] < 0 for field in fields if field != "approved_change_orders"):
        raise ValidationError("WIP amounts must be nonnegative except approved change orders")
    total_cost = values["cost_incurred"] + values["cost_to_complete"]
    price = values["contract_value"] + values["approved_change_orders"]
    if total_cost <= 0 or price < 0 or not isinstance(job["costs_verified"], bool):
        raise ValidationError("WIP requires positive estimated cost, nonnegative contract value, and verification status")
    completion = values["cost_incurred"] / total_cost
    earned = price * completion
    return {"job_id": job["id"], "inputs": job, "completion_fraction": str(completion.quantize(Decimal("0.0001"))),
            "estimated_total_cost": money(total_cost), "estimated_total_profit": money(price - total_cost),
            "earned_revenue": money(earned), "underbilling": money(max(Decimal(0), earned - values["billings"])),
            "overbilling": money(max(Decimal(0), values["billings"] - earned)),
            "uncollected_billings": money(values["billings"] - values["collections"]),
            "remaining_revenue": money(price - earned), "expected_contract_loss": money(max(Decimal(0), total_cost - price)),
            "readiness": "costs_confirmed_by_input" if job["costs_verified"] else "unverified_cost_to_complete",
            "note": "Cost-to-cost diagnostic only. Independent review must establish job costs, change orders, collectability, and accounting treatment."}
