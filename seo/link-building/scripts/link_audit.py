#!/usr/bin/env python3
"""
ApexLink Link Profile Auditor & Health Scorer
Multi-source backlink analysis, Penguin-safe anchor text distribution audit,
toxic link detection, and Google-compliant disavow file generator.
"""

import sys
import os
import json
import re
import argparse
from urllib.parse import urlparse
from collections import Counter

# Benchmark Anchor Text Targets
BENCHMARKS = {
    "branded": {"min": 0.35, "max": 0.55, "label": "Branded (Company / Brand / Founder Name)"},
    "url": {"min": 0.15, "max": 0.25, "label": "URL / Naked Link (https://..., domain.com)"},
    "generic": {"min": 0.10, "max": 0.20, "label": "Generic (click here, read more, visit website)"},
    "exact_match": {"min": 0.02, "max": 0.08, "ceiling": 0.15, "label": "Exact Match Commercial Keywords"},
    "partial_match": {"min": 0.08, "max": 0.18, "ceiling": 0.25, "label": "Partial Match / LSI Keywords"},
    "natural_longtail": {"min": 0.05, "max": 0.15, "label": "Natural Editorial & Long-tail Sentences"}
}

def clean_domain(url):
    if not url:
        return ""
    try:
        netloc = urlparse(url).netloc.lower()
        if netloc.startswith("www."):
            netloc = netloc[4:]
        return netloc
    except Exception:
        return url.lower()

def classify_anchor(anchor, brand_terms=None):
    if not anchor or anchor.strip() == "":
        return "url"
    a_lower = anchor.strip().lower()
    
    # URL / naked check
    if a_lower.startswith("http") or a_lower.startswith("www.") or ".com" in a_lower or ".io" in a_lower or ".ai" in a_lower:
        return "url"
    
    # Generic check
    generic_phrases = ["click here", "read more", "visit website", "learn more", "website", "link", "source", "here", "this page", "check it out", "official site"]
    if a_lower in generic_phrases:
        return "generic"
    
    # Branded check
    if brand_terms:
        for b in brand_terms:
            if b.lower() in a_lower:
                if len(a_lower.split()) <= 3:
                    return "branded"
                else:
                    return "partial_match"
    
    words = a_lower.split()
    if len(words) >= 6:
        return "natural_longtail"
    elif len(words) <= 2:
        return "exact_match"
    else:
        return "partial_match"

