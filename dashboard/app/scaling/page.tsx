import {
  DemoNotice,
  PageHeading,
  SectionHeading,
  Status,
} from "@/components/ui";
import { initiatives } from "@/lib/demo-data";

const horizons = [
  { time: "Day 0-30", objective: "Protect cash, customers, and delivery" },
  { time: "Day 31-100", objective: "Install visibility and clear ownership" },
  {
    time: "Month 4-12",
    objective: "Scale the channels and workflows that prove out",
  },
  { time: "Year 2-3", objective: "Add durable capacity and strategic growth" },
];

const stateTone = (state: string) => {
  if (state === "Needs decision") return "warning" as const;
  if (state === "Being tested") return "info" as const;
  return "neutral" as const;
};

export default function ScalingPage() {
  return (
    <div className="page">
      <PageHeading
        title="Scaling plan"
        description="A costed post-acquisition plan tied to the actual baseline, operating constraints, and a clear proof method."
        action={<Status tone="info">Working plan</Status>}
      />
      <DemoNotice />

      <section className="horizon-grid" aria-label="Scaling horizons">
        {horizons.map((horizon) => (
          <div className="horizon" key={horizon.time}>
            <span>{horizon.time}</span>
            <strong>{horizon.objective}</strong>
          </div>
        ))}
      </section>

      <div className="stack">
        <section>
          <SectionHeading
            title="Initiatives"
            detail="Costs include vendor spend and internal work. Expected results are ranges, not promises."
          />
          <div className="panel table-wrap">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Initiative</th>
                  <th>Horizon</th>
                  <th>State</th>
                  <th>Cost</th>
                  <th>Expected result</th>
                  <th>How we prove it</th>
                </tr>
              </thead>
              <tbody>
                {initiatives.map((initiative) => (
                  <tr key={initiative.id}>
                    <td>
                      <div className="initiative-title">
                        <span>{initiative.id}</span>
                        <strong>{initiative.title}</strong>
                      </div>
                    </td>
                    <td>{initiative.horizon}</td>
                    <td>
                      <Status tone={stateTone(initiative.state)}>
                        {initiative.state}
                      </Status>
                    </td>
                    <td>{initiative.cost}</td>
                    <td>{initiative.impact}</td>
                    <td>{initiative.proof}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <div className="page-grid">
          <section>
            <SectionHeading
              title="Three-year operating case"
              detail="Illustrative annual exit run rate after initiative costs."
            />
            <div className="panel scenario-grid">
              <div className="scenario">
                <span>Downside</span>
                <strong>$3.3m</strong>
                <small>Revenue · $350k normalized earnings</small>
              </div>
              <div className="scenario">
                <span>Base</span>
                <strong>$4.6m</strong>
                <small>Revenue · $610k normalized earnings</small>
              </div>
              <div className="scenario">
                <span>Upside</span>
                <strong>$5.5m</strong>
                <small>Revenue · $790k normalized earnings</small>
              </div>
            </div>
          </section>

          <aside className="side-note">
            <h2>Projection guardrails</h2>
            <p>
              The model does not stack every opportunity at full value. It
              applies lead, crew, cash, and implementation constraints before
              initiative effects reach the financial plan.
            </p>
            <ul className="plain-list">
              <li>Base case includes a 90-day CRM ramp.</li>
              <li>
                No new crew revenue before hiring and utilization gates pass.
              </li>
              <li>
                Software, implementation, and working-capital costs are
                included.
              </li>
            </ul>
          </aside>
        </div>
      </div>
    </div>
  );
}
