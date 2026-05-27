# Edge Digital Twin

## Purpose

An Edge Digital Twin is a parallel AI-native workflow that runs beside the live business workflow before it is trusted with real traffic.

The twin is how Hermes proves a new automation is better before replacing a human/manual process.

## Core Rule

Do not rip out the cash cow. Fork the data stream, run the new system in parallel, compare performance, then migrate gradually only after evidence shows the twin is better.

## How The Twin Works

1. Map the live workflow.
2. Define the business objective.
3. Define baseline KPIs.
4. Fork or copy the input data stream.
5. Run the twin without external action in shadow mode.
6. Compare twin decisions against human/current decisions.
7. Review errors and edge cases.
8. Run a tiny approved live pilot.
9. Expand to a small batch.
10. Migrate more traffic only if promotion gates pass.
11. Keep rollback and human override available.

## Example: Lead Onboarding

Live workflow:

Website form -> Zoho/CRM notification -> support assistant calls later -> gathers data -> checks report -> decides can/cannot help -> books discovery call or rejects.

Twin workflow:

Website form copy -> automated enrichment/qualification -> report retrieval or guided upload -> eligibility decision -> draft rejection or booking action -> compare with support assistant decision.

Shadow mode output:

- The twin says qualified/not qualified.
- The human says qualified/not qualified.
- Differences are logged.
- No customer-facing action happens yet.

Pilot output:

- A small approved subset is routed automatically.
- Humans monitor every action.
- Stop conditions are active.

## Promotion Gates

A twin is ready to move toward live implementation only when all gates pass:

- Accuracy: twin matches or improves on human/current decisions.
- Speed: twin is materially faster.
- Safety: no serious compliance, customer, data, or operational failures.
- Coverage: twin handles the common cases and routes exceptions to humans.
- KPI lift: target KPI improves or is credibly expected to improve.
- Eval: independent evaluator passes it.
- Test: QA simulation/shadow/pilot passes it.
- Rollback: stop/revert path is clear.
- Owner approval: required for live external/customer-impacting migration.

## Suggested Evidence Thresholds

Use these defaults unless the initiative defines better ones:

| Risk Level | Minimum Shadow Runs | Minimum Pilot Runs | Promotion Standard |
| --- | ---: | ---: | --- |
| Low internal workflow | 10-20 | 5-10 | No critical errors, faster or same quality |
| Medium operational workflow | 25-50 | 10-25 | 90%+ agreement or better outcome, no critical errors |
| Customer-facing workflow | 50-100 | 25-50 | 95%+ agreement on routine cases, all exceptions routed safely |
| Compliance/data-sensitive workflow | 100+ | 25-50 with human monitoring | Compliance pass, human review of edge cases, no severe errors |
| Revenue-critical workflow | 100+ or one full business cycle | staged rollout | KPI lift or strong leading indicators, rollback proven |

## Time-Based Criteria

Some workflows need time, not just count.

Examples:

- Email campaigns need enough days for replies, bounces, complaints, and unsubscribes.
- Lead routing needs enough time to observe show rate and close rate.
- SEO needs weeks/months for indexing and rankings.
- Referral nurture needs enough time to measure reactivation.

Default:

- Fast workflows: at least 3-7 days of live observation.
- Sales/lead workflows: at least 2 full sales cycles or 25-50 pilot leads.
- Email/outreach: at least 7-14 days after send.
- SEO/content: at least 30-90 days for performance judgment.

## Stop Conditions

Stop the twin or pilot if:

- Compliance risk appears.
- Customers receive wrong or harmful communication.
- Sensitive data is mishandled.
- Error rate exceeds threshold.
- Human override queue backs up.
- Complaints increase.
- KPI degradation is severe.
- Tool/API behavior is unreliable.

## Decision Outcomes

- Keep shadowing.
- Revise twin.
- Run pilot.
- Expand pilot.
- Ship live.
- Reject and archive.
- Escalate for human/legal/accounting/HR review.
