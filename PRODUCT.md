# BusinessOS Product Brief

## Product

BusinessOS is a private operating system that is deployed on a separate VM for each acquisition target or owned business. It learns the company from its documents, systems, meetings, analytics, and people, then turns that evidence into decisions and controlled execution.

## Who It Is For

- The owner/operator and acquisition partner, who need the whole business in one place.
- Nontechnical managers and employees, who need simple questions, tasks, and updates rather than agent or infrastructure terminology.
- Hermes and specialist agents, which need a stable operating contract, evidence model, and approval boundary.

The owner is the only expected developer. The normal interface must not require technical knowledge.

## Jobs To Be Done

### Before acquisition

1. Ingest and map every available source.
2. Build a professional, source-linked underwriting report.
3. Reconcile financials and state what is known, assumed, conflicting, or missing.
4. Explain the business model, people, systems, risks, and realistic upside.
5. Produce a clear diligence question and request list.

### After acquisition

1. Establish the operational and financial baseline.
2. Produce a scaling plan with projections, costs, tools, channels, owners, and actions.
3. Find inefficiencies and missing capabilities without waiting for the owner to specify the answer.
4. Turn approved recommendations into tested internal tools, automations, and operating changes.
5. Monitor results and update the business model continuously.

## Core Product Model

BusinessOS has three visible parts:

1. **Business intelligence:** evidence, underwriting, risks, and scaling plan.
2. **Operating desk:** dashboard, approvals, work, integrations, and people signals.
3. **Hermes execution loop:** observe, recommend, approve, build, verify, release, measure, and learn.

## Operating Constraints

- One business per VM. Instances do not share company data, credentials, or memory.
- The repository is generic. Business-specific facts live in private instance configuration and runtime data.
- Pre-acquisition access is read-only unless a narrow exception is explicitly approved.
- API keys are entered manually into the VM `.env` for now. The dashboard reports integration health but does not display or edit secrets.
- Material, public, financial, people, compliance, or production changes require recorded approval.
- An agent cannot approve its own work.
- Uncertain or high-impact changes can be backtested, simulated, or run in shadow mode before a live pilot.
- Every material claim, projection, and recommendation must trace to evidence or be labeled as an assumption.

## Product Principles

1. **Plain language first.** Show business meaning before technical detail.
2. **Evidence before confidence.** Every important conclusion is source-linked and uncertainty is visible.
3. **A recommendation includes the real plan.** Cost, expected impact, owner, dependencies, risk, test, and next decision travel together.
4. **Quiet autonomy.** BusinessOS researches and prepares safe work on its own, then asks only for decisions or access that truly block progress.
5. **Prove major changes.** Backtest or simulate when historical activity can answer the question; use shadow mode or a small pilot when it cannot.

## Success

The owner can open one screen and understand the health of the business, the quality of the evidence, the most important risks and opportunities, what needs a decision, and what changed as a result. A nontechnical manager can use their part without learning how the agent system works.
