# Scaling Plan Standard

## Purpose

Turn underwriting and live operating evidence into a practical post-acquisition plan. The plan must say what to do, why it matters, what it costs, who owns it, how it will be tested, and when to stop.

## Inputs

- Latest underwriting report and unresolved risks
- Actual revenue, margin, cash, capacity, pipeline, and service data
- Systems and integration inventory
- Customer and employee signals
- Owner goals, acquisition thesis, financing constraints, and risk tolerance
- Current market and vendor research with dates and sources

## Planning Horizons

- **Day 0-30: stabilize.** Protect cash, customers, employees, access, and delivery.
- **Day 31-100: establish control.** Fix visibility, ownership, handoffs, measurement, and high-confidence leakage.
- **Month 4-12: scale.** Expand proven channels, capacity, automation, and management systems.
- **Year 2-3: compound.** Add durable capabilities, locations, products, acquisitions, or platform leverage only after the core works.

## Required Sections

### 1. Executive plan

- Owner outcomes and constraints
- Baseline versus target
- Five or fewer operating priorities
- Expected investment, cash requirement, and management load
- Critical assumptions and dependencies

### 2. Business baseline

Show the actual starting point and evidence date for:

- Revenue, gross profit, normalized earnings, cash conversion, and working capital
- Leads, conversion, average order or contract value, sales cycle, retention or repeat rate
- Capacity, cycle time, utilization, backlog, rework, and service quality
- Headcount, role coverage, owner dependence, and key-person risk
- Systems, data quality, and reporting latency

Use `unknown` when a metric cannot be established. Do not fill a gap with a generic industry benchmark.

### 3. Capability gaps

Identify missing systems and operating capabilities from the evidence. Each recommendation must include:

- Problem observed and evidence
- Why the current process fails or leaks value
- Minimum viable capability, not just a product name
- Two or three current options when a vendor is required
- Setup cost, monthly cost, implementation time, internal owner, and migration effort
- Expected benefit and the calculation behind it
- Security, compliance, data ownership, and lock-in considerations
- Recommended option and why it fits this business

Example: if a construction company has no CRM, the plan should connect lost follow-ups, slow estimating, unowned leads, and reporting gaps to the required workflow. It should then compare suitable CRM or field-service options using current pricing and recommend the smallest credible implementation.

### 4. Initiatives

Each initiative is an executable investment case with:

- Objective and baseline
- Actions in order
- Owner and supporting roles
- Tools, channels, and data required
- One-time and recurring cost
- Expected financial and operating impact
- Base, downside, and upside projection
- Dependencies, risks, and compliance review
- Proof method: direct launch, backtest, simulation, shadow mode, or pilot
- Promotion gate, stop condition, and rollback
- Measurement window and reporting cadence
- Current lifecycle state

### 5. Integrated projections

Build a monthly base model for at least 12 months and annual model for three years when evidence supports it. Keep initiative effects separate so the owner can see:

- Baseline without improvements
- Timing and ramp of each initiative
- Revenue and gross-margin effect
- Hiring, software, marketing, capital expenditure, and working-capital cost
- Cash balance and financing need
- Expected payback and break-even month
- Downside if an initiative misses or arrives late

Never add all upside cases together without checking shared leads, capacity, people, cash, and timing constraints.

### 6. Operating cadence

- Daily exceptions, only when material
- Weekly operating review
- Monthly financial and initiative review
- Quarterly plan reset
- Named metric owner and source system for every KPI

## Prioritization

Prioritize by value, confidence, time to evidence, risk, cash requirement, and management load. Prefer the smallest action that proves or disproves the business case.

Do not prioritize a polished internal tool over a broken revenue, cash, delivery, or compliance process unless the tool directly fixes it.

## Proof Method

Use the least disruptive credible method:

1. **Historical backtest:** apply the proposed rule or workflow to real past activity.
2. **Simulation:** model outcomes when historical replay is incomplete but assumptions can be bounded.
3. **Shadow mode:** run beside the live process without taking external action.
4. **Pilot:** use a small approved subset with stop conditions.
5. **Launch:** use when the change is low-risk, reversible, and already well supported.

The machine-readable output must validate against `schemas/scaling-plan.schema.json`.
