export default function Loading() {
  return (
    <div
      className="page"
      aria-busy="true"
      aria-label="Loading business workspace"
    >
      <div className="skeleton skeleton-line" />
      <div className="skeleton skeleton-line" style={{ width: "45%" }} />
      <div className="skeleton skeleton-block" style={{ marginTop: 28 }} />
    </div>
  );
}
