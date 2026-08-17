# Parallel Workflow Proof

## Purpose

A parallel workflow proof tests a proposed process against real business activity before it replaces the live process. Use it for high-impact or uncertain changes where a backtest or simple simulation is not enough.

## Core Rule

Copy the relevant input stream, run the proposed workflow without external action, compare it with the current workflow, then promote gradually only when the evidence passes the initiative's gate.

## Flow

1. Map the live workflow and its exceptions.
2. Define the business objective and baseline.
3. Choose historical replay, simulation, shadow mode, or a pilot.
4. Copy only the data needed for the test.
5. Record proposed and actual decisions, time, quality, and outcome.
6. Review disagreements and harmful edge cases.
7. Pass independent evaluation and compliance review when required.
8. Use a small approved live pilot if behavior must be observed.
9. Expand only after the promotion gate passes.
10. Keep human override, stop conditions, and rollback available.

## Example: Lead Intake

The live process may route an inquiry through inboxes, spreadsheets, a CRM, or a dispatcher. The proposed process can receive a copy of the same inquiry, recommend ownership and the next step, then compare its output with what the team actually did. No customer-facing action occurs in shadow mode.

## Promotion Gates

- Accuracy or business outcome meets the defined threshold.
- The process is materially faster or removes meaningful work.
- Common cases are covered and exceptions route safely.
- No serious customer, employee, compliance, security, or data failure occurs.
- The target KPI improves or the leading evidence is strong enough for the planned pilot.
- Independent review and required tests pass.
- The rollback path has been exercised.
- Required owner approval is recorded before live impact.

## Sample Thresholds

These are starting points, not universal rules:

| Risk                          |                   Shadow evidence | Pilot evidence | Promotion standard                                    |
| ----------------------------- | --------------------------------: | -------------: | ----------------------------------------------------- |
| Low internal workflow         |                       10-20 cases |     5-10 cases | No critical errors; same or better quality            |
| Medium operating workflow     |                       25-50 cases |    10-25 cases | 90%+ agreement or a better measured outcome           |
| Customer-facing workflow      |                      50-100 cases |    25-50 cases | Safe exception routing and no severe errors           |
| Sensitive or revenue-critical | One representative business cycle |         Staged | Independent review, proven rollback, and KPI evidence |

Time-based outcomes still require time. Sales changes should normally cover at least two representative sales cycles; campaigns must allow time for responses and complaints; content and search changes may require months.

## Outcomes

- Continue collecting evidence
- Revise the proposed workflow
- Move to a small pilot
- Expand the pilot
- Approve staged release
- Stop and archive the result
- Escalate for human, legal, accounting, HR, security, or compliance review
