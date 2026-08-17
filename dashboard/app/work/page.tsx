import { Check, FlaskConical, ShieldCheck } from "lucide-react";
import {
  DemoNotice,
  PageHeading,
  SectionHeading,
  Status,
} from "@/components/ui";

const workItems = [
  {
    title: "Pilot a shared lead pipeline",
    detail: "$1,300 setup · $90/mo",
    status: "Needs decision",
    current: true,
  },
  {
    title: "Request missing claims history",
    detail: "No cost · blocks final risk view",
    status: "Needs decision",
    current: false,
  },
  {
    title: "Job-level margin reporting",
    detail: "Shadow report on 21 closed jobs",
    status: "Testing",
    current: false,
  },
  {
    title: "Crew-lead scheduling authority",
    detail: "Historical simulation in progress",
    status: "Researching",
    current: false,
  },
];

export default function WorkPage() {
  return (
    <div className="page">
      <PageHeading
        title="Work and decisions"
        description="See what BusinessOS found, what it needs from you, and how approved work is being proven before launch."
      />
      <DemoNotice />

      <div className="work-layout">
        <section>
          <SectionHeading
            title="Needs attention"
            detail="The selected recommendation is shown in full."
          />
          <div className="work-list">
            {workItems.map((item) => (
              <div
                className="work-item"
                aria-current={item.current ? "true" : undefined}
                key={item.title}
              >
                <div className="work-item-top">
                  <h3>{item.title}</h3>
                  <Status
                    tone={
                      item.status === "Needs decision"
                        ? "warning"
                        : item.status === "Testing"
                          ? "info"
                          : "neutral"
                    }
                  >
                    {item.status}
                  </Status>
                </div>
                <p>{item.detail}</p>
              </div>
            ))}
          </div>
        </section>

        <section>
          <SectionHeading
            title="Decision detail"
            detail="No action is wired in this illustrative workspace."
          />
          <article className="decision-detail">
            <header>
              <Status tone="warning">Owner + partner approval</Status>
              <h2>Pilot a shared lead-to-estimate pipeline</h2>
            </header>

            <div className="decision-section">
              <h3>Why this is being recommended</h3>
              <p>
                Forty-three inquiries have no recorded next step, and follow-up
                ownership is split between two inboxes and three spreadsheets. A
                shared pipeline is the minimum capability needed to measure and
                recover the leakage.
              </p>
            </div>

            <div className="decision-facts">
              <div className="decision-fact">
                <span>Expected monthly cost</span>
                <strong>$90 after $1,300 setup</strong>
              </div>
              <div className="decision-fact">
                <span>Base expected impact</span>
                <strong>$11,800 monthly gross profit</strong>
              </div>
              <div className="decision-fact">
                <span>Earliest reliable result</span>
                <strong>30 days after pilot starts</strong>
              </div>
            </div>

            <div className="decision-section">
              <h3>
                <FlaskConical aria-hidden="true" size={15} /> How we prove it
              </h3>
              <p>
                Replay 18 months of inquiry data to establish recoverable
                follow-up, then run a 30-day internal pilot. No automated
                customer messages are included.
              </p>
            </div>

            <div className="decision-section">
              <h3>
                <ShieldCheck aria-hidden="true" size={15} /> Stop and rollback
              </h3>
              <p>
                Stop if weekly admin exceeds four hours, duplicate follow-up
                exceeds 2%, or the recovered gross profit is below $3,000.
                Export the pilot records and return to the current process.
              </p>
            </div>

            <div className="decision-section">
              <h3>
                <Check aria-hidden="true" size={15} /> If approved
              </h3>
              <p>
                BusinessOS creates an isolated build branch and setup checklist.
                You add the selected provider key to `.env`. Independent review
                and the pilot promotion gate happen before any live rollout.
              </p>
            </div>

            <footer className="decision-actions">
              <p>
                Approval controls the pilot scope only. It does not approve
                public launch.
              </p>
              <div className="button-group">
                <span className="button button-secondary" aria-disabled="true">
                  Postpone
                </span>
                <span className="button button-primary" aria-disabled="true">
                  Approve pilot
                </span>
              </div>
            </footer>
          </article>
        </section>
      </div>
    </div>
  );
}
