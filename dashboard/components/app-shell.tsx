"use client";

import type { ReactNode } from "react";
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

export function AppShell({ children }: { children: ReactNode }) {
  const pathname = usePathname();

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
          <span className="workspace-name">Harbor Ridge Construction</span>
          <span className="workspace-stage">
            Pre-acquisition · Illustrative
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
            <strong>System ready</strong>
            <span>Last evidence sync 12m ago</span>
          </div>
        </div>
      </aside>
      <main className="main-content">{children}</main>
    </div>
  );
}
