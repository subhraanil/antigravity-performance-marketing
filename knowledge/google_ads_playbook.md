# Google Ads Architecture & Operational Playbook

## 1. Search Campaigns (Alpha / Beta Model)
- **Search Alpha (Exact Match Winner Pool)**:
  - Bidding: Target CPA or Target ROAS.
  - Match Type: 100% [Exact Match].
  - Setup: Single-intent ad groups with pinned RSA copy.
- **Search Beta (Phrase Match Mining)**:
  - Bidding: Maximize Conversions with CPA cap.
  - Match Type: "Phrase Match".
  - Negative Cross-Pollination: Add all Alpha exact keywords as negative exact to prevent cannibalization.

## 2. Responsive Search Ad (RSA) Copy Strategy
- **Headline 1 (Pinned)**: Exact search intent / keyword match.
- **Headline 2 (Pinned)**: Core benefit, quantifiable metric, or differentiator.
- **Headline 3 (Unpinned)**: Brand name, urgency, or guarantee.
- **Headlines 4–15 (Rotational)**: Social proof, secondary benefits, features, CTAs.
- **Descriptions 1–4**: 90-character problem/solution statements with clear call-to-action.

## 3. Performance Max (PMax) Architecture
- Asset Group segmentation by product category or audience intent.
- Mandatory Account-Level Brand Negative List to keep PMax focused on non-brand discovery.
- Final URL Expansion configured with exclusions for non-converting pages (blog, legal, privacy, careers).
- Audience signals: 1st-party customer match, top 15 high-intent search terms, competitor domains.
