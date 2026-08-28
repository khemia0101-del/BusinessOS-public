export const evidenceCoverage = [
  {
    domain: "Financial performance",
    coverage: 88,
    confidence: "High",
    gap: "March bank statement",
  },
  {
    domain: "Revenue quality",
    coverage: 61,
    confidence: "Medium",
    gap: "Customer-level job history",
  },
  {
    domain: "Operations",
    coverage: 74,
    confidence: "Medium",
    gap: "Crew capacity by trade",
  },
  {
    domain: "People",
    coverage: 82,
    confidence: "High",
    gap: "Two compensation agreements",
  },
  {
    domain: "Legal & compliance",
    coverage: 56,
    confidence: "Low",
    gap: "License and claims history",
  },
] as const;

export const findings = [
  {
    title: "Leads are tracked in inboxes and spreadsheets",
    detail:
      "No shared pipeline owns follow-up, estimates, or lost-lead reasons. BusinessOS found 43 inquiries with no recorded next step.",
    impact: "Revenue leakage",
    tone: "danger" as const,
  },
  {
    title: "Gross margin changes sharply by job type",
    detail:
      "Small renovation work appears to carry more rework and travel time than the current estimates allow for.",
    impact: "Margin risk",
    tone: "warning" as const,
  },
  {
    title: "The owner is the approval path for daily scheduling",
    detail:
      "Four handoffs depend on one person, adding an estimated 1.6 days between signed estimate and scheduled start.",
    impact: "Capacity constraint",
    tone: "warning" as const,
  },
];

export const initiatives = [
  {
    id: "INIT-014",
    title: "Create one lead-to-estimate pipeline",
    horizon: "First 30 days",
    state: "Needs decision",
    cost: "$1,300 setup · $90/mo",
    impact: "$8k-$18k monthly gross profit",
    proof: "Backtest 18 months of inquiries, then 30-day pilot",
  },
  {
    id: "INIT-009",
    title: "Job-level margin reporting",
    horizon: "First 100 days",
    state: "Being tested",
    cost: "$600 setup · $40/mo",
    impact: "2-4 margin points on affected jobs",
    proof: "Shadow report against closed jobs",
  },
  {
    id: "INIT-021",
    title: "Move schedule approval to crew leads",
    horizon: "First 100 days",
    state: "Researching",
    cost: "12 internal hours",
    impact: "1 day faster scheduling",
    proof: "Historical simulation, then one-crew pilot",
  },
  {
    id: "INIT-026",
    title: "Referral follow-up program",
    horizon: "Months 4-12",
    state: "Found",
    cost: "Not priced",
    impact: "Evidence not sufficient",
    proof: "Measure referral baseline first",
  },
] as const;

export const integrations = [
  {
    name: "Google Drive",
    category: "Documents",
    state: "Healthy",
    detail: "184 files indexed · synced 12m ago",
    env: "GOOGLE_DRIVE_DATA_ROOM_URL",
  },
  {
    name: "QuickBooks",
    category: "Finance",
    state: "Needs attention",
    detail: "Connected · last sync failed",
    env: "QUICKBOOKS_CLIENT_ID",
  },
  {
    name: "Plaid",
    category: "Banking",
    state: "Not configured",
    detail: "Read-only bank activity unavailable",
    env: "PLAID_CLIENT_ID",
  },
  {
    name: "CRM",
    category: "Sales",
    state: "Not in use",
    detail: "BusinessOS identified this as a capability gap",
    env: "CRM_PROVIDER",
  },
  {
    name: "Zoom",
    category: "Meetings",
    state: "Not configured",
    detail: "Meeting transcripts are not available",
    env: "ZOOM_CLIENT_ID",
  },
  {
    name: "Google Analytics",
    category: "Web analytics",
    state: "Healthy",
    detail: "Property data available",
    env: "GA4_PROPERTY_ID",
  },
] as const;
