# Meta Ads Campaign Launch Brief & Creative Matrix

**Client / Brand:** {{brand_name}}  
**Campaign Objective:** Sales (Conversions / Purchase)  
**Creation Status:** PAUSED (Safety Mandate Enforced)  
**Target Monthly Budget:** {{monthly_budget}} (Daily: ${{daily_budget}})  

---

## 1. Campaign & Ad Set Structure

### 1. [TOF-ASC] Advantage+ Shopping Campaign (CBO)
- **Budget**: 70% of total spend (${{asc_daily_budget}}/day).
- **Targeting**: Broad (Age: {{min_age}}-{{max_age}}, Location: {{target_country}}).
- **Existing Customer Budget Cap**: 5% maximum.
- **Negative Exclusions**: Custom Audience: 30-day Purchasers & Customer Email List.

### 2. [TEST-ABO] Dynamic Creative Testing Sandbox
- **Budget**: 20% of total spend (${{test_daily_budget}}/day).
- **Ad Set Structure**: DCT enabled (3 Creatives x 2 Primary Texts x 2 Headlines).
- **Graduation Rule**: CPA ≤ ${{target_cpa}} with ≥ 35 purchases graduates into the main ASC campaign.

---

## 2. 3x3 Creative Matrix (Hook-Hold-Offer)

| Creative Asset | 0–3s Hook (Visual + Text) | 3–15s Hold (Mechanism / Demo) | 15–30s Offer & CTA |
| :--- | :--- | :--- | :--- |
| **Video 1 (UGC Review)** | "Stop taking generic vitamins until you see this lab test." | Influencer unpacks pure ingredients, shows absorption difference. | 25% off Starter Bundle + Free UK Delivery. Button: [Shop Now] |
| **Video 2 (Founder Demo)** | "Why 87% of people waste money on low-grade collagen." | Founder explains bioavailable peptide size under microscope. | 60-day risk-free money-back guarantee. Button: [Learn More] |
| **Video 3 (Before / After)** | "My skin and joints after 30 days of clean nutrition." | Split screen day 1 vs day 30 with customer testimonial quote. | Limited time bundle with complimentary shaker. Button: [Claim Offer] |

---

## 3. Copy & Headline Variations

### Primary Text Options:
1. **Option A (Educational/Proof)**: "Most supplements use synthetic fillers that pass right through you. {{brand_name}} uses clinically verified, 100% bioavailable ingredients tested by independent UK labs. Experience real energy and radiance."
2. **Option B (Social Proof/Review)**: "'I was skeptical, but my joint stiffness disappeared in 3 weeks.' Join over 45,000 customers who made the switch to clean wellness."

### Headlines (Under 35 Characters):
1. "Clean, Lab-Verified Nutrition"
2. "25% Off Your First Order"
3. "Try It Risk-Free For 60 Days"

---

## 4. UTM & Tracking Checklist

- **Destination URL**: `https://{{domain}}/products/starter-bundle?utm_source=meta&utm_medium=paid_social&utm_campaign={{campaign.name}}&utm_content={{ad.name}}&utm_term={{adset.name}}`
- **CAPI & Pixel Event**: Verified `Purchase` event active with Advanced Matching enabled.
- **EU AI Act / C2PA**: C2PA provenance metadata verified on video exports.
