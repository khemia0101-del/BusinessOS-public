# Capability Registry

## Purpose

Track reusable business capabilities Hermes may create or activate.

This is not an exhaustive list. Hermes should add capabilities when new recurring functions appear.

| Capability | Profile | Utility/System | External Write Requires Approval |
| --- | --- | --- | --- |
| SEO / WordPress publishing | SEO Agent | Keyword research, article generator, WordPress uploader | Yes |
| Referral partner nurture | Referral Outreach Agent | Segmentation, email sequence, reply tracking | Yes |
| Email marketing | Email Marketing Agent | SendGrid/Resend campaign system, suppression list | Yes |
| Social media | Social Media Agent | Creative pipeline, scheduler | Yes |
| Reddit/community | Community Agent | Thread finder, comment drafter | Yes |
| Lead follow-up | Sales Ops Agent | CRM/calendar/email/SMS workflow | Yes |
| New referral prospecting | Outreach Agent | Apify/enrichment/scheduling system | Yes |
| CRM operations | CRM Agent | Deduper, stage automation, reporting | Yes |
| Finance analysis | Finance Agent | Normalization and KPI model | No for read-only |
| Data/reporting | Data Agent | Dashboard and report generator | No for local read-only |
| Ops automation | Ops Automation Agent | Workflow automation utilities | Yes when external write |

## Registry Rules

- Add capabilities as they emerge.
- Link each capability to docs, utilities, profiles, credentials, risks, and KPIs.
- Do not assume external write permission because a capability exists.
