# Employee Agents

## Purpose

Employee agents collect operational signal from humans connected to the business.

The root `employees.json` file is the shared registry. Each employee agent folder stores that employee's profile and memory.

## Folder Pattern

```txt
agents/employees/<agent_id>/
  profile.md
  memory.md
```

## Root Registry

`employees.json` should contain:

- Name.
- Phone number.
- Telegram handle/user/chat ids.
- Email if useful.
- Role.
- Responsibilities.
- Agent id.
- Profile path.
- Memory path.
- Consent/approval scope.

## Memory Rule

Do not put sensitive personal notes in `employees.json`.

Put personal notes, relationship context, preferences, recurring friction, and historical memory in that employee's `memory.md` file.

## Pre-Acquisition Rule

In pre-acquisition mode, employee agents may only be started if the communication channel and scope are approved. They collect signal; they do not manage employees or promise changes.
