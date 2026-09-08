import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { once } from "node:events";
import { mkdtemp, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { createServer } from "node:net";
import { fileURLToPath } from "node:url";
import { randomBytes } from "node:crypto";
import { setTimeout as delay } from "node:timers/promises";

const root = fileURLToPath(new URL("../../", import.meta.url));
const serverPath = fileURLToPath(new URL("../.next/standalone/server.js", import.meta.url));
async function freePort() { const s = createServer(); s.listen(0, "127.0.0.1"); await once(s, "listening"); const p = s.address().port; await new Promise(r => s.close(r)); return p; }
const apiPort = await freePort(), webPort = await freePort(), storage = await mkdtemp(join(tmpdir(), "businessos-live-test-"));
const owner = randomBytes(32).toString("hex"), reviewer = randomBytes(32).toString("hex"), worker = randomBytes(32).toString("hex");
const env = { ...process.env, BUSINESSOS_MODE: "live", BUSINESSOS_INSTANCE_ID: "synthetic-smoke", BUSINESSOS_DATA_DIR: storage, BUSINESSOS_OWNER_TOKEN: owner, BUSINESSOS_REVIEWER_TOKEN: reviewer, BUSINESSOS_WORKER_TOKEN: worker, BUSINESSOS_API_URL: `http://127.0.0.1:${apiPort}`, BUSINESS_STAGE: "pre_acquisition", HOSTNAME: "127.0.0.1", PORT: String(webPort) };
const python = process.env.BUSINESSOS_PYTHON ?? (process.platform === "win32" ? join(root, ".venv/Scripts/python.exe") : "python");
const api = spawn(python, ["-m", "businessos", "serve", "--port", String(apiPort)], { cwd: root, env, windowsHide: true, stdio: ["ignore", "pipe", "pipe"] });
const web = spawn(process.execPath, [serverPath], { cwd: root, env, windowsHide: true, stdio: ["ignore", "pipe", "pipe"] });
let logs = "";
for (const child of [api, web]) { child.stdout.on("data", x => { logs = (logs + x).slice(-5000); }); child.stderr.on("data", x => { logs = (logs + x).slice(-5000); }); }
const apiExit = once(api, "exit"), webExit = once(web, "exit");
const origin = `http://127.0.0.1:${webPort}`;
const auth = "Basic " + Buffer.from("owner:" + owner).toString("base64");
async function request(path, body, authorization = auth, requestOrigin = origin) {
  return fetch(origin + path, { method: body ? "POST" : "GET", headers: { authorization, origin: requestOrigin, "Content-Type": "application/json" }, body: body ? JSON.stringify(body) : undefined, signal: AbortSignal.timeout(10000) });
}
try {
  for (let n = 0; n < 100; n++) {
    try { const r = await request("/api/runtime/snapshot"); if (r.ok) break; } catch {}
    if (n === 99 || api.exitCode !== null || web.exitCode !== null) throw new Error("Servers not ready: " + logs);
    await delay(200);
  }
  assert.equal((await request("/", undefined, "")).status, 401);
  assert.equal((await request("/api/runtime/snapshot", undefined, "")).status, 401);
  assert.equal((await request("/api/runtime/company", { display_name: "Test" }, auth, "https://attacker.test")).status, 403);
  let r = await request("/api/runtime/company", { display_name: "Synthetic Smoke Company", industry: "construction" });
  assert.equal(r.status, 200, await r.text());
  r = await request("/api/runtime/sources", { document_id: "ledger", filename: "ledger.txt", origin: "primary", content_base64: Buffer.from("Synthetic original evidence").toString("base64") });
  assert.equal(r.status, 200);
  const source = await r.json();
  const snapshot = await (await request("/api/runtime/snapshot")).json();
  assert.equal(snapshot.sources.length, 1);
  assert.equal(snapshot.business.display_name, "Synthetic Smoke Company");
  assert.equal(snapshot.integration_health.accounting, "not_connected");
  assert.equal((await request(`/api/runtime/sources/${source.id}/download`)).status, 200);
  const reviewerAuth = "Basic " + Buffer.from("reviewer:" + reviewer).toString("base64");
  assert.equal((await request("/api/runtime/company", { display_name: "Unauthorized change", industry: "unknown" }, reviewerAuth)).status, 403);
  for (const path of ["/", "/underwriting", "/scaling", "/work", "/integrations"]) {
    const response = await request(path); assert.equal(response.status, 200, path);
    const html = await response.text();
    assert.doesNotMatch(html, /Harbor Ridge Construction|43 inquiries|184 files indexed/);
  }
  api.kill(); await apiExit;
  r = await request("/api/runtime/snapshot");
  assert.equal(r.status, 503);
  assert.match((await r.json()).error, /unavailable/);
  console.log("Live authentication, CSRF, upload, persistence, roles, original download, five routes, and backend-failure checks passed.");
} finally {
  if (api.exitCode === null) api.kill();
  if (web.exitCode === null) web.kill();
  await Promise.allSettled([apiExit, webExit]);
  await rm(storage, { recursive: true, force: true });
}