def audit_backlink_profile(data, brand_names=None, output_disavow=None):
    """
    Evaluates backlink records:
    data = [
      {
         "source_url": "...",
         "target_url": "...",
         "anchor": "...",
         "rel": "dofollow" | "nofollow" | "ugc" | "sponsored",
         "source_dr": 75,
         "spam_score": 2,
         "is_spam": False
      }
    ]
    """
    if not brand_names:
        brand_names = []
    
    total_links = len(data)
    if total_links == 0:
        return {
            "status": "error",
            "message": "No backlink records provided for audit."
        }

    referring_domains = Counter()
    tlds = Counter()
    rel_counts = Counter()
    anchor_categories = Counter()
    toxic_links = []
    suspicious_domains = set()

    tier_counts = {"tier1_dr80+": 0, "tier2_dr60-79": 0, "tier3_dr40-59": 0, "tier4_dr<40": 0}

    for row in data:
        source_url = row.get("source_url", "")
        domain = clean_domain(source_url)
        referring_domains[domain] += 1
        
        # TLD
        parts = domain.split(".")
        if len(parts) > 1:
            tlds[parts[-1]] += 1

        # Rel
        rel = row.get("rel", "dofollow").lower()
        rel_counts[rel] += 1

        # DR Tier
        dr = float(row.get("source_dr", 0) or 0)
        if dr >= 80:
            tier_counts["tier1_dr80+"] += 1
        elif dr >= 60:
            tier_counts["tier2_dr60-79"] += 1
        elif dr >= 40:
            tier_counts["tier3_dr40-59"] += 1
        else:
            tier_counts["tier4_dr<40"] += 1

        # Anchor classification
        anchor = row.get("anchor", "")
        cat = classify_anchor(anchor, brand_names)
        anchor_categories[cat] += 1

        # Toxic checks
        spam_score = float(row.get("spam_score", 0) or 0)
        is_spam = row.get("is_spam", False)
        
        # Penguin Red Flag: Exact match anchor on low DR site
        is_toxic = False
        reasons = []
        if spam_score >= 12:
            is_toxic = True
            reasons.append(f"High Moz/DataForSEO Spam Score ({spam_score}%)")
        if is_spam:
            is_toxic = True
            reasons.append("Manually flagged as toxic pattern")
        if cat == "exact_match" and dr < 15 and rel == "dofollow":
            is_toxic = True
            reasons.append("Exact match commercial anchor on burner domain (<DR 15)")
        if referring_domains[domain] > 150:
            reasons.append("Excessive sitewide links from single domain (>150)")

        if is_toxic:
            toxic_links.append({
                "source_url": source_url,
                "domain": domain,
                "anchor": anchor,
                "reasons": reasons
            })
            suspicious_domains.add(domain)

    num_ref_domains = len(referring_domains)
    dofollow_ratio = rel_counts.get("dofollow", 0) / max(1, total_links)
    toxic_ratio = len(suspicious_domains) / max(1, num_ref_domains)

    # Health Scoring (7 Dimensions)
    factor_scores = {}
    
    # 1. Referring domain volume
    if num_ref_domains >= 250:
        factor_scores["referring_domains"] = 100
    elif num_ref_domains >= 100:
        factor_scores["referring_domains"] = 85
    elif num_ref_domains >= 30:
        factor_scores["referring_domains"] = 65
    else:
        factor_scores["referring_domains"] = 40

    # 2. Quality tier distribution
    high_tier_ratio = (tier_counts["tier1_dr80+"] + tier_counts["tier2_dr60-79"]) / max(1, total_links)
    if high_tier_ratio >= 0.25:
        factor_scores["quality_distribution"] = 95
    elif high_tier_ratio >= 0.10:
        factor_scores["quality_distribution"] = 80
    else:
        factor_scores["quality_distribution"] = 55

    # 3. Anchor text naturalness
    exact_ratio = anchor_categories["exact_match"] / max(1, total_links)
    branded_ratio = anchor_categories["branded"] / max(1, total_links)
    if exact_ratio > BENCHMARKS["exact_match"]["ceiling"]:
        anchor_score = max(20, 100 - int((exact_ratio - BENCHMARKS["exact_match"]["ceiling"]) * 300))
    elif branded_ratio >= 0.30:
        anchor_score = 90
    else:
        anchor_score = 70
    factor_scores["anchor_naturalness"] = anchor_score

    # 4. Toxic link ratio
    if toxic_ratio == 0:
        factor_scores["toxic_ratio"] = 100
    elif toxic_ratio < 0.03:
        factor_scores["toxic_ratio"] = 85
    elif toxic_ratio < 0.08:
        factor_scores["toxic_ratio"] = 60
    else:
        factor_scores["toxic_ratio"] = 25

    # 5. Follow / Nofollow Balance
    if 0.55 <= dofollow_ratio <= 0.85:
        factor_scores["follow_ratio"] = 95
    elif 0.40 <= dofollow_ratio <= 0.95:
        factor_scores["follow_ratio"] = 80
    else:
        factor_scores["follow_ratio"] = 50

    # 6. Domain diversity (no single domain > 10% of total links)
    max_single_domain_pct = max(referring_domains.values()) / max(1, total_links) if referring_domains else 0
    if max_single_domain_pct < 0.05:
        factor_scores["domain_diversity"] = 100
    elif max_single_domain_pct < 0.12:
        factor_scores["domain_diversity"] = 75
    else:
        factor_scores["domain_diversity"] = 40

    # 7. TLD spread
    has_high_trust_tld = any(t in tlds for t in ["edu", "gov", "org"])
    factor_scores["tld_diversity"] = 90 if has_high_trust_tld else 75

    # Composite Health Score
    weights = {
        "referring_domains": 0.20,
        "quality_distribution": 0.20,
        "anchor_naturalness": 0.15,
        "toxic_ratio": 0.20,
        "follow_ratio": 0.10,
        "domain_diversity": 0.10,
        "tld_diversity": 0.05
    }
    composite_health_score = round(sum(factor_scores[k] * weights[k] for k in factor_scores))

    # Generate Disavow File if requested
    disavow_content = ""
    if output_disavow and suspicious_domains:
        disavow_lines = [
            "# ApexLink Penguin-Safe Disavow List",
            f"# Generated for {len(suspicious_domains)} toxic referring domains",
            f"# Evaluated {total_links} total backlinks",
            ""
        ]
        for d in sorted(suspicious_domains):
            disavow_lines.append(f"domain:{d}")
        disavow_content = "\n".join(disavow_lines)
        with open(output_disavow, "w", encoding="utf-8") as f:
            f.write(disavow_content)

    return {
        "health_score": composite_health_score,
        "total_backlinks": total_links,
        "referring_domains_count": num_ref_domains,
        "dofollow_ratio": round(dofollow_ratio * 100, 1),
        "nofollow_ratio": round((1 - dofollow_ratio) * 100, 1),
        "anchor_distribution": {
            k: round((v / max(1, total_links)) * 100, 1) for k, v in anchor_categories.items()
        },
        "dr_tiers": tier_counts,
        "toxic_summary": {
            "toxic_domains_count": len(suspicious_domains),
            "toxic_ratio_pct": round(toxic_ratio * 100, 1),
            "disavow_file_generated": output_disavow if output_disavow else None
        },
        "factor_breakdown": factor_scores,
        "top_referring_domains": referring_domains.most_common(10)
    }

