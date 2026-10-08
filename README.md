# Antigravity Performance Marketing Operating System

[![Antigravity](https://img.shields.io/badge/Antigravity-2.0-blue.svg)](https://antigravity.google)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Open%20Standard-success.svg)](https://agentskills.io)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![EU AI Act](https://img.shields.io/badge/EU%20AI%20Act-Article%2050%20ready-darkred.svg)](knowledge/compliance_and_governance.md)

Production-ready **Performance Marketing Skill, Knowledge Base, and Subagent Suite** for Google Antigravity. Integrates frameworks from the open-source [digital-marketing-pro](https://github.com/indranilbanerjee/digital-marketing-pro) project with proven full-funnel architectures for Meta Ads, Google Ads, and autonomous marketing operations.

---

## 🚀 How to Use on ANY PC (Quick Install)

You can install this skill and knowledge base onto any PC running Google Antigravity in seconds.

### Option 1: Automatic One-Click Install

#### On Windows (PowerShell):
```powershell
git clone https://github.com/subhraanil/antigravity-performance-marketing.git $HOME\.gemini\config\skills\performance-marketing
powershell -ExecutionPolicy Bypass -File $HOME\.gemini\config\skills\performance-marketing\scripts\install.ps1
```

#### On macOS / Linux (Terminal):
```bash
git clone https://github.com/subhraanil/antigravity-performance-marketing.git ~/.gemini/config/skills/performance-marketing
bash ~/.gemini/config/skills/performance-marketing/scripts/install.sh
```

---

### Option 2: Project-Level Workspace Install

If you want to use this exclusively within a single project repository:
1. Clone or copy this repository into your project root under `.agents/skills/performance-marketing`:
   ```bash
   git clone https://github.com/subhraanil/antigravity-performance-marketing.git .agents/skills/performance-marketing
   ```
2. Copy the rules file to your workspace:
   ```bash
   mkdir -p .antigravity
   cp .agents/skills/performance-marketing/rules/.antigravity-rules .antigravity/rules
   ```

---

## 📦 What's Inside

```
antigravity-performance-marketing/
├── SKILL.md                          # Antigravity Agent Skill specification
├── knowledge/                        # Persistent Domain Knowledge
│   ├── performance_marketing_frameworks.md   # 12-Part Flow, Two-Views Model, Unit Economics
│   ├── meta_ads_playbook.md                 # Advantage+ Shopping, DCT, CAPI, Hook-Hold-Offer
│   ├── google_ads_playbook.md               # Search Alpha/Beta, PMax, RSA Strategy
│   ├── target_cpas_and_benchmarks.md        # CPA/ROAS targets across 4 verticals
│   ├── compliance_and_governance.md         # EU AI Act Article 50, C2PA, signal resilience
│   ├── aeo_geo_ai_search_playbook.md        # Google AI Mode, AI Overviews, Perplexity, RFC 9309
│   ├── attribution_modeling_and_mmm.md      # Post-cookie attribution, Google Meridian MMM, Geo-lift
│   └── retention_and_email_playbook.md      # 6 core lifecycle flows, RFM segmentation, churn signals
├── rules/                            # Workspace & Global Rules
│   ├── .antigravity-rules            # Global workspace constraints (.antigravity/rules)
│   ├── performance-marketing.md      # Standard Antigravity rules format
│   ├── GEMINI.md                     # Global memory and system instructions
│   └── AGENTS.md                     # Universal agent discovery manifest
├── brands/                           # Pre-Configured Brand Context Cards
│   ├── nutrabytes.json               # UK Health & Supplements DTC profile
│   ├── share-samadhan.json           # India Financial Recovery consultancy profile
│   ├── airdog.json                   # Clean air hardware DTC profile
│   └── _template.json                # Master brand onboarding template
├── subagents/                        # 24 Specialist Marketing Subagent definitions
│   ├── media-buyer.md                # Paid advertising, bid pacing, campaign setup
│   ├── marketing-strategist.md       # 12-Part Strategy Flow, GTM planning, SOSTAC
│   ├── growth-engineer.md            # PLG, viral loops, activation, unit economics
│   ├── seo-specialist.md             # Technical SEO, Google AI Mode, AEO/GEO
│   ├── brand-guardian.md             # EU AI Act compliance, C2PA, claims audit
│   └── analytics-analyst.md          # Attribution models, GA4/GSC reporting
├── templates/                        # Production Deliverable Templates & JSONs
│   ├── meta_ads_template.json        # Advantage+ (ASC), Testing Sandbox (ABO), DPA
│   ├── google_ads_template.json      # Search Alpha/Beta, PMax, Pinned RSAs
│   ├── digital_marketing_proposal_template.md    # 90-day strategy proposal with Gantt chart
│   ├── weekly_performance_report_template.md     # Pacing scorecard and creative winners
│   ├── seo_technical_audit_template.md          # Technical SEO & Google AI Mode checklist
│   └── meta_ads_launch_brief_template.md        # 3x3 Hook-Hold-Offer launch brief
├── workflows/                        # Standard Operating Procedures
│   ├── engagement-12-part.md         # Canonical 12-Part Strategy Flow
│   ├── campaign-launch.md            # Zero-defect pre-flight launch checklist
│   ├── aeo-geo-audit.md              # 5-phase generative AI search visibility audit
│   ├── competitor-sweep.md           # Competitor Ad Library, creative reverse-engineering
│   ├── client-onboarding.md          # 5-stage agency client onboarding runbook
│   └── continuous-improvement-loop.md# Quarterly MER review and channel rebalancing
├── scripts/                          # Automated Installers & CLI Utilities
│   ├── install.ps1                   # Windows installer
│   ├── install.sh                    # Unix/Linux/macOS installer
│   ├── brand_manager.py              # Brand profile inspection CLI
│   ├── pacing_calculator.py          # Ad budget pacing & 72h scaling evaluator
│   └── utm_builder.py                # GA4 standard UTM URL builder
└── README.md                         # Documentation
```

---

## 🛡️ Core Safety Guardrails & Campaign Constraints

1. **PAUSED on Creation**: All campaigns, ad sets, and ads MUST be generated in `PAUSED` status. No spend without explicit human strategist confirmation.
2. **Budget Stability**: Budget scaling is capped at a maximum of **20% every 72 hours** per campaign to protect algorithmic learning phases.
3. **70/20/10 Budget Split**:
   - **70% Core Scaled**: Proven winning creatives, high-performing CBO / PMax campaigns.
   - **20% Testing Sandbox**: Iterative creative, audience, and offer testing (ABO).
   - **10% Moonshot / Exploratory**: Radical angles, emerging channels, new formats.
4. **Audience Hygiene**: Prospecting campaigns must strictly exclude past 30-day purchasers, active customer match lists, and warm retargeting pools.
5. **Attribution & UTM Taxonomy**: GA4-compliant UTM parameters enforced on all destination URLs (`utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term`).
6. **EU AI Act Article 50 & C2PA**: C2PA provenance metadata and visible AI disclosure clauses required on all synthetic visual/audio assets.

---

## 🎯 Target CPAs & ROAS Benchmarks

| Industry Vertical | Primary KPI | Benchmark Target | Guardrail / Ceiling |
| :--- | :--- | :--- | :--- |
| **DTC E-Commerce** (Apparel / Beauty / CPG) | Target CPA | \$22.00 – \$42.00 | Max CPA: \$38.00 (First Order) |
| | Target ROAS | 3.2x – 4.5x | Breakeven ROAS: 2.0x |
| | CVR / AOV | CVR: 2.5% – 3.8% | AOV: \$65.00 – \$125.00 |
| **B2B SaaS** (Product-Led / Self-Serve) | Free Trial / Signup | \$35.00 – \$75.00 | Max CPA: \$85.00 |
| | Product Qualified Lead (PQL) | \$110.00 – \$240.00 | Max PQL: \$280.00 |
| | Blended CAC | \$450.00 – \$950.00 | CAC Payback < 10 months |
| | LTV : CAC | 3.5x – 5.0x | Min Ratio: 3.0x |
| **High-Ticket B2B & Lead Generation** | Cost Per Lead (CPL) | \$65.00 – \$160.00 | Max CPL: \$180.00 |
| | Sales Qualified Lead (SQL) | \$350.00 – \$850.00 | Lead-to-SQL Rate ≥ 15% |
| **Local Services & Healthcare** | Cost Per Call / Booking | \$28.00 – \$58.00 | Booking Rate ≥ 25% |

---

## 🤝 Subagent Orchestration Loop

This skill registers specialist subagents into Antigravity:
* **`media_buyer`**: Executes ad account architectures, bid pacing, platform specs, and budget hygiene.
* **`marketing_strategist`**: Guides the 12-Part Strategy Flow, GTM planning, and competitive positioning.
* **`growth_engineer`**: Architects product-led growth loops, referral systems, and unit economics models.
* **`seo_specialist`**: Performs audits for Google AI Mode, AI Overviews, schema, and organic visibility.
* **`brand_guardian`**: Ensures regulatory compliance, FTC disclosures, C2PA signing, and brand voice adherence.
* **`analytics_analyst`**: Evaluates attribution models, cohort retention, and incrementality tests.

---

## 📄 License

MIT License. Free to use, adapt, and scale across personal and commercial client portfolios.
