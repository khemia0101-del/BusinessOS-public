# Evidence Source Map

This tracked file defines the map format. The live source inventory is generated privately for each business from `instance/business.yaml` and connected integrations.

## Source Registry

| Source ID     | System       | Record or folder           | Period  | Access      | Last indexed | Reliability | Use                                              |
| ------------- | ------------ | -------------------------- | ------- | ----------- | ------------ | ----------- | ------------------------------------------------ |
| `SRC-EXAMPLE` | Example only | Replace in private runtime | Unknown | Unavailable | Never        | Unknown     | Delete this row when the first source is indexed |

## Expected Source Groups

- Diligence and transaction documents
- Accounting, tax, payroll, banking, and payment records
- Customer, job, order, contract, subscription, and CRM records
- Website, advertising, search, social, email, product, and content analytics
- Process documents, calendars, task systems, and operational databases
- Employee roster, responsibilities, compensation, interviews, and meeting records
- Legal, regulatory, insurance, licensing, security, and compliance records
- Reviews, support, complaints, refunds, cancellations, and other customer signals

## Rules

- Index readable sources without changing them.
- Assign a stable source ID before using a record as evidence.
- Record the exact location, period, retrieval time, access level, and reliability.
- Track documents that conflict, overlap, or leave a material period uncovered.
- Cite the source ID beside every material claim, calculation, and recommendation.
- Summarize sensitive material only as needed; do not copy raw records into the tracked repository.
- Create an access request only when the source blocks a material conclusion or approved initiative.

## Missing Evidence Request

Each request states:

- Evidence needed
- Decision or conclusion it affects
- Materiality: critical, material, or supporting
- Expected owner and source system
- Period required
- Acceptable substitute
- Status and deadline
