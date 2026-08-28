# Dashboard

This is an illustrative owner workspace, not a live business dashboard yet. It uses sample construction-company data from `lib/demo-data.ts`. Integration status, reports, work items, and approval-looking controls are examples; they do not connect accounts or execute business actions.

Use Node.js 22 (Node.js 20.9 or later is supported) and npm:

```sh
npm ci
npm run typecheck
npm run build
npm run test:smoke
npm start
```

Run these commands from `dashboard/`. For local development, use `npm run dev`.

The build copies static assets into `.next/standalone`. `npm start` runs that packaged server; do not use `next start` with this output mode. You can copy the complete `.next/standalone` directory to a separate machine and run `node server.js` there.

For a VM, the service manager must load `/opt/businessos/core/.env` into the process environment. Next.js does not automatically load the parent repository's `.env`. Keep secrets server-side and never use a `NEXT_PUBLIC_` prefix for credentials. Set `HOSTNAME=127.0.0.1` behind the VM's authenticated reverse proxy and set `PORT` as needed (default 3000).

`GET /api/health` reports process health and the configured stage, not integration health. An invalid or missing stage resolves to `pre_acquisition`. Put authentication in front of the dashboard before adding any real business data.
