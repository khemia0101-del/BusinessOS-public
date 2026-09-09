"use client";

import type { ReactNode } from "react";
import { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Blocks,
  Cable,
  ChartNoAxesCombined,
  ClipboardCheck,
  Gauge,
  PanelLeftClose,
} from "lucide-react";

const navigation = [
  { href: "/", label: "Overview", icon: Gauge },
  { href: "/underwriting", label: "Underwriting", icon: ClipboardCheck },
  { href: "/scaling", label: "Scaling plan", icon: ChartNoAxesCombined },
  { href: "/work", label: "Work & decisions", icon: Blocks },
  { href: "/integrations", label: "Integrations", icon: Cable },
];

function isActive(pathname: string, href: string) {
  return href === "/" ? pathname === href : pathname.startsWith(href);
}

export function AppShell({ children, demo = false }: { children: ReactNode; demo?: boolean }) {
  const pathname = usePathname();
  const [company, setCompany] = useState("Private company workspace");
  const [stage, setStage] = useState("Awaiting runtime");
  const [lastRefresh, setLastRefresh] = useState("No evidence refresh confirmed");
  useEffect(() => {
    const listener = (event: Event) => {
      const data = (event as CustomEvent).detail;
      setCompany(data.business.display_name);
      setStage(data.stage.replaceAll("_", " "));
      setLastRefresh(`Workspace refreshed ${new Date(data.generated_at).toLocaleTimeString()}`);
    };
    window.addEventListener("businessos-status", listener);
    return () => window.removeEventListener("businessos-status", listener);
  }, []);

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-row">
          <Link className="brand" href="/" aria-label="BusinessOS overview">
            <span className="brand-mark">B</span>
            <span>BusinessOS</span>
          </Link>
          <PanelLeftClose
            aria-hidden="true"
            className="sidebar-cue"
            size={17}
          />
        </div>

        <div className="workspace-summary">
          <span className="workspace-name">{demo ? "Harbor Ridge Construction" : company}</span>
          <span className="workspace-stage">
            {demo ? "Pre-acquisition · Illustrative" : stage}
          </span>
        </div>

        <nav className="primary-nav" aria-label="Business workspace">
          {navigation.map((item) => {
            const Icon = item.icon;
            return (
              <Link
                aria-current={
                  isActive(pathname, item.href) ? "page" : undefined
                }
                className="nav-link"
                href={item.href}
                key={item.href}
              >
                <Icon aria-hidden="true" size={17} strokeWidth={1.8} />
                <span>{item.label}</span>
              </Link>
            );
          })}
        </nav>

        <div className="sidebar-footer">
          <span className="system-dot" aria-hidden="true" />
          <div>
            <strong>{demo ? "Illustrative workspace" : "Evidence workspace"}</strong>
            <span>{demo ? "Sample data only" : lastRefresh}</span>
          </div>
        </div>
      </aside>
      <main className="main-content">{children}</main>
    </div>
  );
}
