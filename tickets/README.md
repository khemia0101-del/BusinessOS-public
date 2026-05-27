# Ticket System

Do not create tickets for every task.

Use workstreams for autonomous read-only/internal work. Use tickets only for approval gates, missing permissions, external writes, deployments, spend, delegated execution, and rollback-tracked changes.

## States

- `inbox`
- `proposed`
- `approved`
- `postponed`
- `rejected`
- `in-progress`
- `deployed`
- `measuring`
- `closed`

## Ticket Naming

Use:

`YYYY-MM-DD-short-description.md`

## Required Fields

- Title.
- Status.
- Owner agent.
- Source.
- Objective.
- Impact.
- Difficulty.
- Risk.
- Cost.
- Approval required.
- Definition of done.
- Measurement plan.
- Rollback note.
