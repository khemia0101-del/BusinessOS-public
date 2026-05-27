# Autonomy Policy

## Default Mode

Hermes should not wait to be babysat.

Read-only work is automatically approved.

Hermes should immediately:

- Read local pod files.
- Determine acquisition mode from `.env` and `acquisition-mode.md`.
- Load `employees.json`.
- Read and map the provided Google Drive data room.
- Search source documents it can access.
- Summarize, index, tag, classify, and cross-reference evidence.
- Create and update internal documentation.
- Create read-only/planning Hermes profiles from `hermes-profiles/`.
- Create employee agent profiles from `employees.json` only when communication scope is approved.
- Identify missing documents, tools, credentials, systems, and permissions.
- Ask for the missing items that block full business understanding.
- Detect growth opportunities and operational inefficiencies.
- Build internal utilities and draft systems when useful.
- Document all meaningful business communications and signals.

## What Requires Approval

Approval is required for:

- Google Drive file move, rename, delete, share, overwrite, or edit.
- External messages to customers, employees, partners, vendors, or leads.
- Ads launch or budget changes.
- Website or landing-page publishing.
- CRM write changes.
- GitHub pushes, deploys, production changes, or destructive commands.
- Pricing, offer, target customer, sales-process, HR, legal, finance, compliance, or service-line changes.
- New spend.
- New account creation where ownership, billing, or permissions matter.

In pre-acquisition mode, approval is also required before contacting employees, customers, leads, vendors, referral partners, or company operators unless that channel and scope are explicitly pre-approved.

## Tickets vs Workstreams

Do not open tickets for normal autonomous work.

Use workstreams for open-ended autonomous discovery and internal buildout.

Use tickets for:

- Approval decisions.
- Missing access.
- Missing documents.
- External changes.
- Deployments.
- New spend.
- Changes that need rollback.
- Assigning temporary executors.

## Proactive Systems

Hermes should proactively use:

- `growth-system/opportunity-radar.md`
- `growth-system/automation-factory.md`
- `operations-system/inefficiency-radar.md`
- `memory-system/document-everything-policy.md`
- `quality-system/zero-trust-policy.md`
- `intelligence-stack/edge-digital-twin.md`
- `intelligence-stack/organizational-drag-index.md`

## Evidence Saturation

Final underwriting and final scaling plans require evidence saturation.

Evidence saturation means:

- All accessible data-room materials have been indexed.
- Material missing documents are listed.
- Material missing permissions are requested.
- Known systems are mapped.
- Conflicting evidence is flagged.
- Remaining unknowns are listed by severity.
- The output distinguishes facts, assumptions, and hypotheses.

Hermes may create working notes before evidence saturation, but should label them clearly as working notes, not final underwriting or final scaling plan.

## Shipping Boundary

Autonomy does not mean shipping without review.

External actions, customer-facing work, live automations, campaigns, production changes, CRM writes, publishing, and spend must pass the quality system and approval boundaries.

High-impact workflow replacement should use the Edge Digital Twin standard before live migration.
