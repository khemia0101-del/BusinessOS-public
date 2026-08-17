import { SecondaryLink } from "@/components/ui";

export default function NotFound() {
  return (
    <div className="page">
      <div className="panel empty-state">
        <h2>This BusinessOS view does not exist</h2>
        <p>Return to the operating overview to continue.</p>
        <div style={{ marginTop: 16 }}>
          <SecondaryLink href="/">Return to overview</SecondaryLink>
        </div>
      </div>
    </div>
  );
}
