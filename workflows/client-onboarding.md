# Agency Client Onboarding Runbook (5-Stage Framework)

Standard operating procedure for smoothly onboarding any performance marketing or SEO client from contract signing to campaign launch.

---

## Stage 1: Intake & Stone vs. Opinion Discovery (Days 1–3)
- **Action**: Run the client intake questionnaire.
- **Data Tagging**:
  - **Stone (Empirical Reality)**: Historical 12-month revenue, verified blended CPA, gross margins, return rates, average order value, geographic breakdown.
  - **Opinion (Client Hypothesis)**: "Our target audience loves minimalist packaging", "Competitor X is stealing our customers". Treat as hypotheses for research, not ground truth.
- **Deliverable**: Generated `brands/{client_slug}.json` brand profile card.

---

## Stage 2: Technical Tracking & Compliance Audit (Days 4–7)
- **Tracking Setup**:
  - Verify Meta Pixel + Conversions API (CAPI) with Advanced Matching score > 8.0/10.
  - Verify Google Ads Tag + Enhanced Conversions active.
  - Check GA4 custom event tracking (ViewContent, AddToCart, InitiateCheckout, Purchase, Lead).
- **Compliance Check**:
  - Ensure privacy policy includes cookie consent banner and GDPR/CCPA disclosures.
  - Flag any regulatory claim risks (FTC, FDA, SEBI, UK ASA).

---

## Stage 3: Strategy & Channel Architecture (Days 8–11)
- **Deliverable**: 90-Day Digital Marketing Strategy Proposal ([digital_marketing_proposal_template.md](../templates/digital_marketing_proposal_template.md)).
- **Content**:
  - 70/20/10 Budget allocation across Meta, Google, and Retention.
  - Target CPAs, breakeven ROAS, and monthly milestone targets.
  - 3x3 Creative Testing Matrix (Hooks, Holds, Offers).

---

## Stage 4: Creative & Campaign Staging (Days 12–14)
- **Campaign Creation**:
  - Build campaign structures strictly in **`PAUSED`** status.
  - Apply negative exclusions (30-day purchasers, existing customer lists).
  - Embed full GA4 UTM parameters on all destination URLs.
- **Client Sign-off**: Client and lead strategist conduct pre-flight walkthrough.

---

## Stage 5: Launch & First 14-Day Pacing Check (Days 15–30)
- **Day 1**: Activate campaigns during low-traffic overnight window.
- **Day 3**: Check initial CPM, CTR, and lead/purchase event firing.
- **Day 7**: First weekly performance audit; check for budget overpacing / underpacing.
- **Day 14**: Review first batch of creative tests; graduate winners with ≥ 35 conversions at target CPA to scaled CBO campaigns.
