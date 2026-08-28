import { NextResponse } from "next/server";

export const dynamic = "force-dynamic";

export function GET() {
  const configuredStage = process.env.BUSINESS_STAGE;
  const stage = configuredStage && ["pre_acquisition", "transition", "operating"].includes(configuredStage)
    ? configuredStage
    : "pre_acquisition";
  return NextResponse.json({
    ok: true,
    service: "businessos-dashboard",
    instance: process.env.BUSINESSOS_INSTANCE_ID ?? "unconfigured",
    stage,
    timestamp: new Date().toISOString(),
  });
}
