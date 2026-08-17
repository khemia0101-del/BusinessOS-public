import Link from "next/link";
import { evidenceCoverage, findings, initiatives } from "@/lib/demo-data";
import {
  DemoNotice,
  PageHeading,
  PrimaryLink,
  SectionHeading,
  Status,
} from "@/components/ui";

const activities = [
  {
    title: "QuickBooks sync needs attention",
    detail: "The latest financial pull did not finish.",
    time: "18m",
  },
  {
    title: "Two seller documents were indexed",
    detail: "Insurance history and employee roster.",
    time: "1h",
  },
  {
    title: "Job-margin shadow report completed",
    detail: "21 closed jobs compared with the bookkeeping view.",
    time: "3h",
  },
  {
    title: "CRM recommendation updated",
    detail: "Implementation effort and a backtest plan were added.",
    time: "Yesterday",
  },
];

export default function OverviewPage() {
  const averageCoverage = Math.round(
    evidenceCoverage.reduce((total, item) => total + item.coverage, 0) /
      evidenceCoverage.length,
  );

  return (
    <div className="page">
      <PageHeading
        title="Good morning. Here is what matters."
        description="BusinessOS has organized the latest evidence into decisions, risks, and work you can verify."
        action={<PrimaryLink href="/work">Review 2 decisions</PrimaryLink>}
      />
      <DemoNotice />

      <section className="summary-strip" aria-label="Business summary">
        <div className="summary-item">
          <span className="summary-label">Underwriting status</span>
          <span className="summary-value">Decision-ready</span>
          <span className="summary-detail">3 material gaps remain</span>
        </div>
        <div className="summary-item">
          <span className="summary-label">Evidence coverage</span>
          <span className="summary-value">{averageCoverage}%</span>
          <span className="summary-detail">Across 5 decision domains</span>
        </div>
        <div className="summary-item">
          <span className="summary-label">Needs your decision</span>
          <span className="summary-value">2</span>
          <span className="summary-detail">$1,900 proposed setup cost</span>
        </div>
        <div className="summary-item">
          <span className="summary-label">Being tested</span>
          <span className="summary-value">3</span>
          <span className="summary-detail">No public changes active</span>
        </div>
      </section>

      <div className="content-grid">
        <div className="stack">
          <section>
            <SectionHeading
              title="What BusinessOS found"
              detail="Material findings only. Each one links back to evidence."
              action={
                <Link className="text-link" href="/underwriting">
                  Open underwriting
                </Link>
              }
            />
            <div className="panel">
              <ul className="finding-list">
                {findings.map((finding) => (
                  <li className="finding-row" key={finding.title}>
                    <div>
                      <h3>{finding.title}</h3>
                      <p>{finding.detail}</p>
                    </div>
                    <Status tone={finding.tone}>{finding.impact}</Status>
                  </li>
                ))}
              </ul>
            </div>
          </section>

          <section>
            <SectionHeading
              title="Active plan"
              detail="The highest-priority post-close work, with proof before rollout."
              action={
                <Link className="text-link" href="/scaling">
                  Open scaling plan
                </Link>
              }
            />
            <div className="panel table-wrap">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Initiative</th>
                    <th>Stage</th>
                    <th>Cost</th>
                    <th>Expected result</th>
                  </tr>
                </thead>
                <tbody>
                  {initiatives.slice(0, 3).map((initiative) => (
                    <tr key={initiative.id}>
                      <td>
                        <div className="initiative-title">
                          <span>{initiative.id}</span>
                          <strong>{initiative.title}</strong>
                        </div>
                      </td>
                      <td>
                        <Status
                          tone={
                            initiative.state === "Needs decision"
                              ? "warning"
                              : "info"
                          }
                        >
                          {initiative.state}
                        </Status>
                      </td>
                      <td>{initiative.cost}</td>
                      <td>{initiative.impact}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        </div>

        <aside className="stack">
          <section>
            <SectionHeading
              title="Needs your decision"
              detail="Nothing launches from this screen automatically."
            />
            <div className="panel">
              <ul className="decision-list">
                <li className="decision-row">
                  <h3>Pilot a shared lead pipeline</h3>
                  <p>
                    Backtest suggests 11 recoverable estimates. Approve a 30-day
                    internal pilot before any customer automation.
                  </p>
                  <div className="decision-meta">
                    <Status tone="warning">Owner + partner</Status>
                    <span className="decision-cost">$1,300 setup · $90/mo</span>
                  </div>
                </li>
                <li className="decision-row">
                  <h3>Request missing claims history</h3>
                  <p>
                    This blocks a final legal and insurance risk conclusion.
                  </p>
                  <div className="decision-meta">
                    <Status tone="danger">Material gap</Status>
                    <span className="decision-cost">No cost</span>
                  </div>
                </li>
              </ul>
            </div>
          </section>

          <section>
            <SectionHeading title="Underwriting readiness" />
            <div className="panel readiness">
              <div className="readiness-score">
                <strong>{averageCoverage}%</strong>
                <span>evidence coverage</span>
              </div>
              <div className="readiness-copy">
                <strong>Proceed with conditions</strong>
                <span>
                  Revenue and people evidence is usable. Legal history and
                  customer-level job data still need resolution.
                </span>
              </div>
            </div>
          </section>

          <section>
            <SectionHeading title="Recent activity" />
            <div className="panel">
              <ul className="activity-list">
                {activities.map((activity) => (
                  <li className="activity-row" key={activity.title}>
                    <span className="activity-marker" aria-hidden="true" />
                    <div>
                      <strong>{activity.title}</strong>
                      <span>{activity.detail}</span>
                    </div>
                    <time>{activity.time}</time>
                  </li>
                ))}
              </ul>
            </div>
          </section>
        </aside>
      </div>
    </div>
  );
}
