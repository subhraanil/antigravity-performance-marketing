# Google Ads Architecture & Operational Playbook
# Integrates Search Alpha/Beta, PMax, GMC Shopping & Search Terms Forensic Mining

This playbook establishes the operating standard for Google Ads campaign architecture, bidding strategies, shopping feed hygiene, and forensic search query mining.

---

## 1. Search Campaigns (Alpha / Beta Model)

```
+-----------------------------------------------------------------------------+
|                          SEARCH ALPHA / BETA MODEL                          |
+-----------------------------------------------------------------------------+
| Search Alpha (Exact Match Winner Pool):                                     |
|   - Bidding: Target CPA or Target ROAS                                      |
|   - Match Type: 100% [Exact Match]                                          |
|   - Setup: Single-Intent Ad Groups (SIAGs) with pinned RSA copy             |
+-----------------------------------------------------------------------------+
| Search Beta (Phrase Match Query Mining):                                    |
|   - Bidding: Maximize Conversions with CPA cap                              |
|   - Match Type: "Phrase Match"                                              |
|   - Negative Cross-Pollination: Add all Alpha exact keywords as negative    |
|     exact in Beta to prevent cannibalization and route traffic cleanly      |
+-----------------------------------------------------------------------------+
```

---

## 2. Responsive Search Ad (RSA) Copy Strategy

- **Headline 1 (Pinned)**: Exact search intent / keyword match.
- **Headline 2 (Pinned)**: Core benefit, quantifiable metric, or primary differentiator.
- **Headline 3 (Unpinned)**: Brand name, urgency, or risk reversal guarantee.
- **Headlines 4–15 (Rotational)**: Social proof, secondary benefits, certifications, CTAs.
- **Descriptions 1–4**: 90-character problem/solution statements with strong calls-to-action.

---

## 3. Performance Max (PMax) Architecture & Guardrails

- **Asset Group Segmentation**: Segment strictly by product category or distinct customer intent.
- **Account-Level Brand Negative List**: Mandatory to prevent PMax from inflating ROAS on existing brand traffic.
- **Final URL Expansion**: Configured with exclusions for non-converting pages (blogs, legal, privacy, careers, return policies).
- **Audience Signals**: First-party customer match lists, top 15 high-intent search themes, and competitor URL domains.

---

## 4. Shopping & Google Merchant Center (GMC) Hygiene

- **Product Titles**: Structured as `[Brand] + [Product Type] + [Key Attribute / Color / Size] + [Model Number]`.
- **Feed Custom Labels**:
  - `Custom Label 0`: Margin tier (`High-Margin`, `Low-Margin`).
  - `Custom Label 1`: Velocity (`Hero-SKU`, `Slow-Mover`, `Dead-Weight`).
  - `Custom Label 2`: Seasonality (`Core`, `Winter`, `Holiday`).

---

## 5. Search Terms Forensic Audit & Query Mining

### The Core Search Terms Principle
Advertisers do not pay for keywords; they pay for the actual **search terms** triggered by user queries. A high-performing keyword often masks significant budget waste when phrase match allows non-converting query bleeding.

### The 4-Tier Query Classification Framework
```
+-----------------------------------------------------------------------------+
|                     4-TIER QUERY CLASSIFICATION MATRIX                      |
+-----------------------------------------------------------------------------+
| Tier 1: Alpha Winners        --> High CVR, Low CPA. Promote to Exact Match  |
| Tier 2: Beta Discovery       --> Relevant, moderate CTR. Maintain in Phrase |
| Tier 3: Low-Intent Info      --> High clicks, zero conversion. Down-bid/Neg |
| Tier 4: Irrelevant Waste     --> Immediate Negative Exact / Negative Phrase |
+-----------------------------------------------------------------------------+
```

### Zero-Conversion Cutoff Thresholds
- **E-Commerce**: Search terms spending $> 1.5\times$ Target CPA without a purchase are flagged for immediate negative exact exclusion.
- **Lead Gen**: Search terms spending $> 2.0\times$ Target CPL without a form submit or qualified call are added to the negative keyword list.
- **Match-Type Bleeding**: Audit broad and phrase match queries monthly. Queries generating $\ge 5$ conversions graduate to Alpha Exact Match ad groups.
