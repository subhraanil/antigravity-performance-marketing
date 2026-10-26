---
name: performance-marketing
description: Production-ready performance marketing skill for Meta Ads and Google Ads campaign architecture, 12-part strategy flow, target CPA/ROAS guardrails, budget pacing, and subagent orchestration. Activate when planning, auditing, launching, or scaling paid media campaigns.
---

# Performance Marketing Skill & Operating System

This skill empowers Antigravity with an end-to-end performance marketing engine, integrating the open-source **`digital-marketing-pro`** (v3.33.3) framework, proven paid advertising architectures for Meta and Google Ads, strict safety guardrails, and specialized marketing subagents.

---

## 1. Safety Guardrails & Campaign Constraints

Whenever planning, creating, or editing ad campaigns, the agent **MUST** enforce the following rules:

1. **PAUSED on Creation**: All newly generated campaigns, ad sets, and ads MUST be created in `PAUSED` state. No automated script or agent action may publish live ads or increase spending without human confirmation.
2. **Budget Pacing & Scaling**:
   - Limit budget scaling to maximum **20% increases every 72 hours** per campaign to prevent breaking machine learning optimization windows on Meta and Google Ads.
   - Budget split rule:
     - **70% Core Scaled**: Proven winning creatives, high-performing CBO / PMax campaigns.
     - **20% Testing Sandbox**: Iterative creative, audience, and offer testing (ABO).
     - **10% Moonshot / Exploratory**: New channels, radically novel hooks, emerging AI formats.
3. **Audience Hygiene**: Prospecting campaigns must strictly exclude past 30-day purchasers, active customer lists, and warm retargeting audiences.
4. **Attribution & UTM Taxonomy**: GA4-compliant UTM parameters enforced on all destination URLs (`utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term`).
5. **EU AI Act Article 50 & C2PA**: C2PA provenance metadata and visible AI disclosure clauses required on all synthetic visual/audio assets.

---

## 2. Target CPAs & ROAS Benchmarks

| Industry Vertical | Metric | Target Benchmark | Guardrail / Ceiling |
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

## 3. Platform Architecture

### Meta Ads Architecture
- **[TOF-ASC] Advantage+ Shopping (CBO - 70%)**: Algorithmic broad audience targeting, existing customer budget cap set to 5–10%, 30d purchaser exclusions.
- **[TEST-SANDBOX] Dynamic Creative Testing (ABO - 20%)**: 3 videos/images x 2 copy variations x 2 headlines per ad set. Graduation rule: ≥ 35 purchases at target CPA graduates creative to TOF-ASC.
- **[MOF/BOF] Warm Engagement (ABO - 10%)**: 90d social engagers, 50%+ video viewers, 14d cart abandoners.
- **Creative Blueprint (Hook-Hold-Offer)**: 
  - 0–3s Hook: Visual scroll-stopper.
  - 3–15s Hold: Problem agitation & mechanism.
  - 15–30s Offer: Irresistible proposition & CTA.

### Google Ads Architecture
- **Search Alpha / Beta Model**: Exact match high-intent winner pool (Alpha) paired with phrase query discovery (Beta), enforced with exact negative cross-pollination.
- **Responsive Search Ad (RSA) Copy Strategy**:
  - Headline 1 (Pinned): Exact search intent / keyword match.
  - Headline 2 (Pinned): Core benefit or quantifiable metric.
  - Headline 3 (Unpinned): Brand name, urgency, or guarantee.
  - Headlines 4–15: Rotational proof, secondary benefits, and features.
  - Descriptions 1–4: 90-character problem/solution statements with clear CTA.
- **Performance Max (PMax)**: Asset group segmentation, mandatory account-level brand negative list, final URL expansion exclusions for non-converting pages, first-party customer match signals.

---

## 4. Subagent Delegation Roster

When tackling multi-faceted marketing operations, delegate to specialized subagents:

- **`media_buyer`**: Campaign architecture, bid strategy, budget pacing, platform specs, and PAUSED safety rules.
- **`marketing_strategist`**: 12-Part Strategy Flow, GTM planning, SOSTAC & RACE roadmaps, and Two-Views model.
- **`growth_engineer`**: Product-Led Growth (PLG), viral loops, unit economics (LTV/CAC), and ICE/RICE experiment design.
- **`seo_specialist`**: Google AI Mode, AI Overviews (AEO/GEO), schema markup, and crawlability.
- **`brand_guardian`**: EU AI Act Article 50, C2PA provenance signing, FTC disclosures, and voice integrity.
- **`analytics_analyst`**: Attribution modeling, GA4/GSC reporting, cohort retention, incremental ROAS analysis.

---

## 5. Reference Documentation

For deep-dive procedures, view the files in the `knowledge/` directory:
- [performance_marketing_frameworks.md](knowledge/performance_marketing_frameworks.md): 12-part flow, Two-Views model, Stone vs Opinion.
- [meta_ads_playbook.md](knowledge/meta_ads_playbook.md): Full-funnel account setup, DCT testing, CAPI.
- [google_ads_playbook.md](knowledge/google_ads_playbook.md): Search Alpha/Beta, PMax setup, RSA copywriting.
- [target_cpas_and_benchmarks.md](knowledge/target_cpas_and_benchmarks.md): Vertical metrics and unit economics formulas.
- [compliance_and_governance.md](knowledge/compliance_and_governance.md): EU AI Act Article 50, C2PA signing, privacy.
- [aeo_geo_ai_search_playbook.md](knowledge/aeo_geo_ai_search_playbook.md): Google AI Mode, AI Overviews, Perplexity, RFC 9309 crawler standards.
- [attribution_modeling_and_mmm.md](knowledge/attribution_modeling_and_mmm.md): Modern post-cookie attribution, Google Meridian MMM, Geo-lift testing.
- [retention_and_email_playbook.md](knowledge/retention_and_email_playbook.md): 6 core lifecycle flows, RFM segmentation, churn signals.
- [google_shopping_and_gmc_feed_playbook.md](knowledge/google_shopping_and_gmc_feed_playbook.md): Google Merchant Center TSV/CSV feed specs, variants, and custom labels.
- [search_terms_audit_and_query_mining.md](knowledge/search_terms_audit_and_query_mining.md): 4-tier query classification, negative keyword lists, and CPA reduction.
- [technical_seo_and_screaming_frog_remediation.md](knowledge/technical_seo_and_screaming_frog_remediation.md): Screaming Frog crawl fixes, 4xx/3xx redirect chains, and IndexNow API.
- [advanced_schema_entity_templates.md](knowledge/advanced_schema_entity_templates.md): Production JSON-LD snippets (Organization, Product, FAQPage).
- [webinar_funnel_and_lead_generation_playbook.md](knowledge/webinar_funnel_and_lead_generation_playbook.md): High-ticket and regional language automated webinar funnels, WhatsApp/Email nurture, and show-up rate optimization.

---

## 6. Standard Operating Workflows

Standard operating runbooks available in `workflows/`:
- [engagement-12-part.md](workflows/engagement-12-part.md): Canonical 12-Part Strategy Flow across Four Core Documents.
- [campaign-launch.md](workflows/campaign-launch.md): Zero-defect pre-flight launch checklist.
- [aeo-geo-audit.md](workflows/aeo-geo-audit.md): 5-phase generative AI search visibility audit.
- [competitor-sweep.md](workflows/competitor-sweep.md): Competitor Ad Library, creative reverse-engineering, and backlink gaps.
- [client-onboarding.md](workflows/client-onboarding.md): 5-stage agency client onboarding from intake to launch.
- [continuous-improvement-loop.md](workflows/continuous-improvement-loop.md): Quarterly MER review and channel rebalancing.

---

## 7. Real-World Client Audits & Case Studies

Audited client deliverables, field data, and forensic remediation plans organized by client vertical in `case-studies/`:
- **Amma Alochana** (`case-studies/amma-alochana/`):
  - [automated_webinar_funnel_strategy.md](case-studies/amma-alochana/automated_webinar_funnel_strategy.md): Telugu parenting coaching automated webinar funnel, Meta Ads CPL optimization, and WhatsApp automation.