def print_audit_report(res):
    print("\n" + "="*60)
    print(f"      APEXLINK BACKLINK HEALTH SCORE: {res['health_score']}/100")
    print("="*60)
    print(f"Total Backlinks Analyzed: {res['total_backlinks']}")
    print(f"Referring Domains:        {res['referring_domains_count']}")
    print(f"Follow / Nofollow Ratio:  {res['dofollow_ratio']}% dofollow / {res['nofollow_ratio']}% nofollow")
    print("\n[ DR Quality Tier Breakdown ]")
    print(f"  - Tier 1 (DR 80+):  {res['dr_tiers']['tier1_dr80+']} links")
    print(f"  - Tier 2 (DR 60-79): {res['dr_tiers']['tier2_dr60-79']} links")
    print(f"  - Tier 3 (DR 40-59): {res['dr_tiers']['tier3_dr40-59']} links")
    print(f"  - Tier 4 (DR < 40):  {res['dr_tiers']['tier4_dr<40']} links")

    print("\n[ Anchor Text Distribution ]")
    for cat, pct in res["anchor_distribution"].items():
        flag = " [!] OVER OPTIMIZED" if cat == "exact_match" and pct > 15 else ""
        print(f"  - {cat.replace('_', ' ').capitalize():20}: {pct:5.1f}%{flag}")

    print("\n[ Toxic Link & Risk Analysis ]")
    print(f"  - Toxic Referring Domains: {res['toxic_summary']['toxic_domains_count']}")
    print(f"  - Toxic Domain Ratio:      {res['toxic_summary']['toxic_ratio_pct']}%")
    if res['toxic_summary']['disavow_file_generated']:
        print(f"  - Disavow File Saved To:   {res['toxic_summary']['disavow_file_generated']}")

    print("\n[ Factor Score Breakdown ]")
    for f, s in res["factor_breakdown"].items():
        status = "PASS" if s >= 80 else ("WARN" if s >= 60 else "FAIL")
        print(f"  - {f.replace('_', ' ').capitalize():22}: {s}/100 [{status}]")
    print("="*60 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit Backlink Profile & Generate Health Score")
    parser.add_argument("--input", required=False, help="JSON or CSV file containing backlink records")
    parser.add_argument("--brand", nargs="*", default=[], help="Brand names/founders to classify branded anchors")
    parser.add_argument("--disavow", help="Path to write Google disavow file if toxic links are found")
    parser.add_argument("--sample", action="store_true", help="Run audit on built-in realistic sample profile")
    args = parser.parse_args()

    if args.sample or not args.input:
        print("[INFO] Running backlink audit with benchmark demonstration sample...")
        sample_data = [
            {"source_url": "https://g2.com/products/example-saas", "anchor": "Example Brand", "rel": "nofollow", "source_dr": 98, "spam_score": 1},
            {"source_url": "https://techcrunch.com/2026/02/example-brand-launch", "anchor": "Example Brand SaaS", "rel": "dofollow", "source_dr": 92, "spam_score": 1},
            {"source_url": "https://devpost.com/software/example-app", "anchor": "https://example.com", "rel": "dofollow", "source_dr": 86, "spam_score": 2},
            {"source_url": "https://alternativeto.net/software/example", "anchor": "visit official site", "rel": "dofollow", "source_dr": 81, "spam_score": 1},
            {"source_url": "https://hubspot.com/state-of-marketing", "anchor": "Example Brand 2026 research", "rel": "dofollow", "source_dr": 93, "spam_score": 1},
            {"source_url": "https://somuch.com/links/saas", "anchor": "Example Brand", "rel": "dofollow", "source_dr": 64, "spam_score": 2},
            {"source_url": "https://bestseobacklinks123.xyz/cheap-seo", "anchor": "best seo software 2026", "rel": "dofollow", "source_dr": 8, "spam_score": 16, "is_spam": True},
            {"source_url": "https://pbn-network-node4.ru/post", "anchor": "buy backlinks", "rel": "dofollow", "source_dr": 4, "spam_score": 14, "is_spam": True}
        ]
        res = audit_backlink_profile(sample_data, brand_names=["example", "example brand"], output_disavow=args.disavow)
        print_audit_report(res)
    else:
        with open(args.input, "r", encoding="utf-8") as f:
            if args.input.endswith(".json"):
                data = json.load(f)
            else:
                import csv
                reader = csv.DictReader(f)
                data = list(reader)
        res = audit_backlink_profile(data, brand_names=args.brand, output_disavow=args.disavow)
        print_audit_report(res)
