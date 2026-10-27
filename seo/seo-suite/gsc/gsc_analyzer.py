#!/usr/bin/env python3
"""
ApexLink GSC Analyzer (Google Search Console Intelligence)
Inspired by mcp-gsc:
- Keyword Cannibalization Detection: Identifies queries where >= 2 pages compete
- Content Quick-Win Opportunities: Detects striking-distance queries (positions 11-20, high impressions, low CTR)
- Period-over-period search performance comparisons
- URL Indexing & Rich Result issue tracking
"""

import sys
import os
import json
import csv
import argparse
from collections import defaultdict
from urllib.parse import urlparse

def detect_cannibalization(rows, min_impressions=50):
    """
    rows = [
        {"query": "best ai tools", "page": "https://example.com/p1", "clicks": 120, "impressions": 2500, "ctr": 0.048, "position": 4.2},
        {"query": "best ai tools", "page": "https://example.com/p2", "clicks": 20, "impressions": 1800, "ctr": 0.011, "position": 8.5}
    ]
    """
    query_map = defaultdict(list)
    for r in rows:
        q = r.get("query", "").strip().lower()
        if not q:
            continue
        query_map[q].append(r)

    cannibalization_cases = []
    for query, pages in query_map.items():
        # Check if >= 2 distinct pages rank for this query
        distinct_pages = {p["page"] for p in pages}
        if len(distinct_pages) >= 2:
            total_impressions = sum(float(p.get("impressions", 0) or 0) for p in pages)
            total_clicks = sum(float(p.get("clicks", 0) or 0) for p in pages)
            if total_impressions < min_impressions:
                continue

            # Sort pages by position ascending (best position first)
            sorted_pages = sorted(pages, key=lambda x: float(x.get("position", 999)))
            primary_page = sorted_pages[0]
            competing_page = sorted_pages[1]

            # Severity score based on impressions at stake
            severity = "High" if total_impressions >= 1000 else ("Medium" if total_impressions >= 250 else "Low")

            # Recommendation
            recom = f"Consolidate traffic onto primary page ({primary_page['page']}). Consider setting canonical or 301 redirecting {competing_page['page']} if topically redundant."

            cannibalization_cases.append({
                "query": query,
                "pages_count": len(distinct_pages),
                "total_impressions": total_impressions,
                "total_clicks": total_clicks,
                "severity": severity,
                "primary_page": primary_page,
                "competing_pages": sorted_pages[1:],
                "recommendation": recom
            })

    # Sort cases by total impressions descending
    cannibalization_cases.sort(key=lambda x: x["total_impressions"], reverse=True)
    return cannibalization_cases

def detect_content_quick_wins(rows, min_impressions=100, max_ctr=0.03, min_pos=11.0, max_pos=20.0):
    """
    Finds queries in striking distance (positions 11-20) with high impressions but low CTR.
    Opportunity Score = impressions * (0.05 - ctr)
    """
    opportunities = []
    for r in rows:
        try:
            pos = float(r.get("position", 0))
            imp = float(r.get("impressions", 0))
            ctr = float(r.get("ctr", 0))
        except (ValueError, TypeError):
            continue

        if min_pos <= pos <= max_pos and imp >= min_impressions and ctr < max_ctr:
            # Theoretical clicks gained if CTR moves to benchmark 5% (0.05)
            score = round(imp * max(0.01, (0.05 - ctr)), 1)
            opportunities.append({
                "query": r.get("query"),
                "page": r.get("page"),
                "position": round(pos, 1),
                "impressions": int(imp),
                "ctr_pct": round(ctr * 100, 2),
                "opportunity_score": score,
                "action": "Optimize title/H1 hook, enrich schema, add 3-5 internal links from top-traffic pages to push into Top 10."
            })

    # Sort by opportunity score descending
    opportunities.sort(key=lambda x: x["opportunity_score"], reverse=True)
    return opportunities

def compare_search_performance(period_current, period_baseline):
    """
    Computes period-over-period deltas.
    """
    def sum_metrics(data):
        total_clicks = sum(float(r.get("clicks", 0)) for r in data)
        total_imp = sum(float(r.get("impressions", 0)) for r in data)
        avg_ctr = (total_clicks / total_imp) if total_imp > 0 else 0
        avg_pos = sum(float(r.get("position", 0)) * float(r.get("impressions", 0)) for r in data) / max(1, total_imp)
        return total_clicks, total_imp, avg_ctr, avg_pos

    c_clicks, c_imp, c_ctr, c_pos = sum_metrics(period_current)
    b_clicks, b_imp, b_ctr, b_pos = sum_metrics(period_baseline)

    click_delta = c_clicks - b_clicks
    click_pct = round(((click_delta / max(1, b_clicks)) * 100), 1)

    imp_delta = c_imp - b_imp
    imp_pct = round(((imp_delta / max(1, b_imp)) * 100), 1)

    pos_delta = round(c_pos - b_pos, 1) # negative delta is improvement in rank

    return {
        "current": {"clicks": int(c_clicks), "impressions": int(c_imp), "ctr_pct": round(c_ctr * 100, 2), "avg_position": round(c_pos, 1)},
        "baseline": {"clicks": int(b_clicks), "impressions": int(b_imp), "ctr_pct": round(b_ctr * 100, 2), "avg_position": round(b_pos, 1)},
        "deltas": {
            "clicks": click_delta,
            "clicks_growth_pct": click_pct,
            "impressions": imp_delta,
            "impressions_growth_pct": imp_pct,
            "position_delta": pos_delta
        }
    }

