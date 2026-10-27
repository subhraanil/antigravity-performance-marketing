#!/usr/bin/env python3
"""
Initialize Paid Media World Campaign - Shard 01
Generates customized submission copy and registers the campaign ledger.
"""

import os
import json
import hashlib
from datetime import datetime

def generate_key(domain, product_id):
    return hashlib.sha256(f"{domain.lower()}:{product_id.lower()}".encode("utf-8")).hexdigest()[:12]

# Verified Profile Data
BRAND_NAME = "Paid Media World"
FOUNDER_NAME = "Subhranil Naskar"
FOUNDER_TITLE = "Lead Performance Marketing Specialist & Technical Analytics Architect"
CANONICAL_URL = "https://paidmediaworld.com/"
HQ_LOCATION = "Kolkata, West Bengal, India"
GEO_SERVICED = "Global (United States, United Kingdom, Canada, Australia, India)"

TAGLINE = "Paid Ads That Grow Profit, Not Just Clicks"

SHORT_DESCRIPTION = (
    "Paid Media World is an engineered performance marketing agency founded by Subhranil Naskar. "
    "We specialize in Google Ads (Search, Feed-Only PMax), Meta Ads (3:2:2 Dynamic Sandbox, Advantage+), "
    "server-side CAPI tracking, and deterministic CRO for D2C brands, B2B SaaS, and high-ticket lead generation."
)

FULL_OVERVIEW = """Paid Media World is an independent performance marketing agency and research publication founded to bring transparency, deterministic math, and engineering discipline to digital advertising. 

Operating from Kolkata, India and managing campaigns for high-growth brands across the US, UK, Canada, Australia, and India, Paid Media World bridges high-level executive marketing strategy with granular technical execution.

Core Capabilities:
• Google Ads Engineering: High-intent exact match Search architecture, Feed-Only Remarketing Performance Max, negative term bleed elimination, and brand cannibalization audits.
• Meta Ads Architecture: Advantage+ Shopping Campaigns (ASC) fed by systematic 3:2:2 Dynamic Creative Testing Sandboxes.
• Technical Analytics & Attribution: Server-side Meta Conversions API (CAPI) deduplication, offline Google GCLID synchronization, and GA4 revenue reconciliation.
• Conversion Rate Optimization (CRO): High-converting landing page sprints and real-time ad auction optimization.

Engagement Model: Structured 90-day growth sprints and comprehensive 5-day ad account performance audits."""

# Selected Platforms for Agency / Marketing Services
SHARD_PLATFORMS = [
    {
        "name": "Clutch",
        "domain": "clutch.co",
        "dr": 91,
        "follow_type": "nofollow",
        "submission_url": "https://clutch.co/get-listed",
        "category": "B2B Agency & Marketing Directory",
        "notes": "Top B2B agency evaluation platform. List under Digital Marketing & Paid Search."
    },
    {
        "name": "Sortlist",
        "domain": "sortlist.com",
        "dr": 80,
        "follow_type": "dofollow",
        "submission_url": "https://www.sortlist.com/claim/agency",
        "category": "B2B Agency Directory",
        "notes": "Verified dofollow backlink. Select Agency category -> Paid Media / Google Ads."
    },
    {
        "name": "Crunchbase",
        "domain": "crunchbase.com",
        "dr": 90,
        "follow_type": "nofollow",
        "submission_url": "https://www.crunchbase.com/add-new",
        "category": "Company Intelligence & Knowledge Graph",
        "notes": "Authority brand citation. Links founder Subhranil Naskar to company entity."
    },
    {
        "name": "ProvenExpert",
        "domain": "provenexpert.com",
        "dr": 91,
        "follow_type": "dofollow",
        "submission_url": "https://www.provenexpert.com/",
        "category": "Review & Trust Profile",
        "notes": "High DA dofollow business trust and review profile."
    },
    {
        "name": "TechBehemoths",
        "domain": "techbehemoths.com",
        "dr": 72,
        "follow_type": "dofollow",
        "submission_url": "https://techbehemoths.com/companies/get-listed",
        "category": "B2B Tech & Marketing Agency Directory",
        "notes": "Verified dofollow listing for digital marketing and PPC agencies."
    },
    {
        "name": "Brownbook",
        "domain": "brownbook.net",
        "dr": 79,
        "follow_type": "dofollow",
        "submission_url": "https://www.brownbook.net/register/",
        "category": "Global Business Directory",
        "notes": "High-authority dofollow business citation."
    },
    {
        "name": "Callupcontact",
        "domain": "callupcontact.com",
        "dr": 76,
        "follow_type": "dofollow",
        "submission_url": "https://www.callupcontact.com/active/register/register.php?",
        "category": "Global Service Directory",
        "notes": "Dofollow listing with NAP consistency."
    },
    {
        "name": "Bizcommunity",
        "domain": "bizcommunity.com",
        "dr": 78,
        "follow_type": "dofollow",
        "submission_url": "https://www.bizcommunity.com/Signin.aspx?fa=15&l=196&c=1&menu=134&ru=https%3a%2f%2fwww.bizcommunity.com%2fMyAccount%2fCompanies.aspx",
        "category": "B2B News & Marketing Directory",
        "notes": "Dofollow B2B company listing."
    },
    {
        "name": "Cybo",
        "domain": "cybo.com",
        "dr": 74,
        "follow_type": "dofollow",
        "submission_url": "https://www.cybo.com/add-business/",
        "category": "Global Business Directory",
        "notes": "Dofollow business listing."
    },
    {
        "name": "Linktree",
        "domain": "linktr.ee",
        "dr": 94,
        "follow_type": "dofollow",
        "submission_url": "https://linktr.ee/register/select-plan",
        "category": "High Authority Web Profile",
        "notes": "DR 94 dofollow profile linking to primary services, audit page, and case studies."
    }
]

