import type { Metadata } from "next";
import type { ReactNode } from "react";
import { AppShell } from "@/components/app-shell";
import "./globals.css";

export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "BusinessOS",
  description:
    "Evidence, decisions, and controlled execution for one business.",
};

export default function RootLayout({
  children,
}: Readonly<{ children: ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <AppShell demo={process.env.BUSINESSOS_MODE === "demo"}>{children}</AppShell>
      </body>
    </html>
  );
}
