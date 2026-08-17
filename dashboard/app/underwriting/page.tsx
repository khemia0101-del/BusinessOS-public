import {
  Confidence,
  DemoNotice,
  PageHeading,
  SectionHeading,
  Status,
} from "@/components/ui";
import { evidenceCoverage } from "@/lib/demo-data";

const financials = [
  {
    period: "2023",
    revenue: "$2.84m",
    gross: "$986k",
    reported: "$312k",
    normalized: "$348k",
    status: "Reconciled",
  },
  {
    period: "2024",
    revenue: "$3.16m",
    gross: "$1.14m",
    reported: "$371k",
    normalized: "$402k",
    status: "Explained",
  },
  {
    period: "TTM",
    revenue: "$3.42m",
    gross: "$1.19m",
    reported: "$388k",
    normalized: "$421k",
    status: "Open difference",
  },
];

const risks = [
  {
    risk: "Owner controls estimating and schedule approval",
    likelihood: "High",
    impact: "High",
    protection: "Fund a replacement role and require a 90-day transition.",
  },
  {
    risk: "Claims history has not been provided",
    likelihood: "Medium",
    impact: "Critical",
    protection: "Receipt and review before final decision.",
  },
  {
    risk: "Top five customers are 31% of TTM revenue",
    likelihood: "Medium",
    impact: "Medium",
    protection: "Confirm repeatability and model a 20% loss case.",
  },
];

export default function UnderwritingPage() {
  return (
    <div className="page">
      <PageHeading
        title="Underwriting"
        description="A decision-ready view of the business, with every important conclusion tied to evidence or a visible assumption."
        action={<Status tone="warning">Proceed with conditions</Status>}
      />
      <DemoNotice />

      <div className="page-grid">
        <div className="stack">
          <section>
            <SectionHeading
              title="Evidence coverage"
              detail="Coverage is measured by decision domain, not file count."
            />
            <div className="panel">
              <ul className="coverage-list">
                {evidenceCoverage.map((item) => (
                  <li className="coverage-row" key={item.domain}>
                    <div className="coverage-domain">
                      <strong>{item.domain}</strong>
                      <span>
                        {item.coverage >= 80
                          ? "Strong source coverage"
                          : "Reviewable evidence"}
                      </span>
                    </div>
                    <div>
                      <div
                        className="progress-track"
                        aria-label={`${item.domain} ${item.coverage}% covered`}
                      >
                        <div
                          className="progress-fill"
                          style={{ width: `${item.coverage}%` }}
                        />
                      </div>
                      <div className="progress-value">
                        {item.coverage}% covered
                      </div>
                    </div>
                    <Confidence value={item.confidence} />
                    <span className="coverage-gap">Missing: {item.gap}</span>
                  </li>
                ))}
              </ul>
            </div>
          </section>

          <section>
            <SectionHeading
              title="Historical and normalized earnings"
              detail="Seller adjustments and underwriter adjustments remain separate in the full report."
            />
            <div className="panel table-wrap">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Period</th>
                    <th className="numeric">Revenue</th>
                    <th className="numeric">Gross profit</th>
                    <th className="numeric">Reported earnings</th>
                    <th className="numeric">Normalized earnings</th>
                    <th>Reconciliation</th>
                  </tr>
                </thead>
                <tbody>
                  {financials.map((row) => (
                    <tr key={row.period}>
                      <td>
                        <strong>{row.period}</strong>
                      </td>
                      <td className="numeric">{row.revenue}</td>
                      <td className="numeric">{row.gross}</td>
                      <td className="numeric">{row.reported}</td>
                      <td className="numeric">{row.normalized}</td>
                      <td>
                        <Status
                          tone={
                            row.status === "Reconciled"
                              ? "positive"
                              : row.status === "Explained"
                                ? "info"
                                : "warning"
                          }
                        >
                          {row.status}
                        </Status>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>

          <section>
            <SectionHeading title="Material risks and deal protections" />
            <div className="panel table-wrap">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Risk</th>
                    <th>Likelihood</th>
                    <th>Impact</th>
                    <th>Protection or condition</th>
                  </tr>
                </thead>
                <tbody>
                  {risks.map((row) => (
                    <tr key={row.risk}>
                      <td>
                        <strong>{row.risk}</strong>
                      </td>
                      <td
                        className={
                          row.likelihood === "High"
                            ? "risk-high"
                            : "risk-medium"
                        }
                      >
                        {row.likelihood}
                      </td>
                      <td
                        className={
                          row.impact === "Critical" || row.impact === "High"
                            ? "risk-high"
                            : "risk-medium"
                        }
                      >
                        {row.impact}
                      </td>
                      <td>{row.protection}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        </div>

        <aside className="stack">
          <div className="side-note">
            <h2>Decision brief</h2>
            <p>
              The earnings profile supports continued diligence, but the current
              conclusion depends on insurance history, customer-level job
              records, and the treatment of one owner add-back.
            </p>
            <ul className="plain-list">
              <li>Normalized TTM earnings: $421k</li>
              <li>Open reconciliation difference: $38k</li>
              <li>Three material evidence requests remain</li>
            </ul>
          </div>
          <div className="side-note">
            <h2>Evidence still needed</h2>
            <ul className="plain-list">
              <li>Five-year insurance claims history</li>
              <li>Customer-level job export for the last 24 months</li>
              <li>March operating bank statement</li>
              <li>Support for $46k nonrecurring owner add-back</li>
            </ul>
          </div>
          <div className="side-note">
            <h2>Report rule</h2>
            <p>
              BusinessOS will not call this final until each material gap is
              received, resolved, or explicitly waived by the decision makers.
            </p>
          </div>
        </aside>
      </div>
    </div>
  );
}
