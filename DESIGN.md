---
name: BusinessOS
description: A calm operating desk that turns business evidence into clear decisions.
colors:
  operating-blue: "#155eef"
  operating-blue-hover: "#0f4fce"
  canvas-gray: "#f6f7f9"
  paper-white: "#ffffff"
  quiet-surface: "#f8f9fb"
  ink-black: "#12151a"
  working-gray: "#5b6471"
  divider-gray: "#dfe3e8"
  healthy-green: "#11643b"
  attention-amber: "#7a4f01"
  material-red: "#a11d2f"
typography:
  display:
    fontFamily: "Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
    fontSize: "clamp(25px, 3vw, 34px)"
    fontWeight: 720
    lineHeight: 1.16
    letterSpacing: "-0.032em"
  title:
    fontFamily: "Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
    fontSize: "16px"
    fontWeight: 680
    lineHeight: 1.35
    letterSpacing: "-0.015em"
  body:
    fontFamily: "Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: "Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
    fontSize: "12px"
    fontWeight: 650
    lineHeight: 1.4
rounded:
  small: "8px"
  surface: "12px"
  pill: "999px"
spacing:
  tight: "8px"
  control: "14px"
  surface: "18px"
  section: "28px"
  page: "38px"
components:
  button-primary:
    backgroundColor: "{colors.operating-blue}"
    textColor: "{colors.paper-white}"
    typography: "{typography.label}"
    rounded: "{rounded.small}"
    padding: "0 14px"
    height: "38px"
  button-secondary:
    backgroundColor: "{colors.paper-white}"
    textColor: "{colors.ink-black}"
    typography: "{typography.label}"
    rounded: "{rounded.small}"
    padding: "0 14px"
    height: "38px"
  status-chip:
    typography: "{typography.label}"
    rounded: "{rounded.pill}"
    padding: "0 8px"
    height: "23px"
  panel:
    backgroundColor: "{colors.paper-white}"
    textColor: "{colors.ink-black}"
    rounded: "{rounded.surface}"
    padding: "18px"
---

# Design System: BusinessOS

## Overview

**Creative North Star: "The Operating Desk"**

BusinessOS feels like a well-run operating review that has already been prepared for the owner: calm, exact, and immediately useful. It is not an agent playground or developer console. The interface leads with business condition and decisions while keeping evidence and technical detail close enough to inspect.

The density is compact but never cryptic. White space separates decisions, not decoration. Tables, timelines, and structured lists carry the work because the product is used during diligence, daily check-ins, and management reviews.

**Key Characteristics:**

- White, crisp, and operational
- Plain language before technical detail
- Dense lists and tables instead of a wall of cards
- Status colors reserved for real state and risk
- Business evidence always close to the conclusion

## Colors

The palette is neutral and quiet, with one restrained action blue and semantic colors that earn attention.

### Primary

- **Operating Blue** (#155eef): Primary decisions, focused links, and the single dominant action in a view.
- **Operating Blue Hover** (#0f4fce): Hover state for the primary action only.

### Neutral

- **Canvas Gray** (#f6f7f9): Page canvas behind the working surfaces.
- **Paper White** (#ffffff): Tables, panels, and the main reading surface.
- **Quiet Surface** (#f8f9fb): Table headers and low-emphasis support areas.
- **Ink Black** (#12151a): Primary text and the brand mark.
- **Working Gray** (#5b6471): Explanations, metadata, and secondary labels.
- **Divider Gray** (#dfe3e8): Structure between rows and operating regions.

### Status

- **Healthy Green** (#11643b): A connected, verified, or passed state.
- **Attention Amber** (#7a4f01): A decision, dependency, or review is required.
- **Material Red** (#a11d2f): A material risk, failed control, or blocking gap.

**The Earned Color Rule.** Blue names an action; green, amber, and red name a real state. None of them are decorative.

## Typography

- **Display Font:** Inter with the system sans stack
- **Body Font:** Inter with the system sans stack
- **Label/Mono Font:** System monospace only for environment variable names and code

**Character:** Familiar and direct. Tight headings make the workspace feel deliberate; highly legible body text keeps decisions readable in meetings.

### Hierarchy

- **Display** (720, 25-34px, 1.16): Page titles only.
- **Title** (680, 16px, 1.35): Section headings and strong operating labels.
- **Body** (400, 14px, 1.5): Explanations with a practical maximum measure of 68-72 characters.
- **Label** (650, 12px, 1.4): Controls, metrics, statuses, and table labels.

**The Business Language Rule.** User-facing type says what happened, why it matters, and what is needed. Internal agent vocabulary stays in developer detail.

## Layout

The desktop shell uses a 244px fixed sidebar and a content canvas capped at 1440px. Pages use 38px horizontal padding, 28px section rhythm, and compact 12-18px internal spacing. The owner overview can use an asymmetric main-and-aside layout; detailed operating views favor tables. Below 820px the sidebar becomes a sticky horizontal navigation bar, and below 620px structured grids become one column.

## Elevation & Depth

The system is flat by default. One-pixel dividers, neutral canvas changes, and white working surfaces establish hierarchy. Shadows are not used on resting panels; the focus ring is the only halo-like treatment.

**The Flat Working Surface Rule.** A panel earns a border or a surface change, never a border plus a decorative shadow.

## Shapes

Working surfaces use 12px corners and compact controls use 8px corners. Fully rounded shapes are reserved for status labels. Geometry remains practical and consistent, with no nested-card stacks.

## Components

### Buttons

- **Shape:** Compact rectangle with an 8px radius and 38px height.
- **Primary:** Operating Blue with white text and 14px horizontal padding.
- **Hover / Focus:** Darker blue on hover; a 3px translucent blue focus ring on keyboard focus.
- **Secondary:** White with a strong gray border; quiet gray on hover.
- **Disabled:** Reduced opacity and no implied interactivity.

### Chips

- **Style:** A 23px pill with semantic text and a light tonal background.
- **State:** Used only for health, risk, confidence, and lifecycle state.

### Cards / Containers

- **Corner Style:** 12px.
- **Background:** Paper White or Quiet Surface.
- **Shadow Strategy:** None at rest.
- **Border:** One-pixel Divider Gray.
- **Internal Padding:** Usually 17-18px; dense table rows use 12-15px.

### Navigation

Navigation is a compact list with 38px rows, muted default text, a quiet gray hover, and a darker tonal active state. On mobile it becomes a horizontally scrollable sticky row without forcing icons into limited space.

### Evidence Coverage

Coverage combines a domain label, a neutral horizontal bar, confidence status, and the exact missing evidence. A percentage never appears without the material gap beside it.

### Decision Detail

A decision shows the observed problem, cost, expected impact, proof method, stop condition, rollback, and exact approval scope in one continuous record. The action area clearly states when controls are illustrative or inactive.

## Do's and Don'ts

### Do:

- **Do** lead a page with the current business decision or condition.
- **Do** use tables and structured rows for repeated operational data.
- **Do** label illustrative data visibly and keep claims tied to evidence.
- **Do** expose cost, impact, proof, and rollback before approval.
- **Do** preserve keyboard focus, responsive behavior, and plain-language recovery states.

### Don't:

- **Don't** expose agent, tool-call, or infrastructure language in the owner workflow.
- **Don't** use gradients, glass effects, decorative shadows, or color for atmosphere.
- **Don't** build the page from equal icon-heading-description cards.
- **Don't** use a pill for ordinary buttons, panels, or navigation.
- **Don't** imply an action works when it is only a static prototype.
