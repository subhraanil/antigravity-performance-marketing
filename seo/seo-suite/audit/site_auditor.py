#!/usr/bin/env python3
"""
ApexLink Technical Site Auditor & AI Visibility Engine
Inspired by OpenSEO:
- Technical Site Crawling & Diagnostics (status, canonicals, meta, headings, image alt, internal link graph)
- AI Visibility Audit & Fan-Out Query Simulator
- Intent-Driven Keyword Clustering (Informational, Commercial, Transactional, Navigational)
- Executive Action-Oriented SEO Reporting
"""

import sys
import os
import json
import re
import argparse
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from collections import defaultdict

def audit_page_technical(html_content, target_url):
    soup = BeautifulSoup(html_content, "html.parser")
    issues = []
    page_stats = {}

    # 1. Title Tag
    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    title_len = len(title)
    page_stats["title"] = title
    page_stats["title_length"] = title_len
    if not title:
        issues.append({"level": "critical", "type": "Missing Title Tag", "message": "Page lacks an HTML <title> tag."})
    elif title_len < 25:
        issues.append({"level": "warning", "type": "Short Title Tag", "message": f"Title tag is too short ({title_len} chars). Aim for 45-60 chars."})
    elif title_len > 70:
        issues.append({"level": "warning", "type": "Long Title Tag", "message": f"Title tag is truncated by Google ({title_len} chars). Keep under 65 chars."})

    # 2. Meta Description
    meta_desc = soup.find("meta", attrs={"name": lambda x: x and x.lower() == "description"})
    desc_text = meta_desc.get("content", "").strip() if meta_desc else ""
    desc_len = len(desc_text)
    page_stats["description"] = desc_text
    page_stats["description_length"] = desc_len
    if not desc_text:
        issues.append({"level": "critical", "type": "Missing Meta Description", "message": "No meta description found."})
    elif desc_len < 80:
        issues.append({"level": "warning", "type": "Short Meta Description", "message": f"Description is thin ({desc_len} chars). Aim for 130-160 chars."})
    elif desc_len > 175:
        issues.append({"level": "warning", "type": "Long Meta Description", "message": f"Description exceeds search snippet display limits ({desc_len} chars)."})

    # 3. Canonical Tag
    canonical = soup.find("link", attrs={"rel": lambda x: x and "canonical" in x.lower()})
    canon_href = canonical.get("href", "").strip() if canonical else ""
    page_stats["canonical"] = canon_href
    if not canon_href:
        issues.append({"level": "warning", "type": "Missing Canonical Tag", "message": "No canonical tag specified in <head>."})
    elif canon_href != target_url and canon_href.replace("http://", "https://") != target_url:
        issues.append({"level": "info", "type": "Canonical Discrepancy", "message": f"Canonical points to '{canon_href}' instead of '{target_url}'."})

    # 4. Robots Directives
    robots = soup.find("meta", attrs={"name": lambda x: x and "robots" in x.lower()})
    robots_content = robots.get("content", "").lower() if robots else "index, follow"
    page_stats["robots"] = robots_content
    if "noindex" in robots_content:
        issues.append({"level": "critical", "type": "Noindex Directive", "message": "Page has 'noindex' instruction and will not appear in search results."})

    # 5. Headings Architecture
    h1s = [h.get_text(strip=True) for h in soup.find_all("h1")]
    h2s = [h.get_text(strip=True) for h in soup.find_all("h2")]
    page_stats["h1_count"] = len(h1s)
    page_stats["h2_count"] = len(h2s)
    if len(h1s) == 0:
        issues.append({"level": "critical", "type": "Missing H1 Heading", "message": "Page has no H1 element."})
    elif len(h1s) > 1:
        issues.append({"level": "warning", "type": "Multiple H1 Headings", "message": f"Found {len(h1s)} H1 tags. Consolidate into a single primary H1."})

    # 6. Images & Alt Text
    images = soup.find_all("img")
    missing_alt = [img.get("src", "unknown") for img in images if not img.get("alt")]
    page_stats["total_images"] = len(images)
    page_stats["missing_alt_count"] = len(missing_alt)
    if missing_alt:
        issues.append({"level": "warning", "type": "Missing Image Alt Text", "message": f"{len(missing_alt)} of {len(images)} images missing alt text."})

    # 7. Internal & Outbound Link Graph
    links = soup.find_all("a", href=True)
    internal = []
    external = []
    target_netloc = urlparse(target_url).netloc.lower()
    for a in links:
        href = a["href"].strip()
        parsed = urlparse(href)
        if not parsed.netloc or target_netloc in parsed.netloc.lower():
            internal.append(href)
        else:
            external.append(href)
    page_stats["internal_links"] = len(internal)
    page_stats["external_links"] = len(external)

    critical_count = sum(1 for i in issues if i["level"] == "critical")
    warning_count = sum(1 for i in issues if i["level"] == "warning")

    health_score = max(20, 100 - (critical_count * 25) - (warning_count * 8))

    return {
        "url": target_url,
        "health_score": health_score,
        "page_stats": page_stats,
        "issues": issues
    }

