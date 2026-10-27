#!/usr/bin/env python3
"""
ApexLink Competitor Link Intersect & Gap Analyzer
Compares backlink profiles across target site and 1-5 competitors to identify
high-probability link opportunities (domains linking to competitors but not target).
"""

import sys
import os
import json
import csv
import argparse
from urllib.parse import urlparse
from collections import defaultdict

def extract_domain(url):
    if not url:
        return ""
    try:
        netloc = urlparse(url).netloc.lower()
        if netloc.startswith("www."):
            netloc = netloc[4:]
        return netloc.strip()
    except Exception:
        return url.strip().lower()

def run_link_gap_analysis(target_domains_list, competitor_data_dict, dr_lookup=None):
    """
    target_domains_list: set or list of domains already linking to target site
    competitor_data_dict: {
        "competitor_A.com": [{"domain": "techcrunch.com", "dr": 92, "source_url": "...", "anchor": "..."}, ...],
        "competitor_B.com": [{"domain": "devpost.com", "dr": 86, ...}, ...]
    }
    """
    if dr_lookup is None:
        dr_lookup = {}

    target_set = set(target_domains_list)
    competitor_domains = defaultdict(lambda: {"linked_competitors": set(), "dr": 0, "sample_urls": []})

    for comp_name, backlinks in competitor_data_dict.items():
        for b in backlinks:
            ref_dom = b.get("domain") or extract_domain(b.get("source_url", ""))
            if not ref_dom or ref_dom in target_set:
                continue
            
            dr = b.get("dr", 0) or dr_lookup.get(ref_dom, 0)
            competitor_domains[ref_dom]["linked_competitors"].add(comp_name)
            competitor_domains[ref_dom]["dr"] = max(competitor_domains[ref_dom]["dr"], dr)
            if len(competitor_domains[ref_dom]["sample_urls"]) < 3 and b.get("source_url"):
                competitor_domains[ref_dom]["sample_urls"].append(b.get("source_url"))

    # Convert to structured opportunities list
    opportunities = []
    for ref_dom, info in competitor_domains.items():
        comp_count = len(info["linked_competitors"])
        dr = info["dr"]
        
        # Opportunity Priority Score (0-100)
        # Weights: 40% DR, 60% competitor overlap count
        overlap_score = min(100, comp_count * 35)
        dr_score = min(100, dr)
        priority_score = round((overlap_score * 0.6) + (dr_score * 0.4), 1)

        tier = "High Priority (Gold)" if comp_count >= 2 and dr >= 50 else ("Medium Priority" if comp_count >= 2 or dr >= 60 else "Standard Outreach")

        opportunities.append({
            "domain": ref_dom,
            "dr": dr,
            "competitors_linked_count": comp_count,
            "competitors_linked": sorted(list(info["linked_competitors"])),
            "priority_score": priority_score,
            "tier": tier,
            "sample_urls": info["sample_urls"]
        })

    # Sort by priority score descending
    opportunities.sort(key=lambda x: x["priority_score"], reverse=True)

    return {
        "total_gap_opportunities": len(opportunities),
        "multi_competitor_intersects": sum(1 for o in opportunities if o["competitors_linked_count"] >= 2),
        "high_priority_gold_leads": sum(1 for o in opportunities if o["tier"] == "High Priority (Gold)"),
        "opportunities": opportunities
    }

def print_gap_report(res, limit=20):
    print("\n" + "="*70)
    print("        APEXLINK COMPETITOR LINK GAP & INTERSECT REPORT")
    print("="*70)
    print(f"Total New Referring Domain Opportunities: {res['total_gap_opportunities']}")
    print(f"Multi-Competitor Intersects (>=2 comps):   {res['multi_competitor_intersects']}")
    print(f"High-Priority 'Gold' Outreach Targets:   {res['high_priority_gold_leads']}")
    print("-" * 70)
    print(f"{'Domain':<28} | {'DR':<4} | {'Comps':<5} | {'Priority':<8} | {'Tier'}")
    print("-" * 70)
    for opp in res["opportunities"][:limit]:
        print(f"{opp['domain']:<28} | {opp['dr']:<4} | {opp['competitors_linked_count']:<5} | {opp['priority_score']:<8} | {opp['tier']}")
    print("="*70 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Competitor Backlink Gap & Intersect Analyzer")
    parser.add_argument("--target", help="CSV or text file of target domain referring domains")
    parser.add_argument("--competitors", nargs="+", help="JSON files or CSVs of competitor backlink exports")
    parser.add_argument("--output", help="Path to write JSON opportunities")
    parser.add_argument("--sample", action="store_true", help="Run demonstration gap analysis with sample competitors")
    args = parser.parse_args()

    if args.sample or not args.target:
        print("[INFO] Running competitor gap analysis with benchmark SaaS sample...")
        my_existing_links = ["g2.com", "crunchbase.com", "producthunt.com"]
        competitor_profiles = {
            "Competitor_Alpha": [
                {"domain": "techcrunch.com", "dr": 92, "source_url": "https://techcrunch.com/article1"},
                {"domain": "alternativeto.net", "dr": 81, "source_url": "https://alternativeto.net/software/alpha"},
                {"domain": "saashub.com", "dr": 73, "source_url": "https://saashub.com/alpha"},
                {"domain": "supertools.therundown.ai", "dr": 56, "source_url": "https://supertools.therundown.ai/item"},
                {"domain": "g2.com", "dr": 98, "source_url": "https://g2.com/alpha"}
            ],
            "Competitor_Beta": [
                {"domain": "alternativeto.net", "dr": 81, "source_url": "https://alternativeto.net/software/beta"},
                {"domain": "saashub.com", "dr": 73, "source_url": "https://saashub.com/beta"},
                {"domain": "devpost.com", "dr": 86, "source_url": "https://devpost.com/software/beta"},
                {"domain": "techcrunch.com", "dr": 92, "source_url": "https://techcrunch.com/article2"}
            ]
        }
        res = run_link_gap_analysis(my_existing_links, competitor_profiles)
        print_gap_report(res)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(res, f, indent=2)
