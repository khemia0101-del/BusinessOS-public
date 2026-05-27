# Setup Instructions

## 1. Confirm External Anchors

Verify these values in `.env`:

- `GOOGLE_DRIVE_DATA_ROOM_URL`
- `GITHUB_REPO_URL`
- `BUSINESS_NAME`

## 2. Give Hermes Context

When starting Hermes in this folder, provide:

- This folder path.
- Google Drive data-room URL.
- Business owner / partner approval rule.
- Any current work priority.

Suggested start prompt:

```txt
You are Hermes, the orchestrator for this Business Pod. Read HERMES_START.md first, then README.md, pod-manifest.md, business-context.md, data-room-map.md, local-structure-rules.md, system-structure.md, autonomy-policy.md, growth-system/, operations-system/, memory-system/, quality-system/, and agents/orchestrator/*.md. Treat Google Drive as the data room and this folder as the operating layer. Read-only work is automatically approved. Do not execute material external changes without an approved ticket or logged approval.
```

## 3. First Run

Hermes should:

1. Read the core files.
2. Confirm data-room access.
3. Start read-only Drive indexing immediately.
4. Create or prepare core profiles from `hermes-profiles/`.
5. Record missing tools and permissions.
6. Create missing-document requests only when they materially block underwriting, scaling, compliance, or execution.
7. Produce working notes until evidence saturation is reached.
8. Produce final underwriting only after evidence saturation.
9. Produce final scaling plan only after final underwriting and full business understanding.

## 4. Access

Hermes must request access before using:

- Google Drive write operations.
- GitHub write operations.
- CRM.
- Sendblue.
- Ads platforms.
- Search Console.
- Analytics.
- Email sending.
- Billing or payment systems.
- Customer databases.

Read-only local documentation and read-only Drive analysis do not require approval.

## 5. Reporting Cadence

- Weekly: execution status and KPI movement.
- Bi-weekly: Strategic Change Review.
- Monthly: business performance summary and priority reset.
