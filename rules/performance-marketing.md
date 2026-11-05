---
trigger: always_on
description: Performance marketing rules for campaign constraints, target CPAs, workspace routing, and Meta/Google Ads templates
---

# Performance Marketing Rules & Guardrails

## 1. Safety & Execution Mandates
- **Always PAUSED on creation**: New campaigns, ad sets, and ads must never be created active. Manual review is required.
- **Budget Scaling Rule**: Never increase daily spend by more than 20% in a 72-hour window.
- **Negative Exclusions**: Prospecting campaigns must exclude past 30-day purchasers and customer match lists.
- **UTM Standard**: GA4 standard parameters required on all destination URLs (`utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term`).
- **EU AI Act Article 50**: C2PA metadata required for AI creative assets; synthetic persona disclosure clause required.

## 2. Benchmark CPAs & ROAS Targets
- **E-Commerce DTC**: Target CPA \$22–\$42, Blended ROAS 3.2x–4.5x, Breakeven ROAS 2.0x.
- **B2B SaaS**: Trial CPA \$35–\$75, PQL CPA \$110–\$240, Blended CAC \$450–\$950, Payback < 10 months.
- **Lead Generation**: Target CPL \$65–\$160, Target SQL \$350–\$850.
- **Local Services**: Cost Per Booking \$28–\$58.

## 3. Platform Architecture
- **Meta Ads**: Advantage+ Shopping (ASC / CBO 70%), Creative Testing Sandbox (ABO 20%), MOF/BOF Retargeting (10%), DPA Catalog.
- **Google Ads**: Search Alpha/Beta (Exact Winner / Phrase Discovery), Performance Max with account brand negative list and first-party customer match, Demand Gen Video Action.

## 4. Subagent Roster
- `media_buyer`: Ad platform bidding, budget pacing, creative specs, optimization.
- `marketing_strategist`: 12-Part Strategy Flow, high-level roadmaps, SOSTAC & RACE.
- `growth_engineer`: PLG, viral loops, activation funnels, unit economics (LTV/CAC).
- `seo_specialist`: Technical SEO, AEO/GEO (Google AI Mode, Perplexity), schema.
- `analytics_analyst`: Attribution, MMM, GA4/GSC reporting, incrementality.
- `brand_guardian`: Compliance, C2PA, EU AI Act Article 50, claims validation.

## 5. Workspace Directory Taxonomy & Report Output Routing
When loading input data, generating audits, executing scripts, or exporting deliverables, strictly observe workspace routing:
- **Office Workspace** (`C:\Users\test\Videos\Office` — formerly `TE-AI Agent`):
  - **Scope**: Agency deliverables, client account data, enterprise audits, Pet Mode, IAOL, IHLS, RACube, Kuri, Share Samadhan.
  - **Outputs**: Save all client audit outputs and reports to `Office/reports/` or `Office/case-studies/<client>/`.
- **Personal Workspace** (`C:\Users\test\Videos\Personal` — formerly `MY-AI Agent`):
  - **Scope**: Owned digital publishing, PaidMediaWorld, personal blogs, internal marketing calculator tools, portfolio assets.
  - **Outputs**: Save all owned media audits and outputs to `Personal/reports/` or `Personal/case-studies/`.
- **Research Workspace** (`C:\Users\test\Videos\Research` — formerly `Freelance-AI` / `Freelance`):
  - **Scope**: Market intelligence, competitor scraping, algorithmic benchmarking, R&D experiments, new venture audits.
  - **Outputs**: Save all exploratory intelligence to `Research/reports/` or `Research/case-studies/`.
- **Mandate**: NEVER reference, create, or output files to legacy paths `TE-AI Agent`, `MY-AI Agent`, or `Freelance-AI`. All paths must resolve dynamically to the active workspace root.
