import { NextRequest, NextResponse } from "next/server";
import { timingSafeEqual } from "node:crypto";

function matches(a: string, b: string) {
  const left = Buffer.from(a), right = Buffer.from(b);
  return left.length === right.length && timingSafeEqual(left, right);
}

export function proxy(request: NextRequest) {
  if (process.env.BUSINESSOS_MODE === "demo") return NextResponse.next();
  const owner = process.env.BUSINESSOS_OWNER_TOKEN;
  const reviewer = process.env.BUSINESSOS_REVIEWER_TOKEN;
  if (!owner || owner.length < 24 || !reviewer || reviewer.length < 24 || owner === reviewer) {
    return new NextResponse("BusinessOS authentication is not configured. Configure the private runtime before adding company data.", { status: 503 });
  }
  const authorization = request.headers.get("authorization") ?? "";
  const decoded = authorization.startsWith("Basic ") ? Buffer.from(authorization.slice(6), "base64").toString("utf8") : "";
  const split = decoded.indexOf(":");
  const username = decoded.slice(0, split), password = decoded.slice(split + 1);
  const role = username === "owner" && matches(password, owner) ? "owner" : username === "reviewer" && matches(password, reviewer) ? "reviewer" : null;
  if (!role) return new NextResponse("Sign in with your BusinessOS owner or reviewer account.", { status: 401, headers: { "WWW-Authenticate": 'Basic realm="BusinessOS", charset="UTF-8"', "Cache-Control": "no-store" } });
  const headers = new Headers(request.headers);
  headers.set("x-businessos-role", role);
  return NextResponse.next({ request: { headers } });
}

export const config = { matcher: ["/((?!_next/static|_next/image|favicon.ico|api/health).*)"] };
