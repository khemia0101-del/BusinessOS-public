import {
  DemoNotice,
  PageHeading,
  PrimaryLink,
  SecondaryLink,
  Status,
} from "@/components/ui";

export default function ComponentsPage() {
  return (
    <div className="page">
      <PageHeading
        title="BusinessOS components"
        description="The internal component reference for building consistent business views. This route is intentionally outside the main navigation."
      />
      <DemoNotice />

      <div className="components-layout">
        <section className="component-sample">
          <h2>Status</h2>
          <div className="component-row">
            <Status>Researching</Status>
            <Status tone="info">Being tested</Status>
            <Status tone="positive">Healthy</Status>
            <Status tone="warning">Needs decision</Status>
            <Status tone="danger">Material risk</Status>
          </div>
        </section>

        <section className="component-sample">
          <h2>Actions</h2>
          <div className="component-row">
            <PrimaryLink href="/work">Review decision</PrimaryLink>
            <SecondaryLink href="/underwriting">View evidence</SecondaryLink>
            <span className="button button-secondary" aria-disabled="true">
              Unavailable
            </span>
          </div>
        </section>

        <section className="component-sample">
          <h2>Evidence coverage</h2>
          <div className="coverage-domain">
            <strong>Revenue quality</strong>
            <span>Customer-level job history is still needed</span>
          </div>
          <div style={{ marginTop: 12 }}>
            <div
              className="progress-track"
              aria-label="Revenue quality 61% covered"
            >
              <div className="progress-fill" style={{ width: "61%" }} />
            </div>
            <div className="progress-value">61% covered</div>
          </div>
        </section>

        <section className="component-sample">
          <h2>Empty state</h2>
          <div className="empty-state">
            <h2>No public changes are active</h2>
            <p>
              Approved work stays in testing until its promotion gate and final
              release checks pass.
            </p>
          </div>
        </section>
      </div>
    </div>
  );
}
