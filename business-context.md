# Business Context

This file is the generic context contract. Hermes builds the live business context from `instance/business.yaml` and source-linked evidence. Do not add company facts to this tracked template.

## Instance Identity

- Business name: from private instance configuration
- Stage: `pre_acquisition`, `transition`, or `operating`
- Industry: evidence-backed, not inferred from the company name
- Primary sources: defined by the instance and connected integrations

## Evidence Domains

- Transaction and ownership
- Historical financial performance
- Revenue quality and customer concentration
- Sales and marketing
- Delivery and operations
- People and organizational design
- Technology and data
- Legal, regulatory, insurance, and compliance
- Market, competition, and reputation
- Post-close risks, opportunities, and dependencies

## Working Assumptions

- Financial, tax, HR, customer, legal, and compliance material is sensitive.
- Industry-specific rules must be researched and cited before they are treated as constraints.
- The tracked core remains portable and contains no company secrets.

## Primary Business Questions

- How does the company make money, and which customers, channels, products, or jobs drive the economics?
- What is the normalized revenue, gross profit, EBITDA or SDE, cash conversion, and working-capital baseline?
- How reliable are the books, and which records conflict?
- What does the lead-to-cash process look like?
- Which people and workflows are critical or overloaded?
- What legal, regulatory, contractual, and insurance constraints govern the business?
- Which bottlenecks prevent growth after acquisition?
- Which missing capabilities are obvious from the evidence, and what would each cost to implement?
- Which changes require approval, historical backtesting, simulation, shadow mode, or a pilot?

## Source Discipline

Every factual claim needs a source reference. Every estimate needs its method and assumptions. Every unresolved conflict stays visible until reconciled.
