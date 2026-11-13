# Performance Marketing Operating System (Global Rules)

This workspace is configured with the **Performance Marketing Operating System**, integrating the open-source [digital-marketing-pro](https://github.com/indranilbanerjee/digital-marketing-pro) framework, 24 specialized marketing subagents, 25 operational playbooks, 28 workflow SOPs, and 110 automation scripts.

## 1. Master Project Workspace Hierarchy & Output Routing
Always route all data reading, script execution, audits, and report generation into one of the three primary project directories:

- **Office Workspace** (`C:\Users\test\Videos\Office`):
  - **Scope**: Agency deliverables, client account data, enterprise proposals, client audits (e.g. Pet Mode, IAOL, IHLS, RACube, StoriAI, Kuri, Share Samadhan).
  - **Deliverable Outputs**: MUST be written to `C:\Users\test\Videos\Office\reports\` and `C:\Users\test\Videos\Office\case-studies\<client>\`.
- **Personal Workspace** (`C:\Users\test\Videos\Personal`):
  - **Scope**: Owned digital media, PaidMediaWorld, personal blogs, marketing calculators, tools development, portfolio assets.
  - **Deliverable Outputs**: MUST be written to `C:\Users\test\Videos\Personal\reports\` and `C:\Users\test\Videos\Personal\case-studies\`.
- **Research Workspace** (`C:\Users\test\Videos\Research`):
  - **Scope**: Market intelligence, competitor scraping, algorithmic benchmarking, R&D experiments, new venture audits (e.g. Pajama Village, Amma Alochana).
  - **Deliverable Outputs**: MUST be written to `C:\Users\test\Videos\Research\reports\` and `C:\Users\test\Videos\Research\case-studies\`.
- **Strict Guardrail**: NEVER output or write files to legacy directories `TE-AI Agent`, `MY-AI Agent`, `Freelancing-AI`, or `Freelance-AI`. All paths must resolve to the active project folder.

## 2. Key Campaign Constraints & Guardrails
1. **Safety Creation Gate**: All campaigns, ad sets, and ads are generated in `PAUSED` status.
2. **Budget Pacing**: Scaling is capped at ≤ 20% increases every 72 hours per campaign.
3. **Audience Hygiene**: Strict negative exclusions for past 30-day purchasers and customer lists.
4. **Compliance**: EU AI Act Article 50 disclosures and C2PA provenance required on AI assets.
5. **UTM Standard**: GA4 standard parameters required on all destination URLs (`utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term`).

## 3. Target CPAs & Benchmarks
- **DTC E-Commerce**: CPA \$22–\$42, ROAS 3.2x–4.5x, Breakeven ROAS 2.0x
- **B2B SaaS**: Trial CPA \$35–\$75, PQL \$110–\$240, CAC \$450–\$950, CAC Payback < 10 months
- **Lead Gen**: CPL \$65–\$160, SQL \$350–\$850, Lead-to-SQL Rate ≥ 15%
- **Local Services**: Cost Per Call / Booking \$28–\$58, Booking Rate ≥ 25%

## 4. Subagent Architecture (24 Specialists)
Delegations are automatically handled via dedicated specialist subagents:
- `media_buyer`: Meta Ads, Google Ads, bid strategies, pacing, and execution.
- `marketing_strategist`: 12-Part Strategy Flow, GTM planning, and positioning.
- `growth_engineer`: PLG, loops, activation funnels, and unit economics.
- `seo_specialist`: Technical SEO, OpenSEO, AEO/GEO (Google AI Mode), schema.
- `analytics_analyst`: Attribution, reporting, and incrementality.
- `brand_guardian`: Compliance, C2PA, and EU AI Act Article 50.
- `local_coder`: Fast offline code generation via local `qwen2.5-coder:1.5b`.
