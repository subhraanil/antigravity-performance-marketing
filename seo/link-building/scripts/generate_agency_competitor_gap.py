#!/usr/bin/env python3
"""
Generate Competitor Link Intersect for Paid Media World
Compares backlink intersect patterns across top performance marketing agencies.
"""

import os
import json
from competitor_gap import run_link_gap_analysis

my_existing_links = ["paidmediaworld.com"]

# Curated link graphs of primary performance marketing agency competitors
competitor_link_graphs = {
    "KlientBoost": [
        {"domain": "hubspot.com", "dr": 93, "source_url": "https://blog.hubspot.com/marketing/top-ppc-agencies"},
        {"domain": "searchengineland.com", "dr": 91, "source_url": "https://searchengineland.com/author/klientboost"},
        {"domain": "martech.org", "dr": 85, "source_url": "https://martech.org/contributor/klientboost"},
        {"domain": "goodfirms.co", "dr": 83, "source_url": "https://www.goodfirms.co/companies/view/klientboost"},
        {"domain": "themanifest.com", "dr": 82, "source_url": "https://themanifest.com/agencies/ppc"},
        {"domain": "upcity.com", "dr": 81, "source_url": "https://upcity.com/profiles/klientboost"},
        {"domain": "designrush.com", "dr": 81, "source_url": "https://www.designrush.com/agency/profile/klientboost"},
        {"domain": "wordstream.com", "dr": 90, "source_url": "https://www.wordstream.com/blog/best-ppc-agencies"},
        {"domain": "agencyanalytics.com", "dr": 78, "source_url": "https://agencyanalytics.com/blog/agency-spotlight"}
    ],
    "SingleGrain": [
        {"domain": "hubspot.com", "dr": 93, "source_url": "https://blog.hubspot.com/marketing/top-ppc-agencies"},
        {"domain": "searchengineland.com", "dr": 91, "source_url": "https://searchengineland.com/author/singlegrain"},
        {"domain": "martech.org", "dr": 85, "source_url": "https://martech.org/contributor/singlegrain"},
        {"domain": "growthhackers.com", "dr": 79, "source_url": "https://growthhackers.com/posts/single-grain-growth"},
        {"domain": "forbes.com", "dr": 94, "source_url": "https://www.forbes.com/sites/singlegrain"},
        {"domain": "goodfirms.co", "dr": 83, "source_url": "https://www.goodfirms.co/companies/view/single-grain"},
        {"domain": "themanifest.com", "dr": 82, "source_url": "https://themanifest.com/agencies/ppc"},
        {"domain": "designrush.com", "dr": 81, "source_url": "https://www.designrush.com/agency/profile/singlegrain"}
    ],
    "DisruptiveAdvertising": [
        {"domain": "hubspot.com", "dr": 93, "source_url": "https://blog.hubspot.com/marketing/top-ppc-agencies"},
        {"domain": "goodfirms.co", "dr": 83, "source_url": "https://www.goodfirms.co/companies/view/disruptive"},
        {"domain": "themanifest.com", "dr": 82, "source_url": "https://themanifest.com/agencies/ppc"},
        {"domain": "upcity.com", "dr": 81, "source_url": "https://upcity.com/profiles/disruptive"},
        {"domain": "designrush.com", "dr": 81, "source_url": "https://www.designrush.com/agency/profile/disruptive"},
        {"domain": "searchengineland.com", "dr": 91, "source_url": "https://searchengineland.com/article/ppc-roundup"},
        {"domain": "agencyanalytics.com", "dr": 78, "source_url": "https://agencyanalytics.com/blog/agency-spotlight"}
    ]
}

res = run_link_gap_analysis(my_existing_links, competitor_link_graphs)

lines = [
    "# Competitor Link Intersect Report: Paid Media World",
    "**Target:** Paid Media World (https://paidmediaworld.com/)",
    "**Competitors Analyzed:** KlientBoost, Single Grain, Disruptive Advertising",
    f"**Total Gap Opportunities:** {res['total_gap_opportunities']}",
    f"**Multi-Competitor Intersects (>=2 Competitors):** {res['multi_competitor_intersects']}",
    f"**High-Priority 'Gold' Targets:** {res['high_priority_gold_leads']}",
    "",
    "---",
    "",
    "## Prioritized Link Acquisition Targets",
    "",
    "| Domain | DR | Competitor Overlap | Priority Score | Target Strategy | Outreach Action |",
    "|---|:---:|:---:|:---:|---|---|"
]

for opp in res["opportunities"]:
    strategy = "Editorial Guest Contribution / Expert Quote" if opp["dr"] >= 85 else "B2B Agency Profile / Directory Inclusion"
    action = f"Pitch Subhranil Naskar on CAPI & 2026 Ad Auction Benchmarks to editors at {opp['domain']}" if opp["dr"] >= 85 else f"Claim agency listing and submit client case studies on {opp['domain']}"
    lines.append(
        f"| **{opp['domain']}** | {opp['dr']} | {opp['competitors_linked_count']} competitors | {opp['priority_score']} | {strategy} | {action} |"
    )

lines.extend([
    "",
    "---",
    "",
    "## Recommended Action Sequence",
    "1. **Gold Directory Intersects (GoodFirms, The Manifest, DesignRush, UpCity):** These platforms list all 3 competitors. Creating your verified listing here will immediately close the foundational citation gap.",
    "2. **Gold Editorial Intersects (HubSpot, Search Engine Land, MarTech):** These publications cite both KlientBoost and Single Grain for PPC benchmarks. Pitch Subhranil Naskar using the **Data-Anchor** or **Contrarian Hook** pitches from `paidmediaworld_pr_pitches.md` referencing our 2026 Statistics Asset."
])

os.makedirs("campaigns", exist_ok=True)
out_file = "campaigns/paidmediaworld_competitor_gap.md"
with open(out_file, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"[OK] Created {out_file}")
