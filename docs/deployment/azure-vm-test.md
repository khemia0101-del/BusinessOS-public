# Azure VM Test Deployment

## Current Local CLI Status

Observed on 2026-05-27:

- Azure CLI is installed and logged in.
- Logged-in user: `Eli@Queenventures.onmicrosoft.com`
- CLI shows a tenant-level account.
- No usable subscription is visible in `az account list`.
- `az group list` fails with `SubscriptionNotFound`.

Conclusion: this login cannot deploy an Azure VM yet. A subscription must be attached or selected.

## Permission Check Commands

```powershell
az account list --output table
az account show --output json
az group list --output table
```

If no subscription appears, fix billing/subscription access first.

If a subscription appears, select it:

```powershell
az account set --subscription "<subscription id or name>"
```

Then verify VM permissions:

```powershell
az provider show --namespace Microsoft.Compute --query "registrationState" --output tsv
az provider show --namespace Microsoft.Network --query "registrationState" --output tsv
az provider show --namespace Microsoft.Storage --query "registrationState" --output tsv
az role assignment list --assignee "$(az ad signed-in-user show --query id -o tsv)" --all --output table
```

Needed permissions:

- Create resource group or use an existing one.
- Create VM.
- Create NIC/public IP/network security group.
- Create disk/storage resources.
- Assign or use SSH key.

Usually this means `Owner` or `Contributor` on the subscription or target resource group.

## Recommended Test VM

```txt
Ubuntu 24.04 LTS
Standard B2s minimum
2 vCPU
4 GB RAM
Premium SSD
Static public IP
Ports: 22, 80, 443
```

For browser automation or multiple workers:

```txt
Standard B2ms or D2s v5
2 vCPU
8 GB RAM
```

## Suggested Runtime

- Docker / Docker Compose.
- Caddy or Nginx for HTTPS.
- systemd services for Hermes and webhook workers.
- Telegram webhook endpoint.
- Sendblue/iMessage webhook endpoint.
- Tailscale optional for private admin access.

## Webhook Shape

```txt
https://os.yourdomain.com/webhooks/telegram
https://os.yourdomain.com/webhooks/sendblue
https://os.yourdomain.com/webhooks/events
```
