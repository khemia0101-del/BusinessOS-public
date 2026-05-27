# Communication Plan

## Primary Channels

- Telegram for owner/partner communication, approval prompts, reports, and status updates.
- Sendblue for iMessage/SMS workflows, especially employee feedback and lightweight operational check-ins.

## Telegram Setup Requirements

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_ALLOWED_USERS`
- `TELEGRAM_OWNER_CHAT_ID`
- `TELEGRAM_PARTNER_CHAT_ID`

Hermes should restrict Telegram access to explicit allowed user IDs.

## Sendblue Setup Requirements

- `SENDBLUE_API_KEY`
- `SENDBLUE_PHONE_NUMBER`
- `SENDBLUE_OWNER_THREAD`
- `SENDBLUE_PARTNER_THREAD`

## Communication Rules

- Internal status updates can be sent after the channel is configured.
- External customer, employee, lead, vendor, or partner messaging requires approval unless the message is only a pre-approved operational check-in template.
- Employee agents may collect feedback, but may not promise changes or give HR/legal advice.
- All approval decisions received through messaging must be logged in `audit/decisions.md`.
- Meaningful communications should be summarized in `memory-system/` with date, channel, participants, follow-up, tags, and source link when available.
