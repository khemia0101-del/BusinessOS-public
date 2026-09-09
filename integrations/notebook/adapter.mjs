/**
 * On-demand adapter for a CUA-compatible tab (goto/getAXState/paste/click).
 * Browser credentials stay in the user's browser. This module has no cookie,
 * filesystem, network, or hidden Google API access. A trusted host provides tab.
 */
export function parseNotebook(state, expectedUrl) {
  if (!state.includes(expectedUrl)) throw new Error("Notebook identity not confirmed");
  if (/Sign in|Choose an account|Enter your password/.test(state) && !/heading Sources/.test(state)) return { status: "login_required", sources: [] };
  if (!/heading Sources/.test(state)) throw new Error("Notebook Sources panel is unavailable; open it and retry");
  const sources = [];
  const lines = state.split("\n");
  for (let i = 0; i < lines.length; i++) {
    const id = lines[i].match(/source-item-more-button-([a-f0-9-]+)/)?.[1];
    if (!id) continue;
    // The source title is the preceding button, not the following selected checkbox.
    const title = lines.slice(Math.max(0, i - 3), i).reverse().map(l => l.match(/\b\d+ button (.+)$/)?.[1]).find(Boolean);
    if (!title) throw new Error("Source title mapping changed");
    sources.push({ id, title });
  }
  const count = state.match(/\b(\d+) sources\b/)?.[1];
  if (!count || Number(count) !== sources.length) throw new Error("Notebook source inventory is incomplete; no successful sync recorded");
  return { status: "verified", sources };
}

export function element(state, expression) {
  for (const line of state.split("\n")) {
    const match = line.match(/^\s*(\d+) (.+)$/);
    if (match && expression.test(match[2])) return Number(match[1]);
  }
  throw new Error("Expected notebook control is unavailable; UI may have changed");
}

export async function runNotebookJob(job, tab, options = {}) {
  const result = { notebook_url: job.notebook_url, observed_at: new Date().toISOString(), evidence: "", sources: [] };
  let externalWriteAttempted = false;
  try {
    let state = await tab.getAXState({ emit: false, disableDiffing: true });
    if (!state.includes(job.notebook_url)) {
      await tab.goto(job.notebook_url);
      state = await tab.getAXState({ emit: false, disableDiffing: true });
    }
    let inventory = parseNotebook(state, job.notebook_url);
    if (inventory.status === "login_required") return { ...result, status: "login_required", evidence: "Browser login required" };
    result.sources = inventory.sources;
    if (job.action === "read") return { ...result, status: "verified", evidence: `Verified notebook URL and all ${inventory.sources.length} source IDs/titles in the browser.` };
    if (job.action === "ask") {
      // Host must authorize the specific question before this call.
      const query = element(state, /text entry area.*Query box/);
      await tab.click(query);
      await tab.paste(job.question, { format: "text" });
      state = await tab.getAXState({ emit: false, disableDiffing: true });
      // A submit may trigger an external write before its promise rejects. Mark
      // the operation as uncertain before clicking so failures cannot be
      // misreported as a safe, non-mutating failure.
      externalWriteAttempted = true;
      await tab.click(element(state, /^button Submit$/));
      for (let attempt = 0; attempt < 30; attempt++) {
        state = await tab.getAXState({ emit: false, disableDiffing: true });
        const questionAt = state.lastIndexOf(`text ${job.question}`);
        const answerState = questionAt >= 0 ? state.slice(questionAt) : "";
        if (answerState.includes("Copy model response to clipboard") && !answerState.includes("button Stop")) {
          const citations = [...answerState.matchAll(/pop up button (\d+): ([^\n]+)/g)].map(m => ({ reference: m[1], title: m[2] }));
          const text = answerState.split("\n").filter(l => /\btext /.test(l)).map(l => l.replace(/^.*?\btext /, "")).join("\n");
          if (!citations.length) throw new Error("Answer has no captured citations; needs manual review");
          return { ...result, status: "verified", answer: text, citations, evidence: "Completed browser response with source citations; derived analysis only." };
        }
        if (options.onProgress) await options.onProgress(attempt);
      }
      throw new Error("Notebook answer did not finish within the observation budget");
    }
    if (job.action !== "publish") throw new Error("Unsupported action");
    if (!options.confirmPublication) throw new Error("Host must confirm the exact reviewed report and notebook before publishing");
    const title = `BusinessOS ${job.report_id} ${job.content_hash.slice(0, 16)}`;
    if (inventory.sources.some(s => s.title === title)) {
      // A matching title does not prove content identity; reconcile an uncertain upload manually.
      return { ...result, status: "uncertain", evidence: "Matching source already exists; verify its content before marking publication complete." };
    }
    await tab.click(element(state, /^button Add source$/));
    state = await tab.getAXState({ emit: false, disableDiffing: true });
    await tab.click(element(state, /(?:button|link).*Copied text/));
    state = await tab.getAXState({ emit: false, disableDiffing: true });
    // The current personal Notebook dialog has only a Pasted text field.
    // Put the stable identity in the source body; Google may generate its title.
    await tab.click(element(state, /text entry area.*(?:Paste|Text)/));
    await tab.paste(`${title}\n\n${job.content}`, { format: "text" });
    state = await tab.getAXState({ emit: false, disableDiffing: true });
    externalWriteAttempted = true;
    await tab.click(element(state, /^button Insert$/));
    for (let attempt = 0; attempt < 30; attempt++) {
      state = await tab.getAXState({ emit: false, disableDiffing: true });
      inventory = parseNotebook(state, job.notebook_url);
      const previousIds = new Set(result.sources.map(s => s.id));
      const additions = inventory.sources.filter(s => !previousIds.has(s.id));
      if (additions.length > 1) throw new Error("Multiple new sources appeared; reconcile the publication manually");
      const created = additions[0];
      if (created && !/Processing|Uploading/.test(state)) {
        // Open the source and verify the payload text, not just its title.
        const escaped = created.title.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
        await tab.click(element(state, new RegExp(`^button ${escaped}$`)));
        const sourceState = await tab.getAXState({ emit: false, disableDiffing: true });
        const visible = sourceState.split("\n").map(l => l.replace(/^.*?\btext /, "")).join("\n").replace(/\s+/g, " ");
        const paragraphs = [title, ...job.content.split("\n").map(l => l.trim()).filter(Boolean)];
        if (!paragraphs.every(p => visible.includes(p.replace(/\s+/g, " ")))) {
          return { ...result, sources: inventory.sources, status: "uncertain", evidence: "Source was added but full content verification needs review; do not republish." };
        }
        return { ...result, sources: inventory.sources, status: "verified", source_id: created.id,
          content_hash: job.content_hash, processing_complete: true, evidence: "Verified source ID, completed processing, and every published report paragraph in the source view." };
      }
      if (options.onProgress) await options.onProgress(attempt);
    }
    throw new Error("Publication processing did not finish within the observation budget");
  } catch (error) {
    return { ...result, status: externalWriteAttempted ? "uncertain" : "failed", evidence: String(error.message ?? error) };
  }
}
