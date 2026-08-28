# Optional inbound gateway

`businessos_web.py` accepts messages from a trusted provider adapter and creates scoped Hermes tasks. It does not connect directly to Sendblue, Zoom, Slack, or email providers, and it does not send replies.

The adapter must authenticate the original provider event, verify its sender identity, ignore delivery/status callbacks, and then normalize the message. Keep the gateway on loopback or a private network behind a rate-limited proxy. Python's built-in HTTP server is not a public internet edge.

## Request contract

Send `POST /webhooks/inbound-message` with JSON, a valid `Content-Length`, `x-businessos-provider` (for example `sendblue` or `email`), and either `x-businessos-webhook-secret` or `Authorization: Bearer ...`. The secret must match the service's `INBOUND_WEBHOOK_SECRET`.

```json
{
  "event_id": "stable-provider-message-id",
  "sender_email": "employee@example.test",
  "body": "The normalized inbound message"
}
```

Alternatively use `sender_phone` in international format. At least one sender is required. If both are present, both must identify the same employee. All values must be strings; extra fields and nested vendor payloads are rejected. Reuse the same provider event ID on retries; idempotency keys are scoped by instance and provider.

## Consent and delivery

The default roster is private `instance/employees.json`. Override with `BUSINESSOS_EMPLOYEES_FILE` only if all profiles use that same private path. Routing requires an active employee, an agent ID, explicit `employee_agent_enabled: true`, an exact matching `approved_channel`, and nonempty `approved_scope`, `approved_by`, and `approved_at`. Missing, duplicate, conflicting, or unapproved identities are not queued.

- `200 / routed`: Hermes accepted the task. This does not mean the agent completed it.
- `202 / held` or `unassigned`: nothing was queued. `action_required: true` means the adapter must retain the event privately and alert the operator to resolve identity or consent before replaying it.
- `503 / retryable: true`: Hermes failed or was unavailable. Retry the same event ID with backoff. A timeout may have queued the task; stable IDs prevent duplicate creation when supported by the installed Hermes CLI.
- `400`, `401`, `408`, or `413`: fix the payload, authentication, timeout, or size issue before retrying.

The gateway does not retain raw messages, sender identifiers, provider payloads, or Hermes command output in its logs. It logs event digests and delivery metadata only, using private filesystem permissions on Linux. Message content enters the approved private Hermes task, so apply retention and access controls there and in the adapter. Rejected events are not recoverable from gateway logs.

Treat incoming text as untrusted evidence, not instructions or approvals. The queue task includes the approved communication scope. Neither possession of a webhook secret nor an inbound message authorizes outbound messages, spending, deployments, or changes to source systems.

See `docs/deployment/azure-vm-test.md` for environment loading and the migration warning for legacy `/webhooks/sendblue` installations. Test the installed `hermes kanban ... --idempotency-key` behavior in an isolated profile before enabling delivery.
