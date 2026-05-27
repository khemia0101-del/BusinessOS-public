# Quality System

## Purpose

Enforce a zero-trust hierarchy before shipping code, automations, campaigns, workflows, CRM changes, customer-facing content, or external actions.

One LLM or one profile cannot build and ship directly.

## Default Hierarchy

```txt
Builder creates
-> Reviewer evaluates
-> Tester simulates
-> Compliance reviews if needed
-> Orchestrator decides ship/no-ship
-> Owner/partner approval if material/external/high-risk
-> Monitor after launch
```

## Core Rule

No agent approves its own work.
