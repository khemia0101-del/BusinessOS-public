import test from "node:test";
import assert from "node:assert/strict";
import { parseNotebook, runNotebookJob } from "./adapter.mjs";
const url = "https://notebook.google.com/notebook/00000000-0000-0000-0000-000000000001";
const state = `0 AXWebArea Notebook, URL: ${url}\n  1 heading Sources\n  2 button ledger.pdf\n  3 pop up button More, ID: source-item-more-button-00000000-0000-0000-0000-000000000002\n  4 text 1 sources`;
test("source title and stable ID remain linked", () => {
  assert.equal(parseNotebook(state, url).sources[0].title, "ledger.pdf");
});
test("partial inventory cannot pass", () => {
  assert.throws(() => parseNotebook(state.replace("1 sources", "2 sources"), url), /incomplete/);
});
test("wrong notebook fails closed", () => { assert.throws(() => parseNotebook(state, "https://example.test"), /identity/); });
test("read uses no mutation", async () => {
  const r = await runNotebookJob({ action: "read", notebook_url: url }, { getAXState: async () => state });
  assert.equal(r.status, "verified");
});
test("publication requires exact host confirmation", async () => {
  const r = await runNotebookJob({ action: "publish", notebook_url: url }, { getAXState: async () => state });
  assert.equal(r.status, "failed");
  assert.match(r.evidence, /confirm/);
});
test("existing publication does not get duplicated", async () => {
  const r = await runNotebookJob({ action: "publish", notebook_url: url, report_id: "r1", content_hash: "a".repeat(64) }, { getAXState: async () => state.replace("ledger.pdf", "BusinessOS r1 aaaaaaaaaaaaaaaa") }, { confirmPublication: true });
  assert.equal(r.status, "uncertain");
});
test("a failed ask submit is uncertain because the write may have happened", async () => {
  const job = { action: "ask", notebook_url: url, question: "What is the answer?" };
  const states = [state + "\n  5 text entry area Query box", state + "\n  5 button Submit"];
  const result = await runNotebookJob(job, {
    getAXState: async () => states.shift(),
    click: async target => { if (target === 6) throw new Error("request failed after submit"); },
    paste: async () => {},
  });
  assert.equal(result.status, "uncertain");
});
test("current pasted-text dialog supports generated source titles and full verification", async () => {
  const job = { action: "publish", notebook_url: url, report_id: "r1", content_hash: "a".repeat(64), content: "Reviewed synthetic report" };
  const pasted = [];
  const added = state.replace("1 sources", "2 sources") + "\n  8 button Generated title\n  9 pop up button More, ID: source-item-more-button-00000000-0000-0000-0000-000000000003";
  const states = [state + "\n  5 button Add source", "5 button Copied text", "6 text entry area Description: Pasted text", "7 button Insert", added, "1 text BusinessOS r1 aaaaaaaaaaaaaaaa\n2 text Reviewed synthetic report"];
  const result = await runNotebookJob(job, { getAXState: async () => states.shift(), click: async () => {}, paste: async value => pasted.push(value) }, { confirmPublication: true });
  assert.equal(result.status, "verified");
  assert.equal(pasted.length, 1);
  assert.equal(result.source_id, "00000000-0000-0000-0000-000000000003");
});