- **Pet Mode UK** (`case-studies/pet-mode/`):
  - [pet_mode_forensic_audit_and_fixation_plan.md](case-studies/pet-mode/pet_mode_forensic_audit_and_fixation_plan.md): UK pet e-commerce Google Ads forensic audit, feed hygiene, and placement burn elimination.
  - [pet_mode_3month_forecast_report.md](case-studies/pet-mode/pet_mode_3month_forecast_report.md): 90-day conservative, moderate, and aggressive growth financial models.
  - [pet_mode_city_orders_analysis.md](case-studies/pet-mode/pet_mode_city_orders_analysis.md): Geographic density analysis and regional bid adjustments.
  - [pet_mode_search_terms_audit.md](case-studies/pet-mode/pet_mode_search_terms_audit.md): Search query classification and negative keyword sculpting.
  - [pet_mode_turnaround_summary.md](case-studies/pet-mode/pet_mode_turnaround_summary.md): High-level executive turnaround summary.
  - [pet_mode_unit_economics_dashboard.md](case-studies/pet-mode/pet_mode_unit_economics_dashboard.md): LTV/CAC, margin, and contribution analysis.
- **Pajama Village US** (`case-studies/pajama-village/`):
  - [pajama_village_client_strategy_report.md](case-studies/pajama-village/pajama_village_client_strategy_report.md): 66-day Q4 Christmas pajama seasonal DTC scaling architecture.
  - [pajama_village_google_ads_audit_and_christmas_strategy.md](case-studies/pajama-village/pajama_village_google_ads_audit_and_christmas_strategy.md): Pre-holiday account audit, ROAS benchmarks, and scaling roadmap.
  - [pajama_village_locations_and_feed_deepdive.md](case-studies/pajama-village/pajama_village_locations_and_feed_deepdive.md): Merchant Center feed optimization and state-level targeting.
  - [pajama_village_q4_scale_and_retention_plan.md](case-studies/pajama-village/pajama_village_q4_scale_and_retention_plan.md): Cyber 5 scaling, retention funnels, and post-purchase email cadence.
- **Share Samadhan** (`case-studies/share-samadhan/`):
  - [share_samadhan_search_terms_analysis.md](case-studies/share-samadhan/share_samadhan_search_terms_analysis.md): 23-month forensic analysis of 2,780 search queries for high-ticket financial recovery lead generation.
- **Kuri Ethnic Fashion** (`case-studies/kuri/`):
  - [kuri_meta_ads_strategy.md](case-studies/kuri/kuri_meta_ads_strategy.md): Festive season ethnic fashion Meta Ads campaign strategy and copy matrix.
  - [kuri_google_ads_pmax_report.md](case-studies/kuri/kuri_google_ads_pmax_report.md): Performance Max audit and asset group segmentation.
  - [kuri_ad_copy_bank.md](case-studies/kuri/kuri_ad_copy_bank.md): Multi-angle hook and ad copy repository for ethnic apparel.
  - [kuri_negative_keywords_report.md](case-studies/kuri/kuri_negative_keywords_report.md): Irrelevant search term exclusions and brand negative list.
- **SEO & Publishing Remediation** (`case-studies/seo-and-publishing/`):
  - [technical_seo_screaming_frog_remediation.md](case-studies/seo-and-publishing/technical_seo_screaming_frog_remediation.md): Crawl defect remediation plan, 4xx/3xx redirect consolidation, and IndexNow API integration.
  - [schema_markup_implementation_report.md](case-studies/seo-and-publishing/schema_markup_implementation_report.md): Multi-entity JSON-LD graphs for articles, authors, and publisher entities.
  - [category_page_indexing_strategy.md](case-studies/seo-and-publishing/category_page_indexing_strategy.md): Thin taxonomy cleanup, noindex directives, and canonical hierarchy.
  - [gsc_search_performance_optimization.md](case-studies/seo-and-publishing/gsc_search_performance_optimization.md): Google Search Console query mining and CTR optimization.
  - [wordpress_seo_migration_guide.md](case-studies/seo-and-publishing/wordpress_seo_migration_guide.md): Platform migration risk mitigation and URL mapping.
  - [adsense_rpm_growth_framework.md](case-studies/seo-and-publishing/adsense_rpm_growth_framework.md): Viewability optimization and ad unit placement architecture.