def simulate_ai_visibility_audit(brand_name, market_topic, competitors=None):
    """
    Simulates OpenSEO's AI Visibility Audit & Fan-Out Query Engine.
    Exposes which prompts, fan-out queries, and recurring sources influence LLM citations.
    """
    if not competitors:
        competitors = ["Competitor Alpha", "Competitor Beta"]

    # Sample standard prompt research
    prompts = [
        f"What are the best software tools for {market_topic} in 2026?",
        f"Top alternatives to {competitors[0]} for enterprise {market_topic}",
        f"How to automate workflows in {market_topic}?"
    ]

    recurring_sources = [
        {"source": "g2.com/categories", "type": "Review Directory", "cites_competitors": True, "cites_brand": False, "opportunity": "High"},
        {"source": "techcrunch.com", "type": "Media Publication", "cites_competitors": True, "cites_brand": False, "opportunity": "High"},
        {"source": "reddit.com/r/SaaS", "type": "Community Discussion", "cites_competitors": True, "cites_brand": True, "opportunity": "Medium"},
        {"source": "futuretools.io", "type": "AI Directory", "cites_competitors": False, "cites_brand": True, "opportunity": "Verified"}
    ]

    fan_out_queries = [
        f"{market_topic} tools comparison 2026",
        f"best {market_topic} software reviews",
        f"{competitors[0]} vs competitors"
    ]

    recommendations = [
        {
            "priority": "P1",
            "action": f"Acquire placement on Top 2 third-party review listicles that AI engines cite for '{prompts[0]}'",
            "why": f"ChatGPT Search and Perplexity both cite G2 and TechCrunch roundups when answering questions about {market_topic}."
        },
        {
            "priority": "P2",
            "action": f"Create dedicated '{brand_name} vs {competitors[0]}' comparison hub",
            "why": f"Competitors dominate fan-out searches around '{competitors[0]} vs competitors' because no owned comparison page exists."
        }
    ]

    return {
        "brand_name": brand_name,
        "market_topic": market_topic,
        "prompts_evaluated": prompts,
        "fan_out_queries": fan_out_queries,
        "recurring_third_party_sources": recurring_sources,
        "recommendations": recommendations
    }

def cluster_keywords(keywords_list):
    """
    Groups keywords into Intent-driven clusters (OpenSEO style).
    """
    clusters = {
        "Transactional / High-Intent": [],
        "Commercial Investigation": [],
        "Informational": [],
        "Navigational": []
    }

    for kw in keywords_list:
        k_lower = kw.lower()
        if any(term in k_lower for term in ["buy", "pricing", "cost", "hire", "discount", "free trial", "download"]):
            clusters["Transactional / High-Intent"].append(kw)
        elif any(term in k_lower for term in ["best", "top", "review", "vs", "versus", "alternative", "comparison"]):
            clusters["Commercial Investigation"].append(kw)
        elif any(term in k_lower for term in ["how to", "what is", "guide", "tutorial", "learn", "tips", "examples"]):
            clusters["Informational"].append(kw)
        else:
            clusters["Navigational"].append(kw)

    return clusters

