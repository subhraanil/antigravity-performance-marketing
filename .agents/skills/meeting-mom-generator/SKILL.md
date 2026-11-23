---
name: meeting-mom-generator
description: >-
  Extract and synthesize client meeting recordings, Fireflies/Otter transcripts, and rough notes into executive Minutes of Meeting (MOM), structured action matrices, and client email transmittals within 24 hours of call completion.
---

# Client Meeting Minutes of Meeting (MOM) Operating Procedure (SOP)

## 1. Overview & Objective
This SOP establishes an agency-wide, repeatable workflow for capturing, structuring, and distributing high-fidelity Minutes of Meeting (MOM) following all client syncs, weekly pacing reviews, technical audits, and strategy walkthroughs.

The SLA for MOM delivery is **≤ 24 hours** post-meeting conclusion.

---

## 2. Ingestion & Pre-Processing
Whenever a meeting concludes, collect one or more of the following inputs:
- **Transcript Source**: Fireflies.ai URL, Otter.ai export, Zoom AI Companion summary, Google Meet transcript, or raw meeting audio.
- **Meeting Notes**: Rough notes taken during the call by team members.
- **Client Metadata**: Brand name, domain, primary client stakeholders, internal agency team members (Account Lead, Media Buyer, SEO Specialist, Designer).

---

## 3. Four-Stage Synthesis Workflow

```
┌─────────────────────────┐     ┌─────────────────────────┐     ┌─────────────────────────┐     ┌─────────────────────────┐
│ Stage 1: Ingestion &    │ ──> │ Stage 2: Categorization │ ──> │ Stage 3: Decision &     │ ──> │ Stage 4: Dual Routing   │
│ Entity Extraction       │     │ by Workstream           │     │ Action Matrix Extraction│     │ & Client Transmittal    │
└─────────────────────────┘     └─────────────────────────┘     └─────────────────────────┘     └─────────────────────────┘
```

### Stage 1: Ingestion & Entity Extraction
Extract foundational meeting metadata:
- **Client & Domain**: e.g., Label IT Solutions (`labelitsolutions.co.uk`).
- **Date & Call Duration**: Exact timestamp and length.
- **Attendance Roster**: Distinguish clearly between Client Stakeholders and Internal Agency Team members.
- **Recording Archive**: Permanent link to the source audio/video recording.

### Stage 2: Categorization by Strategic Workstream
Never dump unstructured transcript notes. Segment discussions into defined functional pillars:
1. **Paid Media & Acquisition**: Budget pacing, daily caps, CPA/ROAS targets, bid strategy adjustments, channel splits (Search, Shopping, Display, Meta).
2. **SEO & Content Marketing**: Keyword mapping, on-page metadata, technical crawl resolution, content publishing pipeline, backlink velocity.
3. **Tracking & Analytics**: GA4 events, GTM containers, conversion attribution (Purchases, Leads, Add-to-Carts), GMC feeds, Pixel health.
4. **Creative & Brand Assets**: High-res imagery, video cuts, ad banners, PDP visual mockups, copy variations.
5. **Operations, Governance & Contact Routing**: Phone routing, payment gateways, card verifications, CRM handoffs.

### Stage 3: Decision Log & Action Item Matrix Extraction
Filter discussion down into concrete commitments:
- **Binding Decisions**: Irreversible or strategic agreements made on the call (e.g., budget reductions, launch approvals, platform migrations).
- **Consolidated Action Matrix**:
  - `Ref #`: Sequential identifier (e.g., `ACT-01`, `ACT-02`).
  - `Task Description`: Specific, non-ambiguous action.
  - `Owner`: Named individual (never vague "Team" or "Client").
  - `Priority`: `🔴 Urgent` (24–48h), `🟡 High` (3–5 days), `🟢 Medium` (ongoing/standard).
  - `Target Due Date`: Definite date/time (never "ASAP" or "Soon").
  - `Status`: Current state and blocking dependencies.
- **Dependencies & Blockers**: Explicitly identify what client inputs the agency requires to proceed (e.g., product photos, phone numbers, merchant approvals).

### Stage 4: Dual Routing & Client Transmittal
- Deliverable Files:
  - Markdown Report: `C:\Users\test\Videos\Office\reports\{Client}_MOM_{Date}.md`
  - Client Archive: `C:\Users\test\Videos\Office\case-studies\{client-slug}\{Client}_MOM_{Date}.md`
  - Optional Interactive HTML: `C:\Users\test\Videos\Office\reports\{Client}_MOM_{Date}.html`
- **Email Transmittal Draft**: Create a copy-paste ready transmittal email from the Account Lead to the Client Principal summarizing key wins, deliverables needed, and next sync milestones.

---

## 4. Automation CLI Command

Generate standardized MOM documents automatically using the workspace automation tool:

```powershell
python scripts/generate_meeting_mom.py \
  --client "Label IT Solutions" \
  --domain "labelitsolutions.co.uk" \
  --date "2026-11-18" \
  --fireflies-url "https://app.fireflies.ai/view/Weekly-Meeting-Label-It-Solutions-TE::01M75NJ80T3EJZFDHGCXV0Q39D" \
  --notes-file "data/meeting_notes_temp.txt" \
  --lead "Sarnendu Patra" \
  --client-contact "A Allana" \
  --output-dir "reports"
```

---

## 5. Quality Guardrails
1. **Stone vs. Opinion**: Document empirical facts (e.g., "Daily budget capped at £5.00/day") separately from speculative hypotheses (e.g., "Client feels sales will increase on weekends").
2. **Strict Single Owner**: Every action item MUST have exactly one designated individual owner.
3. **No Prohibited Paths**: Outputs MUST strictly be placed in `Office/reports/` and `Office/case-studies/<client>/`. Never output to legacy folders.
