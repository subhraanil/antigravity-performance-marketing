# Meta Ads MCP Forensic Audit Workflow

**Workflow Type**: Automated Multi-Dimensional Account Diagnostics & Opportunity Recovery  
**Engine**: Meta Ads Model Context Protocol (MCP)  
**Assigned Subagents**: `media_buyer`, `analytics_analyst`, `brand_guardian`  

---

## Workflow Overview

This runbook guides Antigravity agents through an end-to-end audit of any Meta Ads account connected via MCP. It automatically detects capital waste, isolates proven buyer demographics, and produces a zero-risk `PAUSED` turnaround campaign.

```
Step 1: Auth & Account Check (ads_get_ad_accounts)
  ↓
Step 2: Opportunity Score & MAPI Guidance (ads_get_opportunity_score)
  ↓
Step 3: Macro Historical Pull (ads_get_ad_entities [level=campaign])
  ↓
Step 4: Micro Breakdowns Triangulation (Age/Gender, Placement, Device, Region)
  ↓
Step 5: Waste Recovery & Demographic Synthesis
  ↓
Step 6: Executable Staging in PAUSED Mode (ads_create_campaign + ad set)
```

---

## Step-by-Step Execution Protocol

### Step 1: Account Identification & Access Validation
```json
{
  "query": "get ad accounts",
  "limit": 10,
  "advertiser_job": "report_measure_or_look_up",
  "client_conversation_id": "{{SESSION_ID}}"
}
```
- Verify `is_ads_mcp_enabled: true` and `is_queryable: true`.
- Confirm local currency (GBP, USD, EUR, INR) to ensure accurate budget scaling.

### Step 2: Algorithmic Health & Best Practice Audit
```json
{
  "ad_account_id": "{{AD_ACCOUNT_ID}}",
  "advertiser_job": "assess_and_optimize_performance",
  "advertiser_request": "Audit account health and opportunity score recommendations",
  "client_conversation_id": "{{SESSION_ID}}"
}
```
- Record **Opportunity Score** (0–100).
- Extract recommendations with `opportunity_score_lift`.
- Filter out recommendations that artificially expand low-quality placements (e.g. forced Audience Network).

### Step 3: Macro Account History Extraction
```json
{
  "ad_account_id": "{{AD_ACCOUNT_ID}}",
  "level": "campaign",
  "date_preset": "maximum",
  "fields": [
    "id", "name", "objective", "effective_status", "daily_budget",
    "amount_spent", "impressions", "reach", "clicks", "link_click",
    "ctr", "cpc", "cpm", "landing_page_view", "omni_add_to_cart",
    "omni_purchase", "omni_purchase_values", "purchase_roas"
  ],
  "sort": "amount_spent_descending",
  "limit": 100,
  "reporting_purpose": ["key_performance"],
  "advertiser_job": "assess_and_optimize_performance",
  "client_conversation_id": "{{SESSION_ID}}"
}
```
- Group spend into **Sales campaigns** vs. **Traffic/Engagement vanity campaigns**.
- Calculate total spent on vanity objectives (e.g. page likes, profile visits) with £0 attributed revenue.

### Step 4: Triangulated Micro Breakdowns

#### Call 4A: Demographic Matrix (Age & Gender)
```json
{
  "ad_account_id": "{{AD_ACCOUNT_ID}}",
  "level": "campaign",
  "object_ids": ["{{TOP_SALES_CAMPAIGN_IDS}}"],
  "breakdowns": ["age", "gender"],
  "fields": ["amount_spent", "impressions", "link_click", "ctr", "cpc", "omni_purchase", "omni_purchase_values", "purchase_roas"],
  "reporting_purpose": ["metric_lookup"],
  "client_conversation_id": "{{SESSION_ID}}"
}
```
- Calculate **Purchase Conversion Rate** (`omni_purchase` / `link_click`).
- Identify cohorts with high CTR (>5%) but 0 purchases (vanity traffic).
- Flag the **Hero Buyer Cohort** (e.g., Women 45–65+).

#### Call 4B: Placement Efficiency Matrix
```json
{
  "ad_account_id": "{{AD_ACCOUNT_ID}}",
  "level": "campaign",
  "object_ids": ["{{TOP_SALES_CAMPAIGN_IDS}}"],
  "breakdowns": ["publisher_platform", "platform_position"],
  "fields": ["amount_spent", "impressions", "link_click", "cpm", "omni_purchase", "omni_purchase_values", "purchase_roas"],
  "reporting_purpose": ["metric_lookup"],
  "client_conversation_id": "{{SESSION_ID}}"
}
```
- Measure **Feed vs. Non-Feed Conversion Ratio**.
- Check Facebook Feed vs. Instagram Feed vs. Reels vs. Audience Network.
- Calculate capital leaked to Audience Network and Reels with < 0.5x ROAS.

#### Call 4C: Hardware & Device Efficiency Matrix
```json
{
  "ad_account_id": "{{AD_ACCOUNT_ID}}",
  "level": "campaign",
  "object_ids": ["{{TOP_SALES_CAMPAIGN_IDS}}"],
  "breakdowns": ["device_platform", "impression_device"],
  "fields": ["amount_spent", "impressions", "link_click", "cpm", "omni_purchase", "omni_purchase_values", "purchase_roas"],
  "reporting_purpose": ["metric_lookup"],
  "client_conversation_id": "{{SESSION_ID}}"
}
```
- Compare iPhone vs Android Smartphone vs iPad vs Desktop.
- Identify tablet/iPad conversion lift among older demographics.
- Verify if Desktop has 0 conversions (standard for impulse mobile e-commerce).

---

## Step 5: Deliverable Generation & Action Blueprint

Synthesize the data into a 3-part deliverable:
1. **The Forensic Profit & Waste Report**:
   - Total waste identified (Reels + Audience Network + Engagement campaigns).
   - Proven conversion demographics (e.g. Women 45–65+).
   - Core converting placements (Facebook Feed & Instagram Feed).
2. **Turnaround Campaign Architecture**:
   - Ready-to-stage campaign and ad set specs.
3. **Execution Payload**:
   - Draft JSON for `ads_create_campaign` and `ads_create_ad_set` in `PAUSED` state.
