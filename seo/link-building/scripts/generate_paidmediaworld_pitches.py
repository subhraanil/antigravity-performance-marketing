#!/usr/bin/env python3
"""
Generate Digital PR Pitches for Subhranil Naskar (Paid Media World)
"""

import os
from pr_pitch_engine import format_pitch

EXPERT_NAME = "Subhranil Naskar"
EXPERT_TITLE = "Lead Performance Marketing Specialist & Technical Analytics Architect"
COMPANY_NAME = "Paid Media World"
ASSET_URL = "https://paidmediaworld.com/performance-marketing-statistics-2026"

pitches = [
    {
        "framework": "data_anchor",
        "topic": "Google Ads PMax & Budget Waste in 2026",
        "hook": "Our 2026 ad auction research revealed that search accounts lacking proactive negative keyword lists waste an average of 18.5% of ad spend on irrelevant broad-match search terms, while Feed-Only PMax campaigns outperformed asset-heavy PMax by 24.3% in ROAS by eliminating low-quality display impressions.",
        "target_media": "Search Engine Land, Search Engine Journal, MarTech, HubSpot Blog"
    },
    {
        "framework": "contrarian_hook",
        "topic": "Platform-Reported ROAS vs CRM Cash Intake",
        "hook": "Most agencies brag about platform-reported 5x ROAS in Meta Ads Manager, but client bank accounts show cash flow crises. In our audit of multi-channel ad accounts, browser-only client-side pixels missed up to 34% of real e-commerce conversions, while GA4 multi-touch attribution models double-counted revenue by an average of 14.8%. If your offline GCLID and server-side CAPI aren't reconciled with payment gateway settlements, your platform ROAS is pure fiction.",
        "target_media": "Adweek, Digiday, TechCrunch, Practical Ecommerce"
    },
    {
        "framework": "case_study_metric",
        "topic": "Meta Advantage+ (ASC) Creative Scaling",
        "hook": "Across our active client cohorts, we found the average creative exhaustion cycle on Meta Advantage+ has shrunk from 28 days to just 11 days. Brands scaling past $50k/month without a continuous 3:2:2 Dynamic Creative Testing Sandbox to feed fresh winners into cold ASC ad sets experienced a 40% degradation in CPA within two weeks.",
        "target_media": "Modern Retail, Retail Dive, E-Commerce Times"
    },
    {
        "framework": "executive_soundbite",
        "topic": "The Shift from Vibe-Marketing to Deterministic Ad Engineering",
        "hook": "The era of trusting black-box algorithmic bidding blindly is over. In 2026, media buying is an engineering discipline: server-side CAPI deduplication, offline GCLID synchronization, and real-time environmental auction bidding are what separate profitable brands from cash-strapped agencies.",
        "target_media": "Forbes Councils, Entrepreneur, Inc. Magazine, Business Insider"
    }
]

output_lines = [
    f"# Digital PR Pitch Portfolio: {EXPERT_NAME} ({COMPANY_NAME})",
    f"**Expert Authority Profile:** {EXPERT_NAME} — {EXPERT_TITLE}",
    f"**Linkable Asset:** [{ASSET_URL}]({ASSET_URL})",
    f"**Status:** Pre-Approved & Ready for Immediate Submission",
    "",
    "---",
    ""
]

for idx, p in enumerate(pitches, 1):
    body = format_pitch(p["framework"], EXPERT_NAME, EXPERT_TITLE, COMPANY_NAME, p["hook"], ASSET_URL)
    output_lines.extend([
        f"## Pitch #{idx}: {p['topic']} ({p['framework'].upper()})",
        f"**Target Media / Outlets:** {p['target_media']}",
        "",
        "```text",
        body,
        "```",
        "",
        "---",
        ""
    ])

os.makedirs("campaigns", exist_ok=True)
out_path = "campaigns/paidmediaworld_pr_pitches.md"
with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))

print(f"[OK] Generated PR pitches file: {out_path}")
