# Setup Instructions

## 1. Confirm External Anchors

Create the private files and load the service environment as described in `docs/deployment/azure-vm-test.md`. Confirm the following without displaying credentials:

- Business identity and approved source locations in `instance/business.yaml`.
- `BUSINESS_STAGE` in the service environment.
- Availability of each configured integration, without exposing its keys.

## 2. Give Hermes Context

When starting Hermes in this folder, provide:

- This folder path.
- Approved data-room and source locations.
- Business owner / partner approval rule.
- Any current work priority.

Suggested start prompt:

```txt
You are Hermes for this business. Follow HERMES_START.md and its load order. Use approved connected sources as evidence and this repository as the operating contract. Start read-only. Do not execute material external changes without an approved ticket or logged approval.
```

## 3. First Run

Hermes should:

1. Read the core files.
2. Confirm data-room access.
3. Start read-only indexing of approved, available sources immediately.
4. Activate only the profiles needed for the current work from `hermes-profiles/`.
5. Record missing tools and permissions.
6. Create missing-document requests only when they materially block underwriting, scaling, compliance, or execution.
7. Produce working notes until evidence saturation is reached.
8. Produce final underwriting only after evidence saturation.
9. Draft the scaling plan early; mark it ready for review only after its baseline, costs, assumptions, and proof plans pass validation and independent review.

## 4. Access

Hermes must request access before using:

- Any source-system write operation.
- GitHub write operations.
- CRM.
- Sendblue.
- Ads platforms.
- Search Console.
- Analytics.
- Email sending.
- Billing or payment systems.
- Customer databases.

Read-only local documentation and analysis of already-approved readable sources do not require another approval. Merely adding an API key does not approve writes.

## 5. Reporting Cadence

- Weekly: execution status and KPI movement.
- Bi-weekly: Strategic Change Review.
- Monthly: business performance summary and priority reset.