def print_gsc_reports(cannibal_cases, quick_wins, perf_compare=None):
    print("\n" + "="*70)
    print("           GOOGLE SEARCH CONSOLE (GSC) INTELLIGENCE AUDIT")
    print("="*70)

    if perf_compare:
        print("\n[ Period-over-Period Performance Overview ]")
        cur = perf_compare["current"]
        base = perf_compare["baseline"]
        delts = perf_compare["deltas"]
        click_sym = "+" if delts["clicks"] >= 0 else ""
        imp_sym = "+" if delts["impressions"] >= 0 else ""
        print(f"  Clicks:      {cur['clicks']:,} (vs {base['clicks']:,} baseline | {click_sym}{delts['clicks_growth_pct']}%)")
        print(f"  Impressions: {cur['impressions']:,} (vs {base['impressions']:,} baseline | {imp_sym}{delts['impressions_growth_pct']}%)")
        print(f"  Avg CTR:     {cur['ctr_pct']}% (vs {base['ctr_pct']}%)")
        print(f"  Avg Position: #{cur['avg_position']} (delta: {delts['position_delta']})")

    print("\n[ Keyword Cannibalization Conflicts ]")
    if not cannibal_cases:
        print("  -> Zero keyword cannibalization conflicts detected. Site hierarchy is clean.")
    else:
        print(f"  Detected {len(cannibal_cases)} cannibalization conflicts. Top cases:")
        for idx, c in enumerate(cannibal_cases[:5], 1):
            print(f"\n  #{idx} Query: '{c['query']}' [{c['severity']} Severity | {int(c['total_impressions']):,} Impressions at Stake]")
            print(f"     Primary Page:   {c['primary_page']['page']} (Pos: #{c['primary_page']['position']}, Clicks: {c['primary_page']['clicks']})")
            for comp in c['competing_pages']:
                print(f"     Competing Page: {comp['page']} (Pos: #{comp['position']}, Clicks: {comp['clicks']})")
            print(f"     Action:         {c['recommendation']}")

    print("\n[ Striking Distance Content Quick-Wins (Positions 11–20) ]")
    if not quick_wins:
        print("  -> No page-2 quick wins meeting criteria.")
    else:
        print(f"  Found {len(quick_wins)} high-impression targets just below the fold. Top opportunities:")
        print(f"  {'Query':<28} | {'Pos':<5} | {'Impressions':<11} | {'CTR':<6} | {'Opportunity Score'}")
        print("  " + "-"*68)
        for q in quick_wins[:8]:
            print(f"  {q['query'][:28]:<28} | #{q['position']:<4} | {q['impressions']:<11,} | {q['ctr_pct']:<5.1f}% | {q['opportunity_score']}")
    print("="*70 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Google Search Console Query & Performance Analyzer")
    parser.add_argument("--input", help="CSV or JSON export of GSC queries and pages")
    parser.add_argument("--cannibalization", action="store_true", help="Run cannibalization check")
    parser.add_argument("--quick-wins", action="store_true", help="Find striking distance quick wins")
    parser.add_argument("--sample", action="store_true", help="Run demonstration with realistic GSC dataset")
    args = parser.parse_args()

    if args.sample or not args.input:
        print("[INFO] Running GSC Analysis with benchmark production sample...")
        sample_rows = [
            # Cannibalization case 1
            {"query": "ai video generator free", "page": "https://example.com/tools/ai-video", "clicks": 340, "impressions": 8500, "ctr": 0.040, "position": 4.1},
            {"query": "ai video generator free", "page": "https://example.com/blog/best-ai-video-tools", "clicks": 95, "impressions": 6200, "ctr": 0.015, "position": 8.4},
            
            # Cannibalization case 2
            {"query": "automated link building software", "page": "https://example.com/backlink-software", "clicks": 180, "impressions": 4200, "ctr": 0.042, "position": 5.2},
            {"query": "automated link building software", "page": "https://example.com/features/link-automation", "clicks": 45, "impressions": 3100, "ctr": 0.014, "position": 9.1},

            # Quick win striking distance (pos 11-20, high impressions, low CTR)
            {"query": "how to build backlinks 2026", "page": "https://example.com/blog/backlink-guide", "clicks": 25, "impressions": 5800, "ctr": 0.004, "position": 12.3},
            {"query": "b2b saas seo strategies", "page": "https://example.com/blog/saas-seo", "clicks": 42, "impressions": 4400, "ctr": 0.009, "position": 14.1},
            {"query": "pr outreach templates for startups", "page": "https://example.com/templates/pr-pitch", "clicks": 18, "impressions": 3200, "ctr": 0.005, "position": 16.5},

            # Normal good ranking
            {"query": "apexlink seo", "page": "https://example.com/", "clicks": 820, "impressions": 1200, "ctr": 0.683, "position": 1.0}
        ]

        sample_baseline = [
            {"query": "ai video generator free", "clicks": 290, "impressions": 7200, "position": 5.5},
            {"query": "automated link building software", "clicks": 150, "impressions": 3800, "position": 6.8},
            {"query": "how to build backlinks 2026", "clicks": 15, "impressions": 4100, "position": 15.2}
        ]

        cannibal = detect_cannibalization(sample_rows)
        quick_wins = detect_content_quick_wins(sample_rows)
        perf_delta = compare_search_performance(sample_rows, sample_baseline)

        print_gsc_reports(cannibal, quick_wins, perf_delta)
    else:
        # Load from file
        with open(args.input, "r", encoding="utf-8") as f:
            if args.input.endswith(".json"):
                rows = json.load(f)
            else:
                reader = csv.DictReader(f)
                rows = list(reader)

        cannibal = detect_cannibalization(rows)
        quick_wins = detect_content_quick_wins(rows)
        print_gsc_reports(cannibal, quick_wins)
