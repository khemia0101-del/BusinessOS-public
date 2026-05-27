# System Structure

## Mental Model

The Google Drive data room stores source documents.

The Business Pod stores operating memory and execution control.

Hermes uses this pod to understand the business, coordinate agents, propose work, request approval, execute approved tickets, and report outcomes.

## Default Flow

```mermaid
flowchart TB
    START["Business Acquired"] --> ROOM["Create Google Drive Data Room"]
    ROOM --> INGEST["Researcher Ingests Data"]
    INGEST --> QUESTIONS["Targeted Questions to Owner / Employees"]
    QUESTIONS --> UNDERWRITE["Underwriting + Baseline Report"]
    UNDERWRITE --> BOTTLENECKS["Find Bottlenecks"]
    BOTTLENECKS --> CGO["CGO Builds Scaling Plan"]
    CGO --> TICKETS["Convert Plan into Tickets"]
    TICKETS --> REVIEW["You + Partner Review"]
    REVIEW --> A["Approve"]
    REVIEW --> P["Postpone"]
    REVIEW --> R["Reject"]
    A --> ACCESS["Orchestrator Requests Needed Access"]
    ACCESS --> BUILD["Executor Builds / Changes / Automates"]
    BUILD --> COMPLIANCE["Compliance Review if Needed"]
    COMPLIANCE --> DEPLOY["Deploy"]
    DEPLOY --> MEASURE["Measure Change-Specific KPI"]
    MEASURE --> REPORT["Weekly / Bi-weekly Report"]
    REPORT --> TICKETS
    P --> BACKLOG["Backlog"]
    R --> ARCHIVE["Archived with Reason"]
```

## Employee Signal Flow

```mermaid
flowchart TB
    EMP1["Employee A"] --> EA1["Employee A Agent"]
    EMP2["Employee B"] --> EA2["Employee B Agent"]
    EMP3["Employee C"] --> EA3["Employee C Agent"]
    EMP4["Employee D"] --> EA4["Employee D Agent"]
    EA1 --> IM["iMessage via Sendblue"]
    EA2 --> IM
    EA3 --> IM
    EA4 --> IM
    IM --> INBOX["Employee Feedback Inbox"]
    INBOX --> CLASSIFY["Classify Feedback"]
    CLASSIFY --> BUG["Bug / Broken Process"]
    CLASSIFY --> IDEA["Suggestion"]
    CLASSIFY --> FRICTION["Employee Friction"]
    CLASSIFY --> CUSTOMER["Customer Issue"]
    CLASSIFY --> RISK["Risk / Compliance Issue"]
    BUG --> SCORE["Score Impact / Difficulty / Risk / Cost"]
    IDEA --> SCORE
    FRICTION --> SCORE
    CUSTOMER --> SCORE
    RISK --> SCORE
    SCORE --> BIWEEKLY["Bi-weekly Strategic Change Review"]
    BIWEEKLY --> APPROVE["Approve"]
    BIWEEKLY --> POSTPONE["Postpone"]
    BIWEEKLY --> REJECT["Reject"]
    APPROVE --> ORCH["Orchestrator"]
    POSTPONE --> BACKLOG["Backlog"]
    REJECT --> ARCHIVE["Archived with Reason"]
    ORCH --> NEEDS["Request API Keys / Access / Info"]
    NEEDS --> YOU["You + Partner"]
```

## Strategic Change Review Output

The bi-weekly output is a Strategic Change Review, not just an employee feedback queue.

It should include:

1. Employee feedback summary.
2. Customer friction summary.
3. Operational bottlenecks.
4. Growth bottlenecks.
5. Marketing opportunities.
6. Sales opportunities.
7. SEO opportunities.
8. Outreach opportunities.
9. Automation opportunities.
10. Fundamental changes.
11. Non-fundamental changes.
12. Agent/profile creation proposals.
13. Approved/postponed/rejected queue.
14. KPI movement since last review.
15. What the orchestrator needs from you.
16. Operational inefficiency radar findings.
17. Automation/system-building opportunities.
18. Documented anomalies and recurring patterns.
19. Quality/eval status for active initiatives.
20. Tool/API/permission blockers.

## Fundamental Changes

- Change pricing.
- Change offer.
- Change target customer.
- Change sales process.
- Add or remove service line.
- Hire, fire, or restructure role.
- Change core workflow.
- Replace core software.
- Change acquisition channel strategy.

## Non-Fundamental Changes

- Build dashboard.
- Improve CRM flow.
- Add email sequence.
- Add SEO pages.
- Improve intake form.
- Add reporting.
- Automate reminders.
- Clean database.
- Create SOP.
- Improve employee utility.

## Operating Systems

Hermes should use:

- `growth-system/` to detect and execute growth/automation initiatives.
- `operations-system/` to find waste, inefficiencies, and automatable workflows.
- `memory-system/` to document communications and signals.
- `quality-system/` to evaluate, test, simulate, approve, ship, and monitor changes.
- `intelligence-stack/` to run Edge Digital Twins, organizational drag scoring, sensing, and learning loops.
