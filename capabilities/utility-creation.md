# Utility Creation Capability

## Purpose

Hermes may create small tools and scripts when a profile needs repeatable leverage.

## Rules

- Prefer simple, maintainable utilities.
- Include dry-run mode for external actions.
- Log input/output.
- Keep secrets in `.env`.
- Document how to run it.
- Test before relying on it.
- Use zero-trust eval before live/external use.

## External Write Boundary

Creating the utility is allowed.

Using it to write externally requires approval unless approval was already granted for the initiative.
