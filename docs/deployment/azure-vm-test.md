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

- Node.js 22 for the Next.js dashboard (minimum supported: 20.9)
- Python 3.12 or newer for optional integration gateways and report validation
- Caddy or Nginx for HTTPS and routing
- systemd or containers for process supervision
- Encrypted backup of private instance data and audit records
- Optional private admin network such as Tailscale

The dashboard is built with `output: "standalone"` so its production artifact can run without the repository or development dependencies.

## Suggested Paths

```text
/opt/businessos/core              generic checked-out repository
/opt/businessos/core/instance     ignored private configuration and roster
/opt/businessos/core/.env         secrets, readable only by the service user
/var/lib/businessos               indexes, records, reports, and working state
/var/lib/businessos/communications metadata-only gateway logs
```

## Deployment Steps

1. Provision a dedicated VM and service account.
2. Clone the approved BusinessOS release into `/opt/businessos/core`.
3. Copy `instance/business.example.yaml` to `/opt/businessos/core/instance/business.yaml` and root `employees.json` to `/opt/businessos/core/instance/employees.json`. Populate only these private copies.
4. Copy `.env.example` to `/opt/businessos/core/.env`. Add credentials manually, set `BUSINESS_STAGE`, and restrict the file to the service user (mode `0600`).
5. Install, build, and smoke-test `dashboard/` using `dashboard/README.md`.
6. Configure the reverse proxy and TLS.
7. Run the dashboard and optional workers under separate restricted services.
8. Verify `/api/health`, backup, log redaction, and restart behavior.
9. Connect sources read-only first.
10. Record the instance and release in the deployment audit.

## Process Configuration

Neither the Python gateway nor a dashboard launched from `dashboard/` automatically loads the root `.env`. Configure the service manager to inject it. Use the same stage setting for Hermes, the gateway, and the dashboard. Never dump the full environment into an agent session or log.

Example dashboard systemd service, after creating the `businessos` service account and building the dashboard:

```ini
[Unit]
Description=BusinessOS dashboard
After=network.target

[Service]
User=businessos
Group=businessos
WorkingDirectory=/opt/businessos/core/dashboard
EnvironmentFile=/opt/businessos/core/.env
Environment=NODE_ENV=production
Environment=HOSTNAME=127.0.0.1
Environment=PORT=3000
ExecStart=/usr/bin/node /opt/businessos/core/dashboard/.next/standalone/server.js
Restart=on-failure
UMask=0077
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

Adjust the Node executable to its installed absolute path. The gateway service uses `WorkingDirectory=/opt/businessos/core`, the same `EnvironmentFile`, and `ExecStart=/usr/bin/python3 /opt/businessos/core/services/businessos_web.py`. Give it access only to its private roster, state directory, and the intended Hermes profile. Configure Hermes's service with the same repository working directory and environment file; verify its installed CLI and profile before enabling workers.

When copying only the standalone dashboard artifact, keep the private environment file outside it and update the service's paths accordingly. Never bundle `.env`, the roster, or business evidence with the browser assets. The current dashboard needs no integration credentials; before real integrations are added, split service environments so each process receives only its required keys.

## Existing-VM Migration

This release is not a drop-in replacement for the old CRR service. The legacy `/webhooks/sendblue` endpoint, public status page, and root employee-roster path have changed. Do not replace a live webhook service until a trusted provider adapter is configured and tested against `services/README.md`. Keep the previous release available for rollback; this repository merge does not deploy or migrate a VM.

If an old installation uses `business.stage`, an employee-registry stage, or `post_acquisition`, have the owner confirm the current authority and migrate to the single `BUSINESS_STAGE` setting. Until then, stay read-only.

## Security Checks

- `.env`, `instance/business.yaml`, and `instance/employees.json` are not committed or served.
- Services run as non-root users with only the permissions they need.
- Webhooks authenticate before payloads are stored or routed.
- Logs redact authorization headers, tokens, customer payloads, and raw secrets.
- Integration permissions start read-only and expand only for an approved initiative.
- The dashboard sits behind authentication before any private business data is loaded.
- Production changes have a release record and rollback path.

## Health

The dashboard exposes `GET /api/health`. Optional integration gateways expose their own health endpoint. Health responses may include instance ID, stage, service version, and sync timestamps, but never credentials or business records.
