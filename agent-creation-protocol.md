# Agent Creation Protocol

## Purpose

The system structure is flexible. The pod starts with default core agents, but the orchestrator may propose new permanent agents when a function becomes recurring and deserves persistent context.

## When To Propose A Permanent Agent

The orchestrator may propose creating a new permanent agent when:

- A recurring function appears more than 3 times.
- A domain requires persistent context.
- A workstream has its own metrics, docs, tools, and recurring decisions.
- Temporary executors are repeatedly needed for the same category.

Examples:

- SEO Agent.
- Ads Agent.
- Sales Ops Agent.
- Outreach Agent.
- Social Media Agent.
- CRM Agent.
- Data Agent.
- Finance Agent.
- Recruiting Agent.
- Compliance Agent.

## Automatic Profile Creation

Core operating profiles are automatically approved:

- Orchestrator.
- Researcher.
- CGO.
- Compliance.

Domain profiles may be created automatically when they are read-only, planning-only, or documentation-only.

Examples:

- SEO Agent for SEO research and planning.
- Ads Agent for ad-account review and campaign planning.
- Sales Ops Agent for CRM and sales-process mapping.
- Outreach Agent for outreach planning.
- Social Media Agent for account inventory and calendar planning.
- Finance Agent for source-linked financial normalization.
- Data Agent for data mapping and dashboard planning.

Automatic profile creation must be logged in `audit/profile-creation-log.md`.

## Approval Still Required

The orchestrator cannot silently grant a new profile external write authority, spend authority, deployment authority, HR authority, customer messaging authority, or permission to modify source systems.

It must create a ticket or access request when the profile needs:

- Write access.
- API keys.
- Customer messaging permissions.
- Ads launch permissions.
- GitHub write permissions.
- CRM write permissions.
- Google Drive edit/share/move/delete permissions.
- Payment, billing, or spend authority.
- Legal, HR, compliance, or finance-sensitive execution authority.

The approval request should include scope, permissions, tools, data access, risks, success metrics, and rollback plan.

## Temporary Executors

Temporary executors can be proposed for approved scoped work when:

- The work has a clear objective.
- The work has a bounded data-access requirement.
- The output is reviewable.
- The executor can be destroyed or archived after completion.

## Employee Agents

Employee agents should collect signal, not manage employees directly.

They may:

- Ask structured questions.
- Receive feedback.
- Classify friction.
- Escalate risks.
- Feed the inbox.

They may not:

- Discipline employees.
- Change compensation.
- Promise policy changes.
- Give legal or HR advice.
- Collect unnecessary sensitive personal information.
