# Hermes Profile Blueprints

These folders define the profile distribution shape Hermes can use when it decides to create profiles.

Hermes profiles are not the same as project folders. A Hermes profile is a separate Hermes home directory with its own `config.yaml`, `.env`, `SOUL.md`, memories, sessions, skills, cron jobs, and gateway state.

Hermes should create profiles on its own when the operating context calls for them. This folder only provides the desired profile shape and soul/config defaults.

## Core Profiles

- `business-orchestrator`
- `business-researcher`
- `business-cgo`
- `business-compliance`
- `business-evaluator`
- `business-qa-tester`

## Distribution Shape

Each blueprint follows the Hermes distribution layout:

```txt
profile-name/
  distribution.yaml
  SOUL.md
  config.yaml
  skills/
  cron/
  mcp.json
```

Secrets, sessions, memories, and live gateway state belong in the real Hermes profile home on the machine, not in this portable pod.

For Telegram, use one bot token per profile if multiple profile gateways run in the same group.
