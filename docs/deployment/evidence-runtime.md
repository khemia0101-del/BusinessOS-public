# Evidence runtime and live dashboard

The version 2 runtime adds local evidence ingestion, decimal calculations, versioned underwriting reports, independent review, initiative measurement, and on-demand notebook exchange. Accounting and banking exports can be ingested now. Direct provider OAuth connectors are not implemented by this release.

## Install and start

Use Python 3.12+ and Node.js 22+. From the repository root:

```sh
python -m venv .venv
# Activate the virtual environment for your platform.
python -m pip install -r requirements-runtime.txt
python -m businessos --business your-company configure /private/company.json
python -m businessos --business your-company serve --port 8790
```

`company.json` contains `display_name`, `industry` (`construction` or `unknown`), and optional `notebook_url`. Runtime identity is the `--business` value or `BUSINESSOS_INSTANCE_ID`, not a client request. Existing `instance/business.yaml` remains the Hermes configuration. Use the same ID and display name; configuration import from YAML is explicit, not an implicit stage setting.

Set three distinct random secrets of at least 24 characters: `BUSINESSOS_OWNER_TOKEN`, `BUSINESSOS_REVIEWER_TOKEN`, and `BUSINESSOS_WORKER_TOKEN`. Set `BUSINESSOS_DATA_DIR` to private, backed-up storage, `BUSINESSOS_API_URL=http://127.0.0.1:8790`, and `BUSINESSOS_MODE=live`. `BUSINESS_STAGE` remains the sole stage setting. Invalid stages resolve to pre-acquisition. Port 8790 avoids the existing inbound gateway on 8787.

From `dashboard`, run `npm ci`, `npm run build`, and `npm start`. Load the same environment into both processes. Next.js does not automatically load the repository parent's `.env`. The dashboard uses HTTP Basic authentication with username `owner` or `reviewer` and that role's token as password. Tokens remain server-side except the browser's normal authentication header. Never paste tokens into notebook chats or model prompts.

Bind both services to loopback. Put authenticated HTTPS with request/rate limits in front of the dashboard for any remote access. Do not expose Python's development HTTP server directly. Restrict the data directory to its service account (Windows ACLs or Unix 0700 directory/0600 files). The local Windows launcher inherits the current user's permissions and binds both ports to loopback.

On Windows, after installation and build, run `./scripts/Start-EvidenceRuntime.ps1 -BusinessId your-company`. It starts both services on loopback, refuses occupied ports, and stops its Python child when the dashboard exits. It creates three random role credentials encrypted with Windows DPAPI in ignored `instance/private/runtime-credentials.clixml`. Do not distribute that file; assign the reviewer credential only to the actual independent reviewer through a protected channel. Role separation assumes the operator does not impersonate that reviewer.

To retrieve the owner password locally in your own PowerShell session:

```powershell
$runtimeCredentials = Import-Clixml -LiteralPath ./instance/private/runtime-credentials.clixml
[System.Net.NetworkCredential]::new('', $runtimeCredentials['owner']).Password
```

Sign in at the launcher's URL with username `owner`. Keep credential output out of screenshots, repository files, and chat. The launcher stores no plaintext credential file. This local setup is not a production identity provider; deploy behind managed identity/HTTPS before multi-user remote access.

## Workflow

1. Open Sources & notebook. Add originals using a stable document identity. Reuse that identity when replacing a statement with a new version. Previous versions are retained and dependent reports become stale.
2. Inspect extracted text and original downloads. Spreadsheet formulas and cached values are preserved separately. Missing formula caches remain unknown. Scanned PDFs without text need OCR before report use.
3. Create a version 2 input JSON using `docs/underwriting/runtime-input.md`. Import it on Underwriting. Calculations run without model calls. The full input fingerprint supports exact repeat requests; changed reports require a new ID.
4. Have a separate reviewer inspect originals and calculation assumptions. They must acknowledge every outstanding gap before approving a conditional report. Neither report approval nor a stage label authorizes buying a company or executing external changes.
5. Import initiatives with sourced baselines. Run shadow tests and record actual observations. Pilot and active states require a reviewer, measured evidence, and transition/operating stage. These states record approval; they do not send campaigns or change source systems.
6. Use notebook exchange only when helpful. It is never a prerequisite to calculation, review, or operating work.

## Notebook host contract

`integrations/notebook/adapter.mjs` exports `runNotebookJob(job, tab, options)`. A trusted browser-capable host supplies the existing signed-in CUA tab. The module does not retrieve cookies or call undocumented Google APIs. It checks the notebook identity, complete source inventory, and citations. For publication the host must confirm the exact reviewed report and destination, then pass `confirmPublication: true`.

The host reads `GET /notebook/jobs` with the worker token, selects an explicitly requested pending job, claims it with `POST /notebook/jobs/{id}/claim` and `{}`, calls the adapter, and submits the returned object to `POST /notebook/jobs/{id}/result` with the worker token. A claim is exclusive; interrupted running jobs require manual reconciliation. The worker token cannot read the rest of the company runtime. A Codex/Hermes operator can also perform these same steps through its approved browser tools. This is an on-demand host integration, not a background browser daemon. No scheduler or persistent browser login is installed by this release.

Report publication uses report ID plus content hash for deduplication. Failed login is `login_required`, UI changes are `failed`, and interrupted external writes are `uncertain`. Never automatically retry uncertain publication. Reconcile its existing source, content, and processing state first. Matching source titles alone are insufficient. Notebook answers and exported BusinessOS reports never count as independent financial corroboration.

## Recovery and compatibility

- Existing version 1 reports remain readable with the original validator. Run `python -m businessos --business ID migrate old.json --mapping explicit-mapping.json --output new-input.json` to prepare a version 2 input. Migration does not approve the old conclusion or infer fiscal dates.
- Stop writes and back up the company SQLite database with SQLite's backup API and its evidence directory together. Test restore into a separate data root before replacing an active instance. Never delete the only evidence copy. Automated backup scheduling is a deployment task, not installed by the runtime.
- Stopping the new services leaves the prior gateway and source systems unchanged. Use `BUSINESSOS_MODE=demo` only with synthetic data; it intentionally disables access to the private runtime and displays illustrative screens.
- `/healthz` and dashboard `/api/health` report process health. `/snapshot` reports evidence and notebook status separately. Last notebook verification is an observation, not a guarantee the session remains signed in.

## Verification

```sh
python -m unittest discover -s tests -v
node --test integrations/notebook/adapter.test.mjs
cd dashboard
npm run typecheck
npm run build
npm run test:smoke
npm run test:live
```

Tests use synthetic data and temporary databases. Passing tests does not certify a target company's financial statements, a live Google publication, or a deployed environment.
