# Ship Decision Protocol

## Purpose

Make final launch decisions explicit.

## Ship Decision Inputs

- Builder summary.
- Eval result.
- Test/simulation result.
- Compliance result if needed.
- Pilot result if available.
- Rollback plan.
- KPI plan.
- Approval record.

## Decisions

- Ship.
- Ship to pilot.
- Hold.
- Revise.
- Reject.
- Needs human/legal/accounting/HR review.

## Ship Log

Every shipped change should be recorded in `audit/deployed-changes.md`.

Every shipped change should have a rollback or stop note in `audit/rollback-notes.md`.
