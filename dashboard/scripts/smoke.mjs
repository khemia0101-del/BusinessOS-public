import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { once } from "node:events";
import { createServer } from "node:net";
import { fileURLToPath } from "node:url";
import { setTimeout as delay } from "node:timers/promises";

const root = fileURLToPath(new URL("../", import.meta.url));
const serverPath = fileURLToPath(new URL("../.next/standalone/server.js", import.meta.url));
const routes = ["/", "/underwriting", "/scaling", "/work", "/integrations", "/components"];

async function freePort() {
  const probe = createServer();
  probe.listen(0, "127.0.0.1");
  await once(probe, "listening");
  const port = probe.address().port;
  await new Promise((resolve, reject) => probe.close((error) => error ? reject(error) : resolve()));
  return port;
}

async function check(configuredStage, expectedStage, checkPages) {
  const port = await freePort();
  const origin = `http://127.0.0.1:${port}`;
  const child = spawn(process.execPath, [serverPath], {
    cwd: root,
    env: { ...process.env, HOSTNAME: "127.0.0.1", PORT: String(port), BUSINESS_STAGE: configuredStage, BUSINESSOS_INSTANCE_ID: "smoke-test" },
    stdio: ["ignore", "pipe", "pipe"],
    windowsHide: true,
  });
  let output = "";
  child.stdout.on("data", (chunk) => { output = (output + chunk).slice(-12000); });
  child.stderr.on("data", (chunk) => { output = (output + chunk).slice(-12000); });
  const exited = once(child, "exit");
  const get = (path) => fetch(`${origin}${path}`, { signal: AbortSignal.timeout(3000) });
  try {
    let healthy = false;
    const deadline = Date.now() + 30000;
    while (Date.now() < deadline) {
      if (child.exitCode !== null) throw new Error(`Standalone server exited: ${output}`);
      try {
        const response = await get("/api/health");
        if (response.ok) { healthy = true; break; }
      } catch { /* Wait only for local server startup. */ }
      await delay(100);
    }
    assert.ok(healthy, `Health endpoint did not become ready: ${output}`);
    const health = await (await get("/api/health")).json();
    assert.equal(health.instance, "smoke-test");
    assert.equal(health.stage, expectedStage);
    if (checkPages) {
      const assets = new Set();
      for (const route of routes) {
        const response = await get(route);
        assert.equal(response.status, 200, route);
        const html = await response.text();
        assert.match(html, /Illustrative/, `Sample data must be labeled on ${route}`);
        for (const match of html.matchAll(/(?:src|href)="([^"\s]*\/_next\/static\/[^"\s]+)"/g)) {
          assets.add(match[1].replaceAll("&amp;", "&"));
        }
      }
      assert.ok(assets.size > 0, "Pages must reference the packaged static assets");
      for (const asset of assets) {
        const response = await get(asset);
        assert.equal(response.status, 200, `Missing standalone asset ${asset}`);
        assert.match(response.headers.get("content-type") ?? "", /(?:javascript|css|font|woff|image)/);
        await response.arrayBuffer();
      }
      assert.equal((await get("/does-not-exist")).status, 404);
      console.log(`Passed ${routes.length} pages, ${assets.size} static assets, health, and 404 checks.`);
    }
    console.log(`Stage ${JSON.stringify(configuredStage)} resolves to ${expectedStage}.`);
  } finally {
    if (child.exitCode === null) child.kill();
    await exited;
  }
}

await check("pre_acquisition", "pre_acquisition", true);
await check("transition", "transition", false);
await check("operating", "operating", false);
await check("post_acquisition", "pre_acquisition", false);
