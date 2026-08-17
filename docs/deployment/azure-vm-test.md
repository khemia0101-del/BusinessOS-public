# Single-Business VM Deployment

## Boundary

Deploy one BusinessOS instance per business. Each VM receives its own private `instance/business.yaml`, `.env`, runtime data, integrations, audit trail, and dashboard. Do not connect one instance to another company's sources.

## Recommended Starting VM

```text
Ubuntu 24.04 LTS
2 vCPU
4-8 GB RAM
Premium SSD
Inbound: 22 through a restricted admin path; 80/443 through the proxy
```

Increase memory for browser automation, local models, or concurrent data processing.

## Runtime

- Node.js 20 or newer for the Next.js dashboard
- Python 3 for optional integration gateways and workers
- Caddy or Nginx for HTTPS and routing
- systemd or containers for process supervision
- Encrypted backup of private instance data and audit records
- Optional private admin network such as Tailscale

The dashboard is built with `output: "standalone"` so its production artifact can run without the repository or development dependencies.

## Suggested Paths

```text
/opt/businessos/core              generic checked-out repository
/opt/businessos/instance          private configuration and runtime data
/etc/businessos/businessos.env    secrets, readable only by the service user
/var/lib/businessos               indexes, records, reports, and working state
/var/log/businessos               redacted operational logs
```

## Deployment Steps

1. Provision a dedicated VM and service account.
2. Clone the approved BusinessOS release into `/opt/businessos/core`.
3. Create the private instance configuration from `instance/business.example.yaml`.
4. Add credentials manually to the protected environment file.
5. Install and build `dashboard/`.
6. Configure the reverse proxy and TLS.
7. Run the dashboard and optional workers under separate restricted services.
8. Verify `/api/health`, backup, log redaction, and restart behavior.
9. Connect sources read-only first.
10. Record the instance and release in the deployment audit.

## Security Checks

- `.env` and `instance/business.yaml` are not committed or served.
- Services run as non-root users with only the permissions they need.
- Webhooks authenticate before payloads are stored or routed.
- Logs redact authorization headers, tokens, customer payloads, and raw secrets.
- Integration permissions start read-only and expand only for an approved initiative.
- The dashboard sits behind authentication before any private business data is loaded.
- Production changes have a release record and rollback path.

## Health

The dashboard exposes `GET /api/health`. Optional integration gateways expose their own health endpoint. Health responses may include instance ID, stage, service version, and sync timestamps, but never credentials or business records.
