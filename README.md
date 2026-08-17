# BusinessOS

BusinessOS is a reusable operating system for understanding, underwriting, and improving a business. Each company receives its own isolated VM, private configuration, integrations, memory, and dashboard.

The repository contains the generic operating contract. Company facts and secrets do not belong in the repository; they are supplied through `instance/business.yaml`, `.env`, and connected source systems.

## Start Here

1. Copy `instance/business.example.yaml` to the private runtime path `instance/business.yaml`.
2. Copy `.env.example` to `.env` on the business VM and add credentials manually.
3. Set `BUSINESS_STAGE` to `pre_acquisition`, `transition`, or `operating`.
4. Give Hermes `HERMES_START.md` as its entry point.
5. Use `docs/underwriting/underwriting-standard.md` before acquisition.
6. Use `docs/scaling/scaling-plan-standard.md` to build the post-close plan.
7. Run the owner dashboard from `dashboard/`.

## Core Model

- Researcher understands the business and indexes evidence from every approved source.
- CGO finds growth paths across offer, channels, sales, marketing, customer friction, and operating capacity.
- Orchestrator turns research and strategy into controlled execution.
- Compliance reviews sensitive, legal, financial, customer-impacting, and regulated changes.
- Employee agents collect operational signal inside an approved communication scope.
- Temporary executors build approved, scoped work.
- Growth-system detects and executes growth and automation initiatives.
- Operations-system detects inefficiencies, waste, missing capabilities, and automatable workflows.
- Memory-system documents communications and business signals for anomaly and pattern detection.
- Quality-system enforces independent evaluation before anything ships.
- Intelligence-stack defines simulation, shadow-mode testing, organizational drag scoring, sensing, and learning loops.

## Repository Map

- `instance/`: private per-business configuration contract and example.
- `docs/underwriting/`: evidence and underwriting standards.
- `docs/scaling/`: post-acquisition plan and projection standards.
- `docs/execution/`: recommendation-to-result lifecycle.
- `dashboard/`: owner-facing operating desk.
- `agents/` and `hermes-profiles/`: roles and boundaries.
- `growth-system/`, `operations-system/`, `quality-system/`, and `intelligence-stack/`: reusable operating protocols.
- `audit/`, `tickets/`, `workstreams/`, and `memory-system/`: runtime records.

## Non-Negotiables

- Read-only research and internal drafting are allowed by default.
- Do not modify source-system records without explicit approval.
- Do not execute material business changes without an approved ticket or logged approval.
- Every extracted insight must cite a source record, ticket, conversation, or research source.
- Every deployed change needs an owner, success metric, stop condition, and rollback note.
- No agent approves its own work.
- In pre-acquisition mode, assume limited authority and read-only access except an approved narrow scope.
- Code, automations, campaigns, workflows, and external changes require independent evaluation before shipping.
- Put company-specific values in the private instance file and secrets in `.env`.
- Do not display, log, commit, or send raw credentials through chat.

## Current Credential Boundary

Credentials are managed manually in `.env`. A Vercel-style secrets page may be added later, but the current dashboard only shows whether an integration is configured and healthy.
