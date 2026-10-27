#!/usr/bin/env python3
"""
Build Shard 03 for Paid Media World: B2B Agency & Review Portals
"""

import os
import hashlib

def generate_key(domain, product_id):
    return hashlib.sha256(f"{domain.lower()}:{product_id.lower()}".encode("utf-8")).hexdigest()[:12]

shard_03_platforms = [
    {
        "name": "GoodFirms",
        "domain": "goodfirms.co",
        "dr": 83,
        "follow_type": "dofollow",
        "submission_url": "https://www.goodfirms.co/get-listed",
        "category": "B2B Agency & Service Directory",
        "notes": "Verified dofollow profile. List under Digital Marketing & PPC Agency."
    },
    {
        "name": "The Manifest",
        "domain": "themanifest.com",
        "dr": 82,
        "follow_type": "dofollow",
        "submission_url": "https://themanifest.com/",
        "category": "B2B Business News & Agency Rankings",
        "notes": "Powered by Clutch data. Claim business profile for automated dofollow citation."
    },
    {
        "name": "DesignRush",
        "domain": "designrush.com",
        "dr": 81,
        "follow_type": "dofollow",
        "submission_url": "https://www.designrush.com/agency-signup",
        "category": "B2B Agency Marketplace & Rankings",
        "notes": "Top digital marketing agency directory. List Google Ads & Meta Ads services."
    },
    {
        "name": "UpCity",
        "domain": "upcity.com",
        "dr": 81,
        "follow_type": "nofollow",
        "submission_url": "https://upcity.com/join",
        "category": "B2B Service Provider Directory",
        "notes": "High DR citation. List under PPC Agencies & Performance Marketing."
    },
    {
        "name": "Digital Agency Network (DAN)",
        "domain": "digitalagencynetwork.com",
        "dr": 75,
        "follow_type": "dofollow",
        "submission_url": "https://digitalagencynetwork.com/membership/",
        "category": "Global Digital Marketing Network",
        "notes": "High authority marketing agency network. Free listing available."
    },
    {
        "name": "SaaSHub",
        "domain": "saashub.com",
        "dr": 73,
        "follow_type": "nofollow",
        "submission_url": "https://www.saashub.com/submit",
        "category": "SaaS & Marketing Software Platform",
        "notes": "List Paid Media World Keyword Match Type Tool & Agency Services."
    },
    {
        "name": "GrowthHackers",
        "domain": "growthhackers.com",
        "dr": 79,
        "follow_type": "dofollow",
        "submission_url": "https://growthhackers.com/",
        "category": "Growth Marketing Case Study Community",
        "notes": "Post technical case studies (CAPI deduplication, Feed-only PMax) with author bio backlink."
    },
    {
        "name": "Indie Hackers",
        "domain": "indiehackers.com",
        "dr": 86,
        "follow_type": "dofollow",
        "submission_url": "https://www.indiehackers.com/products/new",
        "category": "Founder & Business Growth Community",
        "notes": "Create product page for Paid Media World + founder profile for Subhranil Naskar."
    },
    {
        "name": "AgencySpotter",
        "domain": "agencyspotter.com",
        "dr": 65,
        "follow_type": "dofollow",
        "submission_url": "https://www.agencyspotter.com/agencies/new",
        "category": "Agency Search & Review Hub",
        "notes": "Dedicated agency portfolio and client review listing."
    },
    {
        "name": "AllMyFaves",
        "domain": "allmyfaves.com",
        "dr": 73,
        "follow_type": "dofollow",
        "submission_url": "https://allmyfaves.com/",
        "category": "Curated Internet & Business Directory",
        "notes": "Verified dofollow directory entry."
    }
]

table_rows = []
for p in shard_03_platforms:
    key = generate_key(p["domain"], "paidmediaworld")
    table_rows.append(
        f"| {p['domain']} | queued | {p['dr']} | {p['follow_type']} | {p['submission_url']} | — | {key} | — | {p['notes']} |"
    )

content = f"""# Campaign Ledger: Paid Media World — Shard 03 (B2B Agency & Review Portals)

**Brand / Domain:** Paid Media World (https://paidmediaworld.com/)  
**Founder:** Subhranil Naskar  
**Batch Scope:** Shard 03 (10 High-Authority B2B Agency & Community Portals | Average DR: 77.8)  
**Status:** Queued / Ready for Execution  

---

## Submission Queue (Shard 03)

| Domain | Status | DR | Follow Type | Submission URL | Live Link URL | Idempotency Key | Verified Date | Notes |
|---|---|---|---|---|---|---|---|---|
{chr(10).join(table_rows)}

---

## Specific Angle for Shard 03 Portals

1. **Agency Directories (GoodFirms, DesignRush, UpCity, AgencySpotter, DAN):**
   - List under: **Digital Marketing Agencies**, **PPC Management**, **Google Ads Agency**, **Meta Ads Agency**.
   - Portfolio URL: `https://paidmediaworld.com/case-studies/`
   - Client Verification: Feature AirDog, Nutrabytes, and Share Samadhan.

2. **Growth & Founder Communities (Indie Hackers, GrowthHackers):**
   - Founder Profile: **Subhranil Naskar** (Lead Performance Marketing Specialist).
   - Bio Link: `https://paidmediaworld.com/`
   - Publish technical insights: *"How we scaled e-commerce brands on Meta ASC by eliminating browser-side pixel bleed with CAPI."*

---

## Verification Command
```powershell
python link-building-skill/scripts/audit_campaign_record.py campaigns/paidmediaworld_shard_03.md
```
"""

os.makedirs("campaigns", exist_ok=True)
with open("campaigns/paidmediaworld_shard_03.md", "w", encoding="utf-8") as f:
    f.write(content)

print("[OK] Created campaigns/paidmediaworld_shard_03.md successfully!")
