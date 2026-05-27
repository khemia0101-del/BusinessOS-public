# Local Structure Rules

## What Lives Here

This folder stores:

- Agent instructions.
- Business context.
- Google Drive data-room map.
- Local working docs.
- Tickets.
- Workstreams.
- Audit logs.
- Reports.
- Agent creation proposals.
- Execution history.

## What Does Not Live Here

This folder should not become a copy of the data room.

Do not bulk-download financials, tax returns, HR files, customer files, contracts, or source diligence documents into this folder unless there is a specific approved reason.

## Portability Rules

- Use relative links for local files.
- Use external URLs for Google Drive and GitHub.
- Keep secrets out of committed files.
- Keep `.env.example` as the template.
- Treat `.env` as local runtime config only.
- Use plain Markdown for durable context.

## Ticket Rules

Do not create tickets for everything.

Use workstreams for autonomous read-only and internal documentation work.

Use tickets only when a decision, permission, external write, spend, deployment, business change, or delegated executor needs tracking.

Ticket states:

`inbox -> proposed -> approved/postponed/rejected -> in-progress -> deployed -> measuring -> closed`

No skipped status unless the orchestrator records the reason in the ticket and `audit/decisions.md`.

## Workstream Rules

Workstreams are for autonomous work that Hermes can perform without babysitting:

- Reading.
- Indexing.
- Summarizing.
- Asking source-grounded questions.
- Drafting internal docs.
- Creating read-only profiles.
- Mapping systems.
- Preparing underwriting.
- Preparing growth analysis.

Use `workstreams/active/` while running and `workstreams/completed/` when done.

Escalate a workstream into a ticket only when it requires approval, permissions, external execution, or a tracked business decision.

## Audit Rules

Update the audit folder when:

- A decision is made.
- Access is requested.
- A profile is proposed or created.
- A change is deployed.
- A rollback note is created.
- A Drive source is modified, moved, renamed, shared, or deleted.

## Google Drive Rules

- Read and index first.
- Read-only Google Drive access is automatically approved.
- Ask before changing.
- Link back to source files.
- Track missing documents.
- Do not treat local summaries as authoritative when the Drive source is available.
