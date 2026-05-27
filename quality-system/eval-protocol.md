# Eval Protocol

## Purpose

Evaluate the quality, safety, and business fit of work before it ships.

## Eval Roles

- Builder / executor.
- Code reviewer.
- Automation evaluator.
- QA tester.
- Compliance reviewer.
- Orchestrator.
- Owner/partner when required.

## Eval Checklist

- Does it solve the stated problem?
- Are assumptions documented?
- Are sources linked?
- Are edge cases handled?
- Are errors logged?
- Are permissions minimal?
- Are sensitive data paths safe?
- Is there a dry-run mode?
- Is there a rollback/stop plan?
- Are KPIs defined?
- Does it comply with approval boundaries?

## Output

```txt
Eval decision: pass / pass with changes / fail / needs human review
Reviewed item:
Reviewer:
Findings:
Required changes:
Residual risks:
Ship recommendation:
```
