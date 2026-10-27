#!/usr/bin/env python3
"""
Build Shard 02 for Paid Media World
"""

import os
import hashlib

def generate_key(domain, product_id):
    return hashlib.sha256(f"{domain.lower()}:{product_id.lower()}".encode("utf-8")).hexdigest()[:12]

shard_02_platforms = [
    {
        "name": "G2 (Marketing & Advertising Services)",
        "domain": "g2.com",
        "dr": 98,
        "follow_type": "nofollow",
        "submission_url": "https://www.g2.com/products/new",
        "category": "Enterprise B2B Agency & Software Reviews",
        "notes": "Create listing under Marketing Services & Agency Solutions."
    },
    {
        "name": "Substack (Paid Media World Publication)",
        "domain": "substack.com",
        "dr": 93,
        "follow_type": "dofollow",
        "submission_url": "https://substack.com",
        "category": "High Authority Publication & Newsletter",
        "notes": "High-DR dofollow profile link + publish Field Notes from Active Ad Auctions."
    },
    {
        "name": "Medium (Engineering Performance Media)",
        "domain": "medium.com",
        "dr": 94,
        "follow_type": "nofollow",
        "submission_url": "https://medium.com/",
        "category": "Authority Publication Hub",
        "notes": "Author bio backlink to https://paidmediaworld.com/ with CAPI/Google Ads case studies."
    },
    {
        "name": "AlternativeTo (Google Ads Wrapper & Tools)",
        "domain": "alternativeto.net",
        "dr": 81,
        "follow_type": "dofollow",
        "submission_url": "https://alternativeto.net/manage-item/",
        "category": "Software & Tool Directory",
        "notes": "Verified dofollow link. Submit Paid Media World Keyword Match Type Tool."
    },
    {
        "name": "Devpost (Ad Auction Automation Showcase)",
        "domain": "devpost.com",
        "dr": 86,
        "follow_type": "dofollow",
        "submission_url": "https://devpost.com/software/new",
        "category": "Developer Project & Tool Showcase",
        "notes": "Verified dofollow link. Showcase Real-Time AQI Google Ads Smoke Poller & Keyword Wrapper."
    },
    {
        "name": "F6S",
        "domain": "f6s.com",
        "dr": 86,
        "follow_type": "nofollow",
        "submission_url": "https://www.f6s.com",
        "category": "Global Founder & Agency Network",
        "notes": "High authority entity profile linking founder Subhranil Naskar & agency."
    },
    {
        "name": "PRLog",
        "domain": "prlog.org",
        "dr": 83,
        "follow_type": "nofollow",
        "submission_url": "https://www.prlog.org/pub/login.html",
        "category": "Press Release & News Distribution",
        "notes": "Publish agency launch and 2026 Performance Marketing Benchmark Study."
    },
    {
        "name": "OpenPR",
        "domain": "openpr.com",
        "dr": 81,
        "follow_type": "nofollow",
        "submission_url": "https://www.openpr.com/news/submit.html",
        "category": "B2B Press Portal",
        "notes": "Distribute deterministic ad tracking and CAPI research."
    },
    {
        "name": "Startup88",
        "domain": "startup88.com",
        "dr": 88,
        "follow_type": "nofollow",
        "submission_url": "https://startup88.typeform.com/to/CRjWqM",
        "category": "High DR Discovery & Review",
        "notes": "Agency & tools review listing."
    },
    {
        "name": "Featured Customers",
        "domain": "featuredcustomers.com",
        "dr": 71,
        "follow_type": "dofollow",
        "submission_url": "https://www.featuredcustomers.com/",
        "category": "B2B Case Studies & Client Success Hub",
        "notes": "Verified dofollow link. Upload AirDog, Nutrabytes, and Share Samadhan client case studies."
    }
]

table_rows = []
for p in shard_02_platforms:
    key = generate_key(p["domain"], "paidmediaworld")
    table_rows.append(
        f"| {p['domain']} | queued | {p['dr']} | {p['follow_type']} | {p['submission_url']} | — | {key} | — | {p['notes']} |"
    )

content = f"""# Campaign Ledger: Paid Media World — Shard 02 (High DR Authority & Media)

**Brand / Domain:** Paid Media World (https://paidmediaworld.com/)  
**Founder:** Subhranil Naskar  
**Batch Scope:** Shard 02 (10 High Authority Platforms | Average DR: 85.4)  
**Status:** Queued / Ready for Execution  

---

## Submission Queue (Shard 02)

| Domain | Status | DR | Follow Type | Submission URL | Live Link URL | Idempotency Key | Verified Date | Notes |
|---|---|---|---|---|---|---|---|---|
{chr(10).join(table_rows)}

---

## Submission Assets & Tool Angles

### Angle A: Agency Services (G2, F6S, Featured Customers, Startup88)
- Target URL: `https://paidmediaworld.com/`
- Service Focus: Performance Marketing, Google Ads PMax, Meta Ads Advantage+, CAPI, CRO.

### Angle B: Marketing Tools & Engineered Solutions (AlternativeTo, Devpost)
- Target URL: `https://paidmediaworld.com/keyword-match-type-tool/`
- Product Name: `Paid Media World Keyword Match Type Tool & Google Ads Wrapper`
- Tagline: Free, deterministic keyword wrapper tool for Google Ads search query structuring.

### Angle C: Case Studies & Research Distribution (Featured Customers, PRLog, OpenPR)
- Target URL: `https://paidmediaworld.com/case-studies/`
- Featured Clients: AirDog, Nutrabytes, Share Samadhan, IAOL.

---

## Verification Command
```powershell
python link-building-skill/scripts/audit_campaign_record.py campaigns/paidmediaworld_shard_02.md
```
"""

os.makedirs("campaigns", exist_ok=True)
with open("campaigns/paidmediaworld_shard_02.md", "w", encoding="utf-8") as f:
    f.write(content)

print("[OK] Created campaigns/paidmediaworld_shard_02.md successfully!")
