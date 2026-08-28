# Initiative Lifecycle

BusinessOS uses one lifecycle for a CRM implementation, an ad experiment, an internal tool, a workflow change, or any other improvement.

## States

1. **Found:** a source or observed pattern identifies a problem or opportunity.
2. **Researched:** the business case, options, current pricing, risks, and evidence are assembled.
3. **Proposed:** the owner can see the cost, expected impact, proof method, and exact decision required.
4. **Approved:** decision and scope are recorded. Required credentials are added manually to `.env` by the owner.
5. **Building:** an executor creates the change in an isolated branch or environment.
6. **Testing:** independent review, functional tests, and compliance review run as required.
7. **Ready:** evidence shows the promotion gate passed and the release is waiting for final material-change approval when required.
8. **Live:** release is staged with monitoring and rollback available.
9. **Measuring:** actual results are compared with the baseline and projection.
10. **Closed or stopped:** the result and lesson are recorded; unsuccessful work is rolled back or retired.

## Proof Choice

- Use a historical backtest when existing business activity can answer the question.
- Use simulation when inputs can be bounded but replay is incomplete.
- Use shadow mode when a new workflow should be compared with the live workflow without taking action.
- Use a small pilot when real behavior is necessary.
- Launch directly only when the change is low-risk, reversible, and already supported.

## Approval Boundary

Read-only research, internal drafts, local prototypes, and simulations may proceed automatically. Approval is required before spend, new access, external messages, production writes, customer or employee impact, legal or compliance exposure, or a material operating change.

Approval never transfers ownership of a raw secret to an agent. For the current version, the owner adds credentials to `.env`; the system receives only the permission and configuration status it needs.

## Required Record

Every initiative keeps:

- Source problem and evidence
- Business case and rejected alternatives
- Owner, cost, dependencies, and timeline
- Approval and access record
- Build and review record
- Test data and promotion result
- Launch, monitoring, stop condition, and rollback
- Actual result versus projection
- Lesson returned to BusinessOS memory
