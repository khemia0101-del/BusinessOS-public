# Version 2 financial input

The runtime accepts explicit, source-linked input through `POST /reports` or `python -m businessos --business ID report input.json`. All financial amounts may be decimal strings. Null is not zero. The output includes the original inputs, deterministic results, fingerprint, material gaps, and review record.

Required root fields: `schema_version: 2`, `report_id`, `business_id`, `as_of_date`, `periods`, `adjustments`, `reconciliations`, `scenarios`, `coverage`, `citations`, `recommendation`. Optional: `ltm_period_ids`, `risks`, `legacy_report_id`.

- **Periods:** `id`, `start`, `end`, `basis` (cash/accrual), `status` (actual/forecast), `currency`, `earnings_definition` (net_income/ebitda/sde), `revenue`, `reported_earnings`, `source_ids`. Optional `period_type: fiscal_year`. Normalized earnings are calculated, never trusted from submitted totals.
- **Adjustments:** `id`, `period_id`, `classification`, signed `amount`, boolean `accepted`, `rationale`, `source_ids`, `recurrence_test`, `replacement_cost_test`. Accepted rows need both tests set to `passed`. Replacement and under-recorded expenses must reduce earnings. Unsupported adjustments cannot be accepted. Each adjustment applies only to its named period.
- **Reconciliations:** `id`, `source_a`, `source_b`, `amount_a`, `amount_b`, `status` (open/reconciled/explained/waived), explanation for explained differences, and `review_id` for waivers. Differences are recalculated. Source B must be independent evidence.
- **Citations:** `source_id`, exact `locator` from extraction (page, cell, paragraph, or line), and `claim`. These pin claims to immutable source versions; a citation does not by itself establish the claim's truth.
- **Coverage:** `id`, `status` (missing/in_progress/complete), `notes`, `source_ids` when complete. The runtime fills missing general and construction checklist items and requires independent cited sources for complete items.
- **Recommendation:** `decision` (pause/decline/proceed/proceed_with_conditions), `summary`, and `conditions` array. Unconditional proceed is rejected while material gaps exist.
- **Scenarios:** `name`, `assumptions` array, `source_ids`, plus explicit annual `revenue`, `gross_margin` (fraction), `operating_cost` (excluding owner replacement, taxes and financing), `replacement_cost`, `cash_taxes`, `capex`, `working_capital_increase`, `annual_debt_service`, `opening_cash`, `minimum_cash`, `multiple`, `debt`, `excess_cash`, `transaction_fees`. EBITDA is revenue times margin less operating/replacement costs. Cash available for debt service deducts cash taxes, capex and working capital; coverage uses this amount, not unadjusted EBITDA. Ending cash deducts debt service. Enterprise value is positive EBITDA times the disclosed multiple; nonpositive earnings return no earnings-based valuation. Equity value deducts debt and adds excess cash. No market multiple or financing term is inferred.

Historical LTM requires exactly twelve contiguous, complete actual calendar months, one currency, one basis and one earnings definition. Full fiscal-year rows may coexist with monthly detail but are not included in LTM. Annual figures and monthly detail should reconcile independently.

## Operating input

`POST /initiatives` requires `id`, `title`, `owner`, numeric `baseline`, numeric `target`, `metric`, `measurement_end`, `stop_condition`, `rollback`, `source_ids`, `benefit_group`, `setup_cost`, `monthly_cost`, `monthly_cash_benefit`, `monthly_hours`, integer `start_month`, integer `ramp_months`. Use a shared benefit group where initiatives overlap; model their combined effect before running them together. Costs and benefits are assumptions until observations establish results.

`POST /projections` accepts `opening_cash`, `months` (ordered `period`, `net_cash_flow` records), `initiatives`, and `capacity` (`monthly_hours`, `minimum_cash`). The runtime returns monthly baseline/base/downside/upside ending cash and financing gaps. Current sensitivity factors are 1.0/0.5/1.25 times ramped benefit with full costs; they are explicit scenario assumptions, not probabilities. Baseline monthly cash flows must already include seasonal revenue, operating costs, taxes, capex, debt service and working-capital changes.

`tests/test_runtime.py` provides synthetic minimal inputs and expected calculation results. Do not import test inputs into a real company as evidence.
