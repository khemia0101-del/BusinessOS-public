"""Deterministic calculations. Inputs are decimal strings; outputs never use floats."""

from calendar import monthrange
from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


class ValidationError(ValueError):
    pass


def decimal(value, label="amount"):
    if value is None or isinstance(value, bool):
        raise ValidationError(f"{label} is required; missing is not zero")
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValidationError(f"{label} must be numeric") from None
    if not result.is_finite():
        raise ValidationError(f"{label} must be finite")
    return result


def money(value):
    return str(decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def required(row, fields):
    for field in fields:
        if field not in row or row[field] is None or row[field] == "":
            raise ValidationError(f"{field} is required")


def date_value(value):
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        raise ValidationError("Dates must be YYYY-MM-DD") from None


def normalize_period(period, adjustments):
    required(period, ("id", "start", "end", "basis", "status", "currency", "earnings_definition", "reported_earnings", "revenue", "source_ids"))
    start, end = date_value(period["start"]), date_value(period["end"])
    if start > end:
        raise ValidationError("Period start must precede end")
    if period["basis"] not in ("cash", "accrual"):
        raise ValidationError("Accounting basis must be cash or accrual")
    if period["status"] not in ("actual", "forecast"):
        raise ValidationError("Period status must be actual or forecast")
    if period["earnings_definition"] not in ("net_income", "ebitda", "sde"):
        raise ValidationError("Explicit earnings definition required")
    if not isinstance(period["currency"], str) or len(period["currency"]) != 3 or not period["currency"].isalpha() or not period["currency"].isupper():
        raise ValidationError("Currency must be a three-letter uppercase code")
    if not isinstance(period["source_ids"], list) or not period["source_ids"]:
        raise ValidationError("Period needs source IDs")
    earnings = decimal(period["reported_earnings"])
    seen, accepted = set(), []
    for adjustment in adjustments:
        required(adjustment, ("id", "period_id", "classification", "accepted", "amount", "source_ids", "rationale"))
        if adjustment["id"] in seen:
            raise ValidationError("Duplicate adjustment ID")
        seen.add(adjustment["id"])
        if adjustment["period_id"] != period["id"]:
            continue
        if not isinstance(adjustment["accepted"], bool):
            raise ValidationError("accepted must be boolean")
        if adjustment["accepted"]:
            if adjustment["classification"] == "unsupported" or not adjustment["source_ids"]:
                raise ValidationError("Unsupported adjustments cannot be accepted")
            required(adjustment, ("recurrence_test", "replacement_cost_test"))
            if adjustment["recurrence_test"] != "passed" or adjustment["replacement_cost_test"] != "passed":
                raise ValidationError("Accepted adjustment needs recurrence and replacement-cost tests")
            amount = decimal(adjustment["amount"])
            if adjustment["classification"] in ("replacement_cost", "under_recorded_expense") and amount > 0:
                raise ValidationError("Replacement and missing expenses must reduce earnings")
            earnings += amount
            accepted.append(adjustment["id"])
    return {**period, "revenue": money(period["revenue"]), "reported_earnings": money(period["reported_earnings"]),
            "normalized_earnings": money(earnings), "accepted_adjustment_ids": accepted}


def historical_ltm(periods):
    """Exactly twelve contiguous, complete actual months; never annualize a stub."""
    if len(periods) != 12:
        raise ValidationError("Historical LTM requires twelve complete actual months")
    rows = sorted(periods, key=lambda p: p["start"])
    previous = None
    identity = {(p["currency"], p["basis"], p["earnings_definition"]) for p in rows}
    if len(identity) != 1:
        raise ValidationError("LTM cannot mix currencies, bases, or earnings definitions")
    for row in rows:
        start, end = date_value(row["start"]), date_value(row["end"])
        if row["status"] != "actual":
            raise ValidationError("Forecast months cannot enter historical LTM")
        if start.day != 1 or end != date(start.year, start.month, monthrange(start.year, start.month)[1]):
            raise ValidationError("LTM requires complete calendar months")
        if previous and (start - previous).days != 1:
            raise ValidationError("LTM months must be contiguous and non-overlapping")
        previous = end
    return {"start": rows[0]["start"], "end": rows[-1]["end"], "status": "actual",
            "currency": rows[0]["currency"], "earnings_definition": rows[0]["earnings_definition"],
            "revenue": money(sum(decimal(r["revenue"]) for r in rows)),
            "normalized_earnings": money(sum(decimal(r["normalized_earnings"]) for r in rows)),
            "period_ids": [r["id"] for r in rows]}


def reconcile(row):
    required(row, ("id", "source_a", "source_b", "amount_a", "amount_b", "status"))
    if row["source_a"] == row["source_b"]:
        raise ValidationError("Reconciliation requires distinct sources")
    difference = decimal(row["amount_a"]) - decimal(row["amount_b"])
    if row["status"] == "reconciled" and difference != 0:
        raise ValidationError("Reconciled amounts must match exactly")
    if row["status"] == "explained" and not row.get("explanation", "").strip():
        raise ValidationError("Explained differences require an explanation")
    if row["status"] not in ("open", "reconciled", "explained", "waived"):
        raise ValidationError("Invalid reconciliation status")
    if row["status"] == "waived":
        required(row, ("review_id",))
    return {**row, "difference": money(difference)}


def working_capital(components):
    """Explicit included operating balances; exclude cash and financing debt."""
    allowed = {"receivables": 1, "inventory": 1, "retainage": 1, "underbillings": 1,
               "prepaids": 1, "payables": -1, "overbillings": -1, "customer_deposits": -1,
               "accrued_operating_liabilities": -1}
    if not components:
        raise ValidationError("Working-capital components are required")
    unknown = set(components) - set(allowed)
    if unknown:
        raise ValidationError("Unsupported working-capital component")
    total = Decimal(0)
    for key, value in components.items():
        amount = decimal(value, key)
        if amount < 0:
            raise ValidationError("Enter nonnegative component balances; signs are determined by account type")
        total += amount * allowed[key]
    return {"net_working_capital": money(total), "included_components": components,
            "note": "Transaction-specific inclusion policy; not a negotiated working-capital peg."}


def scenario(row):
    required(row, ("name", "revenue", "gross_margin", "operating_cost", "replacement_cost", "cash_taxes", "capex", "working_capital_increase", "annual_debt_service", "opening_cash", "minimum_cash", "multiple", "debt", "excess_cash", "transaction_fees"))
    values = {key: decimal(row[key], key) for key in row if key not in ("name", "source_ids", "assumptions")}
    if not 0 <= values["gross_margin"] <= 1:
        raise ValidationError("Gross margin must be between zero and one")
    for key in ("revenue", "operating_cost", "replacement_cost", "cash_taxes", "capex", "annual_debt_service", "minimum_cash", "multiple", "debt", "excess_cash", "transaction_fees"):
        if values[key] < 0:
            raise ValidationError(f"{key} must be nonnegative")
    earnings = values["revenue"] * values["gross_margin"] - values["operating_cost"] - values["replacement_cost"]
    available = earnings - values["cash_taxes"] - values["capex"] - values["working_capital_increase"]
    cash_flow = available - values["annual_debt_service"]
    ending_cash = values["opening_cash"] + cash_flow
    ev = earnings * values["multiple"] if earnings > 0 else None
    equity = ev - values["debt"] + values["excess_cash"] if ev is not None else None
    return {"name": row["name"], "inputs": row, "normalized_ebitda": money(earnings),
            "cash_available_for_debt_service": money(available),
            "debt_service_coverage": str((available / values["annual_debt_service"]).quantize(Decimal("0.001"))) if values["annual_debt_service"] else None,
            "cash_flow_after_debt_service": money(cash_flow), "ending_cash": money(ending_cash),
            "funding_gap": money(max(Decimal(0), values["minimum_cash"] - ending_cash)),
            "enterprise_value": money(ev) if ev is not None else None,
            "equity_value": money(equity) if equity is not None else None,
            "buyer_cash_before_financing": money(equity + values["transaction_fees"]) if equity is not None else None,
            "valuation_note": "Assumption-based scenario, not an appraisal. Negative earnings require another valuation method."}


def project_cash(opening_cash, months, initiatives, capacity):
    """Monthly incremental cases with explicit mutually-exclusive benefit groups."""
    required(capacity, ("monthly_hours", "minimum_cash"))
    available_hours = decimal(capacity["monthly_hours"])
    minimum_cash = decimal(capacity["minimum_cash"])
    if available_hours < 0 or minimum_cash < 0:
        raise ValidationError("Capacity and minimum cash must be nonnegative")
    groups, ids = set(), set()
    month_keys = [m.get("period") for m in months]
    if len(month_keys) != len(set(month_keys)):
        raise ValidationError("Duplicate projection periods")
    for index, key in enumerate(month_keys):
        start = date_value(str(key) + "-01")
        if index:
            previous = date_value(month_keys[index - 1] + "-01")
            if (start.year * 12 + start.month) - (previous.year * 12 + previous.month) != 1:
                raise ValidationError("Projection months must be chronological and contiguous")
    for initiative in initiatives:
        required(initiative, ("id", "benefit_group", "start_month", "ramp_months", "setup_cost", "monthly_cost", "monthly_cash_benefit", "monthly_hours"))
        if initiative["id"] in ids or initiative["benefit_group"] in groups:
            raise ValidationError("Duplicate initiative or overlapping benefit group; model combined effect explicitly")
        ids.add(initiative["id"])
        groups.add(initiative["benefit_group"])
        for key in ("setup_cost", "monthly_cost", "monthly_cash_benefit", "monthly_hours"):
            if decimal(initiative[key]) < 0:
                raise ValidationError(f"{key} must be nonnegative")
        for key in ("start_month", "ramp_months"):
            if type(initiative[key]) is not int or initiative[key] < 1:
                raise ValidationError(f"{key} must be a positive integer")
    balances = {case: decimal(opening_cash) for case in ("baseline", "base", "downside", "upside")}
    results = []
    for index, month in enumerate(months, 1):
        required(month, ("period", "net_cash_flow"))
        baseline_flow = decimal(month["net_cash_flow"])
        active = [i for i in initiatives if index >= i["start_month"]]
        hours = sum(decimal(i["monthly_hours"]) for i in active)
        if hours > available_hours:
            raise ValidationError(f"Capacity exceeded in {month['period']}; sequence or resize initiatives")
        for case, factor in (("baseline", Decimal(0)), ("base", Decimal(1)), ("downside", Decimal("0.5")), ("upside", Decimal("1.25"))):
            impact = Decimal(0)
            if case != "baseline":
                for i in active:
                    ramp = min(Decimal(1), Decimal(index - i["start_month"] + 1) / i["ramp_months"])
                    impact += decimal(i["monthly_cash_benefit"]) * ramp * factor - decimal(i["monthly_cost"])
                    if index == i["start_month"]:
                        impact -= decimal(i["setup_cost"])
            balances[case] += baseline_flow + impact
            results.append({"period": month["period"], "scenario": case, "incremental_cash_flow": money(impact),
                            "ending_cash": money(balances[case]), "funding_gap": money(max(Decimal(0), minimum_cash - balances[case]))})
    return results
