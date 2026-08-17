# System Structure

BusinessOS is a generic core deployed as one isolated VM per company. The company-specific shape comes from private instance configuration, connected evidence, and the observed business model. It does not come from industry assumptions embedded in the repository.

The complete architecture is maintained as Mermaid in `docs/architecture/businessos-general.mmd`.

## Three Product Layers

1. **Business intelligence:** evidence ledger, living business model, underwriting, risks, scaling plan, projections, and missing capability detection.
2. **Operating desk:** a plain-language dashboard for the owner, partner, and later scoped manager or employee views.
3. **Hermes execution loop:** research, recommendation, approval, isolated build, independent review, proof, release, measurement, and learning.

## Stage Behavior

### Pre-acquisition

BusinessOS works read-only by default. It maps the evidence, reconstructs and reconciles the business, produces a professional acquisition write-up, identifies decision-changing gaps, and drafts the first post-close plan.

### Post-acquisition

BusinessOS keeps the baseline current, finds risks and inefficiencies, identifies missing capabilities, researches current options and costs, proposes costed initiatives, and executes approved work through the quality lifecycle.

## Instance Boundary

- One business per VM.
- One private `business.yaml` and `.env` per VM.
- No cross-business memory, credentials, or runtime data.
- Credentials are entered manually for now and are never shown in the dashboard.
- New integrations start read-only and receive write authority only for approved work.

## Proof Before Major Change

BusinessOS selects historical backtesting, simulation, shadow mode, or a small pilot based on the evidence and risk. Direct launch is reserved for low-risk, reversible changes. Every initiative has a promotion gate, stop condition, rollback, and actual-versus-projected review.
