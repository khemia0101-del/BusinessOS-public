# BusinessOS

BusinessOS is a reusable operating system for understanding, underwriting, and improving a business. Each company receives its own isolated VM, private configuration, integrations, memory, and dashboard.

The repository contains the generic operating contract. Company facts and secrets do not belong in the repository; they are supplied through `instance/business.yaml`, `.env`, and connected source systems.

## Start Here

1. Copy `instance/business.example.yaml` to the private runtime path `instance/business.yaml`.
2. Copy `.env.example` to `.env` on the business VM and add credentials manually.
3. Set `BUSINESS_STAGE` in `.env` to `pre_acquisition`, `transition`, or `operating`. This is the only stage setting; an unset or invalid value means pre-acquisition.
4. Give Hermes `HERMES_START.md` as its entry point.
5. Use `docs/underwriting/underwriting-standard.md` before acquisition.
6. Use `docs/scaling/scaling-plan-standard.md` to build the post-close plan.
7. Follow `dashboard/README.md` to build and run the owner dashboard. Use `docs/deployment/azure-vm-test.md` for VM paths and environment loading.

Copy the root `employees.json` template to private `instance/employees.json` before adding people or approved contact scopes. Never populate the tracked template with real employee records.

## What Works Today

The version 2 evidence runtime and authenticated live dashboard are now implemented. Start with [the runtime guide](docs/deployment/evidence-runtime.md). They support private versioned document ingestion, deterministic financial calculations, source-linked reports and independent review, initiative measurements, and optional on-demand Notebook exchange. Direct accounting/banking OAuth connectors and unattended browser workers are not included. Use `BUSINESSOS_MODE=demo` for the original illustrative dashboard described below.

The original operating instructions, version 1 report validators, sample-data dashboard, and optional message-to-Hermes gateway remain available. Adding API keys alone does not install connectors. Hermes and each required external integration must be installed and configured separately.

The architecture describes the intended complete system. Only demo mode uses illustrative integration-health indicators; live mode displays persisted evidence and connection observations.

## Validation

```sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python scripts/validate_reports.py underwriting /private/path/report.json
python scripts/validate_reports.py scaling-plan /private/path/plan.json
```

Dashboard validation commands are in `dashboard/README.md`. GitHub Actions runs the Python tests, dashboard type check, production build, and packaged-server smoke test on pull requests. Report validation checks readiness and evidence references; it does not replace independent review of the evidence or grant approval to act.

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

Credentials are managed manually in the VM's ignored `.env`. A Vercel-style secrets page may be added later. The intended dashboard boundary is status only, never raw keys; current integration statuses are sample data.
