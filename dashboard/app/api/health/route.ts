import { NextResponse } from "next/server";

export const dynamic = "force-dynamic";

export function GET() {
  return NextResponse.json({
    ok: true,
    service: "businessos-dashboard",
    instance: process.env.BUSINESSOS_INSTANCE_ID ?? "unconfigured",
    stage: process.env.BUSINESS_STAGE ?? "pre_acquisition",
    timestamp: new Date().toISOString(),
  });
}
