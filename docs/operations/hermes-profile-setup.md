# Hermes Profile Notes

This pod includes local profile blueprints under `hermes-profiles/`.

## Important Hermes Facts

- A Hermes profile is a separate Hermes home directory.
- Each profile has its own `config.yaml`, `.env`, `SOUL.md`, memories, sessions, skills, cron jobs, and gateway state.
- Profiles do not sandbox filesystem access.
- Hermes should set `terminal.cwd` explicitly so each profile starts in this pod folder on the current machine.
- Each gateway profile should use its own Telegram bot token if multiple gateways run in the same Telegram group.

## Hermes Creation Rule

Hermes can create profiles by itself. Do not require the owner to run profile creation commands manually.

When Hermes starts, it should:

- Read `agent-creation-protocol.md`.
- Read `hermes-profiles/`.
- Create the core profiles if missing.
- Create domain profiles as needed after understanding the business.
- Log each created profile in `audit/profile-creation-log.md`.
- Request missing credentials and permissions through `docs/operations/missing-tools-and-permissions.md` and `audit/access-requests.md`.

Configure Sendblue and Telegram credentials in the real Hermes profile `.env` or this pod `.env`, depending on how the integration is installed.
