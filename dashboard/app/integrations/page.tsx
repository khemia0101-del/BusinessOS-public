import { LiveWorkspace } from "@/components/live-workspace";
import { KeyRound } from "lucide-react";
import {
  DemoNotice,
  PageHeading,
  SectionHeading,
  Status,
} from "@/components/ui";
import { integrations } from "@/lib/demo-data";

function integrationTone(state: string) {
  if (state === "Healthy") return "positive" as const;
  if (state === "Needs attention") return "warning" as const;
  return "neutral" as const;
}

export default function IntegrationsPage() {
  if (process.env.BUSINESSOS_MODE !== "demo") return <LiveWorkspace view="integrations" />;
  return (
    <div className="page">
      <PageHeading
        title="Integrations"
        description="See which business systems are available to BusinessOS and whether their latest sync is healthy."
      />
      <DemoNotice />

      <div className="setup-callout">
        <KeyRound aria-hidden="true" size={18} />
        <div>
          <h2>Credentials are managed manually for now</h2>
          <p>
            Add API keys to the VM `.env`, then restart the relevant service.
            This dashboard reports configuration and health only; it never
            displays the secret value.
          </p>
        </div>
      </div>

      <section>
        <SectionHeading
          title="Connected systems"
          detail="A system may be configured but still need attention if its latest sync fails."
        />
        <div className="panel">
          <ul className="integration-list">
            {integrations.map((integration) => (
              <li className="integration-row" key={integration.name}>
                <div className="integration-name">
                  <strong>{integration.name}</strong>
                  <span>{integration.category}</span>
                </div>
                <span className="integration-detail">{integration.detail}</span>
                <Status tone={integrationTone(integration.state)}>
                  {integration.state}
                </Status>
                <code className="env-key">{integration.env}</code>
              </li>
            ))}
          </ul>
        </div>
      </section>
    </div>
  );
}
