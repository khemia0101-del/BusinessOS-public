# Employee Agents

## Purpose

Employee agents collect operational signal from humans connected to the business.

Private `instance/employees.json` is the shared registry, copied from the empty root template. Keep real profiles and personal memory in private instance storage, not in tracked template files.

## Folder Pattern

```txt
instance/runtime/employees/<agent_id>/
  profile.md
  memory.md
```

## Private Registry

`instance/employees.json` should contain:

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

Do not put sensitive personal notes in the registry or any tracked file.

Put personal notes, relationship context, preferences, recurring friction, and historical memory in that employee's `memory.md` file.

## Pre-Acquisition Rule

In pre-acquisition mode, employee agents may only be started if the communication channel and scope are approved. They collect signal; they do not manage employees or promise changes.