def build_campaign_file():
    os.makedirs("campaigns", exist_ok=True)
    campaign_file = "campaigns/paidmediaworld_shard_01.md"

    table_rows = []
    for p in SHARD_PLATFORMS:
        key = generate_key(p["domain"], "paidmediaworld")
        table_rows.append(
            f"| {p['domain']} | queued | {p['dr']} | {p['follow_type']} | {p['submission_url']} | — | {key} | — | {p['notes']} |"
        )

    content = f"""# Campaign Ledger: Paid Media World — Shard 01 (Tier 1 Foundational Backlinks)

**Brand / Domain:** {BRAND_NAME} ({CANONICAL_URL})  
**Founder:** {FOUNDER_NAME} ({FOUNDER_TITLE})  
**Category:** Performance Marketing Agency (Google Ads, Meta Ads, Technical Web Analytics)  
**Location:** {HQ_LOCATION} | **Coverage:** {GEO_SERVICED}  
**Status:** In-Progress (Batch Shard 01)  
**Batch Scope:** 10 High-Authority Platforms (Average DR: 82.5)  

---

## Brand Submission Copy (Pre-Approved Facts)

- **Official Name:** `{BRAND_NAME}`
- **Website URL:** `{CANONICAL_URL}`
- **One-Sentence Tagline:** `{TAGLINE}`
- **Short Summary (for directories with 250-char limits):**
  > {SHORT_DESCRIPTION}

- **Full Profile Overview (for Clutch, Sortlist, Crunchbase):**
```text
{FULL_OVERVIEW}
```

- **Target Category Tags:** Performance Marketing, PPC Agency, Google Ads Management, Meta Ads, B2B SaaS Growth, Conversion Rate Optimization.
- **Anchor Text Rule:** Strictly `{BRAND_NAME}` or `{CANONICAL_URL}` (Zero commercial keyword anchors to ensure 100% Penguin safety).

---

## Submission Queue (Shard 01)

| Domain | Status | DR | Follow Type | Submission URL | Live Link URL | Idempotency Key | Verified Date | Notes |
|---|---|---|---|---|---|---|---|---|
{chr(10).join(table_rows)}

---

## Step-by-Step Execution Protocol

1. **Step 1:** Open each `Submission URL` in browser.
2. **Step 2:** Paste the exact pre-approved name (`{BRAND_NAME}`), canonical URL (`{CANONICAL_URL}`), and matching description.
3. **Step 3:** Use your company email (`contact@paidmediaworld.com` or founder address) for verification.
4. **Step 4:** Once submitted or live, update the `Status` column (`submitted` or `live_verified`) and paste the live profile URL.
5. **Step 5:** Run audit verification:
   ```powershell
   python link-building-skill/scripts/audit_campaign_record.py campaigns/paidmediaworld_shard_01.md
   ```
"""

    with open(campaign_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[OK] Created campaign file: {campaign_file}")
    return campaign_file

if __name__ == "__main__":
    campaign_path = build_campaign_file()
