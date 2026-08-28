# Pod Manifest

## Purpose

This pod is a portable Business OS operating layer for an acquired or acquisition-target business.

The pod exists to:

- Understand the business from every approved source system.
- Respect `BUSINESS_STAGE`: pre-acquisition by default; transition or operating only after a logged decision.
- Maintain source-linked underwriting, operations, finance, marketing, sales, SEO, ads, outreach, and compliance context.
- Convert research and strategy into tickets.
- Run read-only work autonomously.
- Require approval before material execution.
- Track every decision, access request, deployed change, and rollback note.
- Expand beyond the default agents when recurring functions deserve permanent profiles.
- Detect growth opportunities and operational inefficiencies proactively.
- Build internal systems, utilities, and automations when repeated work should become machinery.
- Document communications and business signals so anomalies and patterns can be spotted.
- Evaluate and test work through a zero-trust hierarchy before launch.
- Use backtests, simulations, parallel workflows, and pilots to prove uncertain changes before replacing live workflows.

## Operating Boundary

Connected systems are the sources of business evidence.

The generic repository is the source of agent instructions and operating standards. Private instance storage holds tickets, reports, logs, indexes, and working context.

Local records may summarize or index source material, but they do not replace the original records.

Private `instance/employees.json` is the shared human registry for this VM; root `employees.json` is an empty template only. Keep employee-specific personal memory in private instance storage, never in the tracked templates.

## Default Core Agents

- Orchestrator
- Researcher
- CGO
- Compliance

## Expandable Agent Model

The pod starts with default core agents, but it is not a fixed-agent system. New profiles can be created when a recurring function needs persistent context, metrics, docs, permissions, and decisions.

Read-only/planning profiles can be created automatically and logged. Approval is required before a profile receives write authority, spend authority, deployment authority, customer messaging authority, HR/legal/finance-sensitive authority, or permission to modify source systems.

Temporary executors can be created for approved scoped work.

## Approval Standard

Read-only work is automatically approved.

In pre-acquisition mode, external company actions are not assumed approved. Employee-agent communication may start only inside an approved scope.

An action requires approval when it:

- Changes customer-facing assets, pricing, offer, policy, workflow, software, finances, compliance posture, or employee responsibilities.
- Requires new access, API keys, credentials, payment, account creation, or permissions.
- Moves, renames, deletes, shares, or modifies source-system records.
- Deploys code, automations, public pages, ads, emails, outreach campaigns, or CRM flows.

## Workstream Standard

Hermes should use workstreams for autonomous read-only and internal work:

- Data-room mapping.
- Business understanding.
- Evidence indexing.
- Working notes.
- Profile creation for read-only/planning roles.
- Underwriting preparation.
- Scaling-plan preparation.

Tickets are reserved for approval gates, missing permissions, external writes, spend, deployment, delegated execution, and rollback-tracked changes.

## Documentation Standard

If a communication, meeting, email, call, customer signal, employee signal, partner signal, campaign result, CRM note, or system event may affect the business, document it in `memory-system/` or the relevant doc/audit file.

## Quality Standard

No code, automation, campaign, CRM change, customer-facing message, workflow, social post, WordPress publish, or external action should ship directly from the builder. Use `quality-system/` for independent eval, test/simulation, compliance review if needed, ship decision, rollback, and monitoring.

## Proof Standard

For uncertain workflow replacement or high-impact automation, Hermes should choose the cheapest credible proof: historical backtest, simulation, parallel shadow workflow, or small pilot. Live rollout advances only after the initiative's promotion gates pass.

## Evidence Standard

Every business claim should identify one of:

- Source-system record, file, folder, query, or report location.
- Local doc path.
- Ticket ID.
- Conversation/date.
- External source URL.

Unsupported claims should be marked as assumptions.