def print_audit_report(tech_res, ai_vis=None):
    print("\n" + "="*70)
    print(f"       APEXLINK SITE AUDIT & TECHNICAL SEO REPORT")
    print(f"       Health Score: {tech_res['health_score']}/100")
    print("="*70)
    stats = tech_res["page_stats"]
    print(f"Target URL:        {tech_res['url']}")
    print(f"Title:             '{stats['title']}' ({stats['title_length']} chars)")
    print(f"Meta Description:  '{stats['description'][:60]}...' ({stats['description_length']} chars)")
    print(f"Canonical URL:     '{stats['canonical']}'")
    print(f"Robots Tag:        '{stats['robots']}'")
    print(f"Headings:          {stats['h1_count']} H1 / {stats['h2_count']} H2 tags")
    print(f"Internal Links:    {stats['internal_links']} | External Links: {stats['external_links']}")
    print(f"Images:            {stats['total_images']} total ({stats['missing_alt_count']} missing alt text)")

    print("\n[ Diagnostics & Technical Issues ]")
    if not tech_res["issues"]:
        print("  [+] No technical SEO defects discovered.")
    else:
        for iss in tech_res["issues"]:
            lvl = iss["level"].upper()
            print(f"  [{lvl:8}] {iss['type']}: {iss['message']}")

    if ai_vis:
        print("\n" + "-"*70)
        print("         AI VISIBILITY & CITATION GAP AUDIT (OpenSEO Model)")
        print("-" * 70)
        print(f"Brand:        {ai_vis['brand_name']}")
        print(f"Market Topic: {ai_vis['market_topic']}")
        print("\n[ Fan-Out Queries (Searches Run by AI Models Before Answering) ]")
        for fq in ai_vis["fan_out_queries"]:
            print(f"  -> '{fq}'")

        print("\n[ Recurring Third-Party Sources Cited by AI ]")
        for src in ai_vis["recurring_third_party_sources"]:
            stat = "[CITES COMPETITORS ONLY]" if src["cites_competitors"] and not src["cites_brand"] else "[CITES BRAND]"
            print(f"  * {src['source']:<28} ({src['type']:<20}) {stat}")

        print("\n[ Priority Strategic Recommendations ]")
        for rec in ai_vis["recommendations"]:
            print(f"  {rec['priority']}: {rec['action']}")
            print(f"      Why: {rec['why']}")
    print("="*70 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OpenSEO Technical Site Auditor & AI Visibility Engine")
    parser.add_argument("--url", default="https://example.com/ai-product", help="Target URL")
    parser.add_argument("--file", help="Local HTML file to inspect")
    parser.add_argument("--sample", action="store_true", help="Run benchmark demonstration")
    args = parser.parse_args()

    sample_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <title>Best AI SEO Software for Modern Marketers</title>
      <meta name="description" content="Discover the next-generation AI SEO suite for high-growth SaaS teams. Automate site audits, GSC queries, and backlink prospecting in one unified dashboard.">
      <link rel="canonical" href="https://example.com/ai-product">
    </head>
    <body>
      <h1>Next-Gen AI SEO Automation</h1>
      <p>Accelerate organic visibility and off-page citation building.</p>
      <h2>Comprehensive Site Audits</h2>
      <p>Inspect technical health and robots configurations.</p>
      <img src="/assets/chart.png" alt="SEO Performance Growth Chart">
      <img src="/assets/logo.png">
      <a href="/features">Features</a>
      <a href="/pricing">Pricing</a>
      <a href="https://g2.com">External Review</a>
    </body>
    </html>
    """

    res = audit_page_technical(sample_html, args.url)
    ai_vis = simulate_ai_visibility_audit("ApexEngine", "AI SEO Automation", ["Competitor Alpha", "Competitor Beta"])
    print_audit_report(res, ai_vis)
