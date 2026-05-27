# Automation Factory

## Purpose

Allow Hermes to create internal systems, utilities, scripts, and workflows when repeated work should become machinery.

## When To Build Automation

Build or propose automation when:

- The same task repeats.
- Manual work delays revenue.
- Manual work creates errors.
- A workflow depends on employee availability but does not require human judgment.
- Data is copied between systems.
- A lead/customer waits for a routine next step.
- A report is built manually.
- A campaign needs repeatable execution.
- A profile needs a reusable utility to operate at scale.

## Utility Creation Rule

Hermes may create utilities/scripts for internal/read-only or local processing without approval.

Approval is required before a utility:

- Sends external messages.
- Writes to CRM, Drive, website, social, ads, payment, HR, or production systems.
- Publishes content.
- Spends money.
- Touches customer sensitive data live.
- Deletes or mutates source data.

## Build Standard

Each utility needs:

- Purpose.
- Inputs.
- Outputs.
- Required environment variables.
- Dry-run mode.
- Logging.
- Error handling.
- Rate limits.
- Test data.
- Rollback/stop plan when applicable.
- Owner profile.

## Batch And Pilot Standard

External actions should launch in controlled batches:

1. Dry run.
2. Fake/test data.
3. Shadow mode.
4. Tiny pilot.
5. Small batch.
6. Scaled batch.
7. Continuous monitoring.

## Examples

- WordPress article uploader.
- Keyword clustering utility.
- Referral partner segmentation tool.
- Email sequence sender.
- CRM deduper.
- Lead qualification router.
- Calendar scheduler.
- Social post scheduler.
- Review monitoring tool.
- KPI report generator.
