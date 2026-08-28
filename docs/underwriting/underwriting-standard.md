# Underwriting Standard

## Purpose

Produce a professional acquisition write-up that a buyer can use to decide whether to proceed, what to verify, how to structure the deal, and what must change after close. The report must be understandable without access to Hermes or the dashboard.

## Status Labels

Every report is one of:

- **Working:** evidence is still being collected.
- **Decision-ready with exceptions:** the material gaps are disclosed and the decision can still be made.
- **Final:** all material checks are complete or explicitly waived by the decision makers.

Never use a completion percentage alone. Show the missing material evidence beside it.

## Evidence Rules

1. Give every source a stable evidence ID, date, owner, period covered, and location.
2. Attach evidence IDs to every material fact in the report.
3. Keep seller claims, source facts, calculations, assumptions, and external research separate.
4. Record conflicts instead of silently choosing one number.
5. Mark freshness and reliability: `primary`, `derived`, `seller_statement`, or `external`.
6. Never infer zero from a missing value.
7. Keep sensitive raw records private; cite their location rather than copying them into tracked files.

## Required Work

### 1. Business and transaction

- Legal entities, ownership, deal structure, proposed price, financing, working-capital treatment, and closing conditions.
- Products or services, customer promise, pricing, geography, seasonality, and delivery model.
- Owner involvement, related parties, licenses, contracts, and change-of-control dependencies.

### 2. Financial reconstruction

Rebuild at least three full fiscal years plus trailing twelve months when available. Reconcile:

- Profit and loss to tax returns.
- Profit and loss to bank deposits or processor settlements.
- Balance sheet to debt, cash, receivables, payables, and tax records.
- Revenue to CRM, invoices, jobs, orders, or customer records when available.
- Payroll to employee roster and contractor payments.

For every reconciliation, state the source periods, difference, likely explanation, owner, and resolution status.

### 3. Normalized earnings

Show reported earnings, each proposed adjustment, adjusted earnings, and the evidence for the adjustment. Classify adjustments as:

- Owner compensation normalization
- One-time or nonrecurring
- Related-party
- Discretionary
- Buyer-required replacement cost
- Deferred or under-recorded expense
- Unsupported seller add-back

Include both the seller case and the underwriter case. Do not accept an add-back without recurrence, replacement-cost, and evidence tests.

### 4. Revenue quality

Analyze revenue by the dimensions available to the business:

- Customer and top-customer concentration
- Product, service, job, or contract type
- Channel and salesperson
- Recurring versus project-based
- New versus existing customer
- Geography
- Cohort, retention, repeat rate, cancellations, refunds, discounts, and bad debt
- Pipeline conversion and backlog quality

State which dimensions could not be tested.

### 5. Cash, working capital, and debt

- Cash conversion, collection timing, seasonality, and minimum operating cash.
- Normal working-capital range and proposed peg.
- Receivables aging, collectability, retainage, deposits, deferred revenue, and payables.
- Debt, liens, leases, guarantees, tax balances, equipment obligations, and off-balance-sheet commitments.
- Maintenance and growth capital expenditure requirements.

### 6. Operations, people, and systems

- Lead-to-cash and delivery workflow.
- Capacity, utilization, cycle time, rework, errors, complaints, and dependency bottlenecks.
- Organization, compensation, tenure, responsibilities, single points of failure, and owner replacement plan.
- Core systems, data ownership, integration gaps, access, security, and business continuity.
- Missing capabilities. For example, if a field-service business has no CRM, quantify the resulting leakage before recommending a tool.

### 7. Market, legal, and compliance

- Market size and structure, local conditions, competition, reputation, and demand drivers.
- Material contracts, licenses, permits, insurance, disputes, employment exposure, privacy, tax, and industry rules.
- Customer-facing claims and practices that create regulatory or reputational risk.

Use current primary sources for laws, pricing, and market facts. Record the research date.

### 8. Downside and deal protection

Model at least base, downside, and severe-downside cases. Each scenario must state:

- Revenue and margin assumptions
- Working-capital and capital-expenditure needs
- Debt-service impact when financing is known
- Owner replacement or key-person cost
- Liquidity runway and covenant headroom when applicable

Translate material risks into a mitigation, diligence condition, price adjustment, escrow, representation, earn-out, or walk-away condition.

## Required Output

1. Executive decision brief
2. Company and transaction overview
3. Evidence coverage and unresolved conflicts
4. Historical and normalized financials
5. Revenue quality and customer economics
6. Cash flow, working capital, debt, and capital needs
7. Operations, people, systems, market, and compliance
8. Risk register and deal protections
9. Valuation and return scenarios, when deal terms are available
10. First 100-day priorities
11. Missing evidence and seller questions
12. Recommendation: proceed, proceed with conditions, pause, or decline

The machine-readable output must validate against `schemas/underwriting.schema.json`.

Run `python scripts/validate_reports.py underwriting /private/path/report.json` before review or promotion. Working reports may have incomplete financials. Decision-ready and final reports require sourced periods, reconciliations, and base/downside/severe-downside cases. A final report cannot contain open reconciliations or unreceived material evidence unless explicitly waived; each waiver records approver, date, and reason. Each remaining `material_gaps` entry must exactly match a waived request in `missing_evidence`. Decision-ready exceptions must also be disclosed in the recommendation's conditions.

Use registered source IDs in `source_ids`, risk `evidence`, and reconciliation `source_a` / `source_b`. The validator rejects dangling references, duplicate IDs, unexplained differences, and accepted unsupported add-backs. Validation is a minimum consistency check, not proof that sources are true, calculations are correct, coverage is sufficient, or a waiver is authorized. The independent evaluator must verify those against the underlying evidence and logged decisions.

## Confidence

Confidence is reported by section, not as one vague overall score:

- **High:** primary sources reconcile and cover the material period.
- **Medium:** sufficient evidence exists, but a disclosed assumption or unresolved difference can change the conclusion.
- **Low:** material evidence is missing, stale, seller-provided only, or contradictory.

The executive brief must name every low-confidence issue that could change price, terms, or the acquisition decision.
