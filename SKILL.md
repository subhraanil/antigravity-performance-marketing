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
