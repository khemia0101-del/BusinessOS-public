# Workflow Automation Protocol

## Purpose

Turn inefficient workflows into controlled automations.

## Stages

1. Map current flow.
2. Identify human-only judgment points.
3. Identify removable steps.
4. Identify automation candidates.
5. Define future flow.
6. Define data inputs/outputs.
7. Define system integrations.
8. Define failure modes.
9. Build dry-run version.
10. Shadow against human process.
11. Compare decisions/results.
12. Run small live pilot.
13. Scale after eval and approval.
14. Monitor continuously.

For high-impact workflows, follow `intelligence-stack/edge-digital-twin.md` before live migration.

## Human Exception Model

Automations should route exceptions to humans. They should not force every edge case through brittle rules.

Examples of exceptions:

- Missing data.
- Conflicting data.
- Compliance uncertainty.
- High-value lead.
- Angry customer.
- Legal/HR/financial issue.
- System error.

## Required Documentation

- Current workflow.
- Future workflow.
- Decision rules.
- Integrations.
- Permissions.
- Data handled.
- Eval plan.
- Shadow-mode result.
- KPI impact.
- Rollback/stop plan.
