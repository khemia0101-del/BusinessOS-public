# Business OS Pod

This folder is the local agent operating layer for Hermes and related agents.

The folder is not the data room. The Google Drive is the data room.

This folder tells Hermes how to use the data room, reason about the business, document work, request approvals, create tickets, coordinate agents, and execute approved changes.

## Start Here

1. Read `pod-manifest.md`.
2. Read `business-context.md`.
3. Read `data-room-map.md`.
4. Read `acquisition-mode.md`.
5. Read `employees.json`.
6. Read `local-structure-rules.md`.
7. Read `autonomy-policy.md`.
8. Read `growth-system/README.md`.
9. Read `operations-system/README.md`.
10. Read `memory-system/README.md`.
11. Read `quality-system/README.md`.
12. Read `intelligence-stack/README.md`.
13. Read the relevant agent profile under `agents/`.
14. Use workstreams for autonomous read-only work.
15. Create tickets only for approval gates, missing permissions, external writes, deployments, spend, delegated execution, and rollback-tracked changes.
16. Log decisions, access requests, deployed changes, and rollback notes under `audit/`.

## Core Model

- Researcher understands the business and indexes evidence from the Google Drive data room.
- CGO finds growth paths across offer, channels, sales, marketing, SEO, ads, outreach, and customer friction.
- Orchestrator turns research and strategy into approved, documented execution.
- Compliance reviews sensitive, legal, financial, customer-impacting, and regulated changes.
- Employee agents feed operational signal.
- Root `employees.json` maps humans to employee agents and communication handles.
- Temporary executors build approved tasks.
- New permanent agents are proposed when a function becomes recurring.
- Read-only/planning profiles may be created automatically and logged.
- Growth-system detects and executes proactive or owner-directed growth/automation initiatives.
- Operations-system detects inefficiencies, waste, and automatable workflows.
- Memory-system documents communications and business signals for anomaly/pattern detection.
- Quality-system enforces zero-trust evals before anything ships.
- Intelligence-stack defines Edge Digital Twin testing, organizational drag scoring, sensing, and learning loops.

## External Anchors

- Google Drive Data Room: https://drive.google.com/drive/folders/1sYx2xvPTceGDpSgGCwIhtWNoE-uaCWIJ
- GitHub Repository: https://github.com/khemia0101-del/YBS
- GitHub Default Branch Observed: `main`
- GitHub HEAD Observed: `e9f2e54ce58107a6dfd1e034ddf09db6bea44f7a`

## Non-Negotiables

- Do not move, rename, delete, or overwrite Google Drive files without explicit approval.
- Read-only work is automatically approved.
- Do not execute material business changes without an approved ticket or logged approval.
- Every extracted insight must cite a source file, folder, ticket, or conversation.
- Every deployed change needs a rollback note.
- Profile creation is allowed for read-only/planning roles. Write, spend, deployment, customer messaging, HR, legal, compliance, and finance-sensitive authority requires approval.
- In pre-acquisition mode, assume limited company authority and read-only access except approved employee-agent communication scope.
- Every meaningful communication/signal should be documented.
- Code, automations, campaigns, workflows, and external changes require zero-trust eval before shipping.
- Keep local files portable. Use environment variables and URLs instead of machine-specific secrets.
