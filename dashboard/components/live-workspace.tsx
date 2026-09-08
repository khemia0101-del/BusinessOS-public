"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";
import { PageHeading, Status } from "@/components/ui";

type Row = Record<string, any>; // Versioned runtime JSON is validated by the Python service.
type Snapshot = { business: Row; sources: Row[]; reports: Row[]; initiatives: Row[]; notebook_jobs: Row[]; events: Row[]; integration_health: Row; processing: Row; stage: string; role: string; generated_at: string };

function human(value: string) { return value.replaceAll("_", " "); }
function display(value: unknown) { return value === null || value === undefined ? "Unknown" : String(value); }

export function LiveWorkspace({ view }: { view: "overview" | "underwriting" | "scaling" | "work" | "integrations" }) {
  const [state, setState] = useState<Snapshot | null>(null);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);
  const [source, setSource] = useState<Row | null>(null);
  const [selectedReport, setSelectedReport] = useState("");
  const [exceptionsAccepted, setExceptionsAccepted] = useState(false);
  const [projection, setProjection] = useState<Row[] | null>(null);
  const refresh = useCallback(async () => {
    try {
      const response = await fetch("/api/runtime/snapshot", { cache: "no-store" });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error);
      setState(data); setProjection(data.projections?.[0]?.results ?? null); setError("");
      window.dispatchEvent(new CustomEvent("businessos-status", { detail: data }));
    } catch (e) { setError(e instanceof Error ? e.message : "Runtime unavailable"); }
  }, []);
  useEffect(() => { void refresh(); }, [refresh]);
  async function post(path: string, data: Row) {
    setBusy(true); setError(""); setMessage("");
    try {
      const response = await fetch("/api/runtime/" + path, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) });
      const result = await response.json();
      if (!response.ok) throw new Error(result.error ?? "Request failed");
      setMessage(path === "notebook/jobs" ? `Notebook request ${result.status}. A browser worker must verify the result.` : "Saved and verified by the local runtime.");
      await refresh(); return result;
    } catch (e) { setError(e instanceof Error ? e.message : "Request failed"); return null; }
    finally { setBusy(false); }
  }
  async function importJson(event: FormEvent<HTMLFormElement>, path: string) {
    event.preventDefault();
    try {
      const file = new FormData(event.currentTarget).get("file") as File;
      if (!file.size) throw new Error("Select an input JSON file");
      const result = await post(path, JSON.parse(await file.text()));
      if (path === "projections" && result) setProjection(result);
    } catch (e) { setError(e instanceof Error ? e.message : "Invalid input file"); }
  }
  async function upload(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget), file = form.get("file") as File;
    if (!file.size || file.size > 25 * 1024 * 1024) return setError("Choose a file up to 25 MB");
    const buffer = new Uint8Array(await file.arrayBuffer());
    let binary = "";
    for (let i = 0; i < buffer.length; i += 8192) binary += String.fromCharCode(...buffer.subarray(i, i + 8192));
    await post("sources", { filename: file.name, document_id: form.get("document_id"), origin: form.get("origin"), content_base64: btoa(binary) });
  }
  const report = state?.reports.find(r => r.id === selectedReport) ?? state?.reports[0];
  const owner = state?.role === "owner";
  return <div className="page live-workspace">
    <PageHeading title={{ overview: "Evidence into decisions.", underwriting: "Underwriting", scaling: "Scaling plan", work: "Work & decisions", integrations: "Sources & notebook" }[view]} description="Company evidence, calculated results, and explicit review. Notebook is an optional research companion." action={<button className="button button-secondary" disabled={busy} onClick={() => void refresh()}>Refresh</button>} />
    {error && <div role="alert" className="runtime-error">{error}</div>}
    {message && <div role="status" className="runtime-message">{message}</div>}
    {!state ? <section className="panel runtime-panel"><h2>{error ? "Runtime needs attention" : "Loading private workspace…"}</h2><p>Start the BusinessOS runtime and sign in. Unavailable data is never replaced with sample figures.</p></section> : <>
      <div className="runtime-toolbar"><strong>{state.business.display_name}</strong><Status tone="info">{human(state.stage)}</Status><span>Signed in as {state.role} · Updated {new Date(state.generated_at).toLocaleString()}</span></div>
      {view === "overview" && <>
        <section className="summary-strip" aria-label="Verified workspace summary">
          {[ ["Evidence versions", state.sources.length], ["Latest report", report ? human(report.stale ? "stale_evidence" : report.status) : "Not prepared"], ["Material gaps", report ? report.gaps.length : "Unknown"], ["Operating initiatives", state.initiatives.length] ].map(([label, value]) => <div className="summary-item" key={label}><span className="summary-label">{label}</span><strong className="summary-value">{value}</strong></div>)}
        </section>
        <section className="panel runtime-panel"><h2>{report ? human(report.recommendation.decision) : "Establish the evidence baseline"}</h2><p>{report?.recommendation.summary ?? "Add source documents, prepare a financial model, and review the evidence before making an acquisition decision."}</p>{report?.gaps.map((gap: string) => <p key={gap}><Status tone="warning">Unresolved</Status> {human(gap)}</p>)}</section>
        <section className="panel runtime-panel"><h2>Processing</h2><p>{state.processing.sources} source versions · {state.processing.cache_hits} cached extractions · {state.processing.extraction_ms} ms extraction time · ${state.processing.model_cost_usd} model spend in this deterministic runtime.</p><p>External model costs are not included.</p></section>
      </>}
      {view === "underwriting" && <>
        {owner && <section className="panel runtime-panel"><h2>Calculate an underwriting report</h2><p>Import the version 2 financial input file. The runtime calculates earnings and scenarios and checks its citations. Each revision needs a new report ID.</p><form onSubmit={e => void importJson(e, "reports")}><label>Financial input file<input name="file" type="file" accept=".json" required /></label><button className="button button-primary" disabled={busy}>Calculate report</button></form></section>}
        {state.reports.length > 0 && <label>Report version<select value={report?.id} onChange={e => { setSelectedReport(e.target.value); setExceptionsAccepted(false); }}>{state.reports.map(r => <option key={r.id} value={r.id}>{r.id} · {r.as_of_date}</option>)}</select></label>}
        {report ? <>
          <section className="panel runtime-panel"><h2>{human(report.status)} {report.stale && <Status tone="danger">Evidence changed — review again</Status>}</h2><p>{report.recommendation.summary}</p><a className="text-link" href={`/api/runtime/reports/${report.id}/memo`}>Download decision memo</a><p>Actual LTM earnings: {report.ltm ? display(report.ltm.normalized_earnings) : "Not established"}</p></section>
          <section className="panel table-wrap"><table className="data-table"><thead><tr><th>Period</th><th>Basis</th><th>Actual / forecast</th><th>Earnings definition</th><th>Revenue</th><th>Normalized earnings</th></tr></thead><tbody>{report.periods.map((p: Row) => <tr key={p.id}><td>{p.start} – {p.end}</td><td>{p.basis}</td><td><Status tone={p.status === "forecast" ? "warning" : "neutral"}>{p.status}</Status></td><td>{human(p.earnings_definition)}</td><td>{p.currency} {p.revenue}</td><td>{p.normalized_earnings}</td></tr>)}</tbody></table></section>
          <section className="panel table-wrap"><table className="data-table"><thead><tr><th>Scenario</th><th>EBITDA</th><th>Ending cash</th><th>Funding gap</th><th>Coverage</th><th>Enterprise value</th></tr></thead><tbody>{report.scenarios.map((s: Row) => <tr key={s.name}><td>{human(s.name)}</td><td>{s.normalized_ebitda}</td><td>{s.ending_cash}</td><td>{s.funding_gap}</td><td>{display(s.debt_service_coverage)}</td><td>{display(s.enterprise_value)}</td></tr>)}</tbody></table></section>
          <section className="panel runtime-panel"><h2>Coverage and exceptions</h2>{report.coverage.map((c: Row) => <p key={c.id}><Status tone={c.status === "complete" ? "info" : "warning"}>{human(c.status)}</Status> {human(c.id)} — {c.notes}</p>)}<h3>All material gaps</h3>{report.gaps.map((g: string) => <p key={g}>{human(g)}</p>)}</section>
          <section className="panel runtime-panel"><h2>Evidence behind the report</h2>{report.citations.map((c: Row, i: number) => <p key={i}>{c.claim} <button className="text-link" onClick={async () => { const r = await fetch(`/api/runtime/sources/${c.source_id}`); const d = await r.json(); r.ok ? setSource(d) : setError(d.error); }}>{c.source_id} · {c.locator}</button></p>)}</section>
          {state.role === "reviewer" && <section className="panel runtime-panel"><h2>Independent review</h2><p>Verify the original evidence and assumptions. Approval acknowledges the exact version and every listed gap; it does not authorize a purchase.</p><form onSubmit={async e => { e.preventDefault(); const f = new FormData(e.currentTarget); await post(`reports/${report.id}/review`, { decision: f.get("decision"), rationale: f.get("rationale"), exceptions: exceptionsAccepted ? report.gaps : [] }); }}><label>Decision<select name="decision"><option value="reject">Return for correction</option><option value="approve">Approve this report version</option></select></label><label>Review rationale<textarea name="rationale" required /></label><label className="check-label"><input type="checkbox" checked={exceptionsAccepted} onChange={e => setExceptionsAccepted(e.target.checked)} />I acknowledge every material gap listed above.</label><button disabled={busy || report.stale} className="button button-primary">Record review</button></form></section>}
        </> : <section className="panel runtime-panel"><h2>No underwriting report yet</h2><p>Evidence can be indexed while financial data and independent confirmations remain incomplete.</p></section>}
      </>}
      {(view === "scaling" || view === "work") && <>
        {owner && <section className="panel runtime-panel"><h2>Propose measurable work</h2><p>Import an initiative with its baseline, owner, cost, evidence, target, stop condition, and rollback. External actions are not executed by this screen.</p><form onSubmit={e => void importJson(e, "initiatives")}><label>Initiative file<input name="file" type="file" accept=".json" required /></label><button disabled={busy} className="button button-primary">Add initiative</button></form></section>}
        {!state.initiatives.length && <p>No initiatives recorded. Establish the baseline before forecasting benefits.</p>}
        {state.initiatives.map(i => <section className="panel runtime-panel" key={i.id}><h2>{i.title} <Status tone="info">{human(i.state)}</Status></h2><p>{i.owner} · {i.metric}: {i.baseline} → {i.target} · Measure by {i.measurement_end}</p><p>Setup {i.setup_cost}; monthly cost {i.monthly_cost}; expected monthly cash benefit {i.monthly_cash_benefit}; hours {i.monthly_hours}.</p><p>Stop: {i.stop_condition}</p><p>Rollback: {i.rollback}</p>{i.observations.map((o: Row, n: number) => <p key={n}>Actual {o.value} as of {o.as_of_date} · {o.source_id}</p>)}<form onSubmit={async e => { e.preventDefault(); const f = new FormData(e.currentTarget); await post(`initiatives/${i.id}/action`, Object.fromEntries(f)); }}><label>Action<select name="action"><option value="observe">Record actual result</option><option value="shadow">Begin shadow test</option>{state.role === "reviewer" && <><option value="pilot">Approve pilot</option><option value="active">Approve active state</option></>}<option value="stopped">Stop</option><option value="closed">Close</option></select></label><label>Actual value<input name="value" type="number" step="any" /></label><label>Evidence source<select name="source_id"><option value="">Select evidence</option>{state.sources.filter(s => !s.superseded).map(s => <option key={s.id} value={s.id}>{s.filename}</option>)}</select></label><label>As of<input name="as_of_date" type="date" /></label><label>Decision rationale<textarea name="rationale" /></label><button disabled={busy} className="button button-secondary">Record action</button></form></section>)}
        {owner && view === "scaling" && <section className="panel runtime-panel"><h2>Model cash and capacity</h2><p>Compare baseline, base, downside, and upside. Duplicate benefit groups and insufficient capacity block the model.</p><form onSubmit={e => void importJson(e, "projections")}><label>Projection input file<input name="file" type="file" accept=".json" required /></label><button disabled={busy} className="button button-primary">Calculate projections</button></form>{projection && <table className="data-table"><thead><tr><th>Period</th><th>Case</th><th>Ending cash</th><th>Funding gap</th></tr></thead><tbody>{projection.map((p, i) => <tr key={i}><td>{p.period}</td><td>{p.scenario}</td><td>{p.ending_cash}</td><td>{p.funding_gap}</td></tr>)}</tbody></table>}</section>}
      </>}
      {view === "integrations" && <>
        {owner && <section className="panel runtime-panel"><h2>Company configuration</h2><form key={state.business.updated_at} onSubmit={async e => { e.preventDefault(); await post("company", Object.fromEntries(new FormData(e.currentTarget))); }}><label>Company name<input name="display_name" defaultValue={state.business.display_name} required /></label><label>Industry<select name="industry" defaultValue={state.business.industry}><option value="unknown">General business</option><option value="construction">Construction / fabrication</option></select></label><label>Optional Google notebook URL<input name="notebook_url" type="url" defaultValue={state.business.notebook_url ?? ""} /></label><button className="button button-primary" disabled={busy}>Save configuration</button></form></section>}
        <section className="panel runtime-panel"><h2>Connections</h2>{Object.entries(state.integration_health).map(([name, status]) => <p key={name}>{human(name)}: <Status tone={status === "healthy" || status === "verified" ? "positive" : "warning"}>{human(String(status))}</Status></p>)}<p>Accounting and banking adapters are not connected. Import their original exports below.</p></section>
        {owner && <section className="panel runtime-panel"><h2>Add original evidence</h2><form onSubmit={e => void upload(e)}><label>Document identity<input name="document_id" pattern="[a-zA-Z0-9][a-zA-Z0-9_-]{0,95}" placeholder="e.g. monthly-ledger" required /></label><p>Reuse this identity for a revised copy; earlier versions are preserved.</p><label>Source type<select name="origin"><option value="primary">Original source document</option><option value="seller_statement">Seller claim</option><option value="external">External research</option><option value="notebook">Notebook-derived analysis</option><option value="businessos">BusinessOS-derived report</option></select></label><label>Source file<input name="file" type="file" accept=".pdf,.xlsx,.docx,.txt,.md,.csv,.json" required /></label><button disabled={busy} className="button button-primary">Index evidence</button></form></section>}
        <section className="panel table-wrap"><table className="data-table"><thead><tr><th>Document</th><th>Version</th><th>Origin</th><th>Extraction</th><th>Retrieved</th><th>Original</th></tr></thead><tbody>{state.sources.map(s => <tr key={s.id}><td><button className="text-link" onClick={async () => { const r = await fetch(`/api/runtime/sources/${s.id}`); const d = await r.json(); r.ok ? setSource(d) : setError(d.error); }}>{s.filename}</button></td><td>{s.version} {s.superseded && "(superseded)"}</td><td>{s.origin}</td><td>{human(s.extraction_status)}</td><td>{new Date(s.retrieved_at).toLocaleDateString()}</td><td><a className="text-link" href={`/api/runtime/sources/${s.id}/download`}>Download</a></td></tr>)}</tbody></table></section>
        <section className="panel runtime-panel"><h2>Notebook companion</h2><p>On-demand research and reviewed report exchange. Notebook answers cannot independently verify financial facts.</p>{state.business.notebook_url ? <a className="text-link" href={state.business.notebook_url} target="_blank" rel="noreferrer">Open company notebook ↗</a> : <p>No notebook configured.</p>}{owner && state.business.notebook_url && <><p><button className="button button-secondary" disabled={busy} onClick={() => void post("notebook/jobs", { action: "read" })}>Request source inventory</button></p><form onSubmit={async e => { e.preventDefault(); const f = new FormData(e.currentTarget); await post("notebook/jobs", { action: "ask", question: f.get("question") }); }}><label>Research question<textarea name="question" required /></label><button disabled={busy} className="button button-secondary">Queue notebook question</button></form><form onSubmit={async e => { e.preventDefault(); await post("notebook/jobs", { action: "publish", report_id: new FormData(e.currentTarget).get("report_id") }); }}><label>Reviewed report to publish<select name="report_id" required><option value="">Select reviewed report</option>{state.reports.filter(r => r.review?.decision === "approve" && !r.stale).map(r => <option key={r.id} value={r.id}>{r.id}</option>)}</select></label><button disabled={busy} className="button button-primary">Queue publication to this notebook</button></form></>}{state.notebook_jobs.map(j => <details key={j.id}><summary>{j.action} · {human(j.status)} · {new Date(j.requested_at).toLocaleString()}</summary><p>{j.result?.answer ?? j.result?.evidence ?? "Awaiting browser worker. No notebook change confirmed."}</p>{j.result?.sources?.map((s: Row, i: number) => <p key={i}>{s.title ?? s.id}</p>)}</details>)}</section>
      </>}
      {source && <section className="panel runtime-panel" aria-label="Evidence detail"><button className="button button-secondary" onClick={() => setSource(null)}>Close evidence</button><h2>{source.filename}</h2><p>SHA-256: <code>{source.sha256}</code> · {source.origin} · {source.verification}</p><div className="source-text">{source.segments.map((s: Row, i: number) => <div key={i}><strong>{s.locator}</strong><pre>{s.text}</pre>{s.formula && <p>Cached workbook value: {display(s.cached_value)}. Recalculate and verify the workbook before relying on formulas.</p>}</div>)}</div></section>}
      {(view === "overview" || view === "work") && <section className="panel runtime-panel"><h2>Audit activity</h2>{state.events.length ? state.events.map((e, i) => <p key={i}><time>{new Date(e.at).toLocaleString()}</time> · {e.actor} · {e.action} · {e.record_id}</p>) : <p>No activity recorded.</p>}</section>}
    </>}
  </div>;
}
