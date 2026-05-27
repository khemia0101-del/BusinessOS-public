# Acquisition Mode

## Purpose

Tell Hermes what stage the business is in and what authority exists.

Default mode: `pre_acquisition`

## Modes

### Pre-Acquisition

Use when the business has not been acquired yet or the buyer has limited access.

Default assumptions:

- Read-only data room access.
- No direct authority over company systems unless explicitly granted.
- No customer-facing changes.
- No employee management authority.
- No production changes.
- No spending.
- No system writes unless explicitly approved.
- Employee agents may be spun up only for approved communication/feedback collection and must not manage employees.

Allowed by default:

- Read data room.
- Summarize evidence.
- Build underwriting working notes.
- Map missing documents.
- Map missing tools and permissions.
- Draft questions.
- Create internal profiles.
- Create internal docs, workstreams, and analysis.
- Start employee-agent setup if names/contact/consent are provided.
- Collect employee feedback if owner/partner approves the channel and scope.

Not allowed by default:

- Change CRM, website, ads, social, email, documents, or operational systems.
- Contact customers, leads, vendors, referral partners, or employees without approved messaging scope.
- Publish content.
- Send campaigns.
- Spend money.
- Represent ownership/control of the business.

### Post-Acquisition

Use after control and authority are confirmed.

Default assumptions:

- Broader operational work may proceed through the approval and quality systems.
- External writes still require approval based on risk level.
- Employee agents can become recurring signal collectors if approved.
- Automation can move from shadow mode to pilot and live rollout.

## Stage Transition

Changing from `pre_acquisition` to `post_acquisition` requires a logged decision in `audit/decisions.md`.

Before transition, Hermes should confirm:

- Ownership/control status.
- System access.
- Communication authority.
- Employee communication policy.
- Customer communication authority.
- Spending authority.
- Compliance constraints.

## Pre-Acquisition Output Priorities

1. Source-linked underwriting readiness.
2. Missing document and access list.
3. Risk register.
4. Operational inefficiency hypotheses.
5. Growth upside hypotheses.
6. Questions for seller/owner/employees.
7. Edge Digital Twin candidates for post-close implementation.
