# Webinar Funnel Reporting & Proposal Playbook
**Standard Origin:** Amma Alochana Trading Academy Client Deliverable (2026)

This playbook establishes the standard format, visual styling, KPI taxonomy, and workflow architecture for client-facing performance marketing proposals and webinar acquisition funnels.

---

## 1. Executive Framing & Scope Discipline
1. **The Lead Thesis**: Always begin Section 1 with the direct partnership contract:
   *"We build and run the system that fills your [Offer/Event]. You teach and enrol; we deliver the audience."*
2. **Accountability Separation**:
   - **Marketing Scope (Agency KPIs)**:
     - Cost Per Lead (CPL)
     - Total Registered Leads
     - Live Webinar Attendees (joined in Zoom/livestream)
     - Calendar Add Rate & Multi-touchpoint Reminder Delivery
   - **Client Responsibility**:
     - Live masterclass delivery & presentation
     - Pitch & offer conversion
     - Post-webinar 1-on-1 counseling calls & sales closing
3. **Measurement Source of Truth**:
   Include a 3-column verification table establishing the exact attribution source (e.g. Meta/Google Ad Manager, CRM tags, Zoom attendee report).

---

## 2. Six-Part Document Architecture
- **Part 1 — Summary**: Executive thesis, 4-metric grid, scope callout, and KPI measurement table.
- **Part 2 — Automated Workflow**: 8-step numbered visual cards with channel tags (`Meta · Google`, `Mobile page`, `CRM`, `WhatsApp · Email`, `Calendar`, `Zoom`, `Post-event`).
- **Part 3 — Projections & Funnel Math**:
  - Comparison table (Month 1 Pilot vs Month 2 Scale).
  - Explicit `<span class="tag">KPI</span>` badges on guaranteed marketing deliverables.
  - Derived rows in italics (implied lead-to-attendee rate, implied cost per live attendee).
  - Pure CSS horizontal funnel visualization (Leads &rarr; Calendar Sync &rarr; Live Attendees).
  - Decision rules: `Scale up if...`, `Hold and fix if...`, `How we scale`.
- **Part 4 — Video Production Brief & Scripts**:
  - Clear roles (Client records raw 9:16 vertical smartphone footage; Agency edits, captions, and launches).
  - Time-stamped script templates with embedded Base64 fonts for native regional scripts (Telugu, Hindi, etc.) + English translations.
- **Part 5 — Launch Plan & Requirements**:
  - 4-phase launch timeline (Days 1–3, 3–6, 4–7, Day 7+).
  - Client prerequisites list (Admin access, raw video, syllabus PDF, webinar link).
  - Vertical-specific compliance warning (SEBI, FTC, financial claims).
- **Part 6 — Commercial Terms & Next Steps**:
  - Client-provided costs box (Ad spend, CRM subscription, custom domain, WhatsApp API, Zoom).
  - 2 pricing components: One-time setup fee + Monthly maintenance retainer.
  - 3-step Next Steps gradient block.

---

## 3. Technical & Styling Requirements
- **Color Palette**: Deep Teal (`#0f766e`), Mint (`#ccfbf1`), Slate Dark (`#0f172a`), Ocean Blue (`#0284c7`), Soft Grey (`#f8fafc`).
- **Self-Contained Fonts**: Embed Base64 WOFF2 strings directly into `@font-face` for non-Latin scripts to eliminate external HTTP dependencies and guarantee identical rendering across all PDF engines.
- **Print Pagination**: Use `@media print` with `@page { size: A4; margin: 12mm; }`, `break-inside: avoid;`, and `break-after: avoid;` to produce zero orphaned table rows or broken cards.
