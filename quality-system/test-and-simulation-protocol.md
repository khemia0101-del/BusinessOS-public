# Test And Simulation Protocol

## Purpose

Verify behavior before live execution.

## Test Modes

- Unit test: small logic checks.
- Integration test: tool/API interaction against safe environment.
- Dry run: no external action.
- Fake-data simulation.
- Shadow mode: compare against current human process.
- Tiny pilot: approved live subset.

## Required For External Automations

Before live use:

- Use fake/test data.
- Use dry-run mode.
- Log actions that would have happened.
- Confirm rate limits.
- Confirm error handling.
- Confirm stop condition.
- Confirm rollback.

## Output

```txt
Tested item:
Test mode:
Data used:
Expected result:
Actual result:
Errors:
Decision:
Next step:
```
