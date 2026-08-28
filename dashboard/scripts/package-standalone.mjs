import { cpSync, existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { join } from "node:path";

const root = fileURLToPath(new URL("../", import.meta.url));
const standalone = join(root, ".next", "standalone");
if (!existsSync(join(standalone, "server.js"))) {
  throw new Error("Build the Next.js standalone server before packaging assets.");
}
cpSync(join(root, ".next", "static"), join(standalone, ".next", "static"), { recursive: true });
if (existsSync(join(root, "public"))) {
  cpSync(join(root, "public"), join(standalone, "public"), { recursive: true });
}
console.log("Standalone server and browser assets are ready. Run npm start.");
