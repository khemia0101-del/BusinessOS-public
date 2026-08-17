import type { ReactNode } from "react";
import Link from "next/link";
import { ArrowRight, Info } from "lucide-react";

export type Tone = "neutral" | "positive" | "warning" | "danger" | "info";

export function Status({
  children,
  tone = "neutral",
}: {
  children: ReactNode;
  tone?: Tone;
}) {
  return <span className={`status status-${tone}`}>{children}</span>;
}

export function PageHeading({
  title,
  description,
  action,
}: {
  title: string;
  description: string;
  action?: ReactNode;
}) {
  return (
    <header className="page-heading">
      <div>
        <h1>{title}</h1>
        <p>{description}</p>
      </div>
      {action ? <div className="page-action">{action}</div> : null}
    </header>
  );
}

export function SectionHeading({
  title,
  detail,
  action,
}: {
  title: string;
  detail?: string;
  action?: ReactNode;
}) {
  return (
    <div className="section-heading">
      <div>
        <h2>{title}</h2>
        {detail ? <p>{detail}</p> : null}
      </div>
      {action}
    </div>
  );
}

export function PrimaryLink({
  href,
  children,
}: {
  href: string;
  children: ReactNode;
}) {
  return (
    <Link className="button button-primary" href={href}>
      {children}
      <ArrowRight aria-hidden="true" size={16} />
    </Link>
  );
}

export function SecondaryLink({
  href,
  children,
}: {
  href: string;
  children: ReactNode;
}) {
  return (
    <Link className="button button-secondary" href={href}>
      {children}
    </Link>
  );
}

export function DemoNotice() {
  return (
    <div className="demo-notice" role="note">
      <Info aria-hidden="true" size={16} />
      <span>
        Illustrative workspace. Values show the intended product behavior, not
        live company data.
      </span>
    </div>
  );
}

export function Confidence({ value }: { value: "High" | "Medium" | "Low" }) {
  const tone: Tone =
    value === "High" ? "positive" : value === "Medium" ? "warning" : "danger";
  return <Status tone={tone}>{value} confidence</Status>;
}
