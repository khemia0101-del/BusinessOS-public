# Zero-Trust Policy

## Rule

Do not trust one agent, one model, one script, or one successful run enough to ship directly.

## Applies To

- Code.
- Automations.
- CRM changes.
- Website changes.
- WordPress publishing.
- Ads.
- Email/SMS campaigns.
- Social posts.
- Outreach.
- Lead routing.
- Customer-facing messaging.
- Data transformations.
- Reports used for decisions.

## Requirements

- Builder self-check.
- Independent review.
- Test or simulation.
- Risk review.
- Compliance review when sensitive.
- Ship/no-ship decision.
- Rollback/stop plan.
- Monitoring.

## Forbidden

- Builder ships its own work without review.
- Untested automation touches real customers.
- Campaign sends at scale without pilot.
- Code deploys without review/test.
- CRM/customer-data automation runs live without simulation.
- External action runs without stop condition.
