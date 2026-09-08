import { NextRequest, NextResponse } from "next/server";
import { runtimeFetch } from "@/lib/runtime";

export const dynamic = "force-dynamic";

async function forward(request: NextRequest, context: { params: Promise<{ path: string[] }> }) {
  if (process.env.BUSINESSOS_MODE === "demo") return NextResponse.json({ error: "Demo mode cannot access private runtime" }, { status: 403 });
  const { path } = await context.params;
  if (path.some(p => !/^[a-zA-Z0-9_-]+$/.test(p))) return NextResponse.json({ error: "Invalid path" }, { status: 400 });
  if (request.method === "POST") {
    const origin = request.headers.get("origin");
    let sameOrigin = false;
    try {
      const parsed = new URL(origin ?? "");
      sameOrigin = process.env.BUSINESSOS_PUBLIC_ORIGIN
        ? parsed.origin === process.env.BUSINESSOS_PUBLIC_ORIGIN
        : ["http:", "https:"].includes(parsed.protocol) && parsed.host === request.headers.get("host");
    } catch { /* Missing or malformed Origin is rejected. */ }
    if (!sameOrigin) return NextResponse.json({ error: "Same-origin request required" }, { status: 403 });
    if (Number(request.headers.get("content-length") ?? 0) > 52 * 1024 * 1024) return NextResponse.json({ error: "File too large" }, { status: 413 });
  }
  try {
    const body = request.method === "POST" ? await request.text() : undefined;
    if (body && Buffer.byteLength(body) > 52 * 1024 * 1024) return NextResponse.json({ error: "File too large" }, { status: 413 });
    const response = await runtimeFetch("/" + path.join("/"), { method: request.method, body });
    const headers = new Headers({ "Content-Type": response.headers.get("content-type") ?? "application/json", "Cache-Control": "no-store", "X-Content-Type-Options": "nosniff" });
    const disposition = response.headers.get("content-disposition");
    if (disposition) headers.set("Content-Disposition", disposition);
    return new NextResponse(await response.arrayBuffer(), { status: response.status, headers });
  } catch {
    return NextResponse.json({ error: "Runtime unavailable. No operation has been confirmed; refresh before retrying." }, { status: 503 });
  }
}
export const GET = forward;
export const POST = forward;
