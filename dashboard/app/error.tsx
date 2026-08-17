"use client";

export default function ErrorPage({
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div className="page">
      <div className="panel empty-state" role="alert">
        <h2>This view could not load</h2>
        <p>
          The underlying business data was not changed. Try loading the view
          again.
        </p>
        <button
          className="button button-primary"
          onClick={reset}
          style={{ marginTop: 16 }}
          type="button"
        >
          Try again
        </button>
      </div>
    </div>
  );
}
