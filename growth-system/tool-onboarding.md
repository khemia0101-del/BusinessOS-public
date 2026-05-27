# Tool Onboarding

## Purpose

When a new tool is needed, Hermes should request the minimum useful access and document how the tool will be used.

## Tool Request Format

```txt
Tool:
Needed for:
Minimum permission:
Data accessed:
Actions requested:
Risks:
Secrets needed:
Where secret should live:
Test plan:
Owner approval needed:
```

## Common Tools

- WordPress API.
- Zoho CRM API.
- SendGrid.
- Resend.
- Apify.
- InMailer / LinkedIn InMail.
- Telegram.
- Sendblue.
- Google Search Console.
- Google Analytics.
- Ads platforms.
- Calendar API.
- Email inbox.
- Review platforms.

## Secret Handling

Secrets should live in machine-local Hermes profile `.env` files or the pod `.env` when explicitly acceptable.

Never commit real secrets.

Never paste secrets into reports.
