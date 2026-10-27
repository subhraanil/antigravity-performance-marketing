#!/usr/bin/env python3
"""
ApexLink Live Verification Crawler
Deterministically verifies known backlinks: checks live HTTP status, extracts anchor text,
determines rel attributes (dofollow, nofollow, sponsored, ugc), detects JS-only links,
and detects link removal or modification.
"""

import sys
import os
import json
import argparse
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 (ApexLink Backlink Verifier)"

def verify_single_backlink(source_url, target_domain, timeout=12):
    """
    Checks if source_url links to target_domain.
    Returns structured verification dict.
    """
    clean_target = target_domain.lower()
    if clean_target.startswith("http://") or clean_target.startswith("https://"):
        parsed = urlparse(clean_target).netloc
        if parsed.startswith("www."):
            parsed = parsed[4:]
        clean_target = parsed
    elif clean_target.startswith("www."):
        clean_target = clean_target[4:]

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "DNT": "1"
    }

    try:
        resp = requests.get(source_url, headers=headers, timeout=timeout, allow_redirects=True)
        status_code = resp.status_code
        final_url = resp.url

        if status_code >= 400:
            return {
                "source_url": source_url,
                "target_domain": clean_target,
                "status": "error_http",
                "http_status": status_code,
                "link_found": False,
                "error": f"HTTP {status_code}"
            }

        # Check content type
        content_type = resp.headers.get("Content-Type", "").lower()
        if "text/html" not in content_type and "xml" not in content_type:
            return {
                "source_url": source_url,
                "target_domain": clean_target,
                "status": "non_html_response",
                "http_status": status_code,
                "link_found": False,
                "error": f"Content-Type: {content_type}"
            }

        html = resp.text
        soup = BeautifulSoup(html, "html.parser")

        # Check for meta robots noindex
        robots_meta = soup.find("meta", attrs={"name": lambda x: x and x.lower() == "robots"})
        is_noindexed = False
        if robots_meta and "noindex" in robots_meta.get("content", "").lower():
            is_noindexed = True

        # Find all matching <a> tags
        found_links = []
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            # check if target_domain is in href
            if clean_target in href.lower():
                rel = a.get("rel", [])
                if isinstance(rel, list):
                    rel_str = " ".join(rel).lower()
                else:
                    rel_str = str(rel).lower()

                is_dofollow = not any(r in rel_str for r in ["nofollow", "sponsored", "ugc"])
                anchor_text = a.get_text(separator=" ", strip=True)

                found_links.append({
                    "href": href,
                    "anchor_text": anchor_text,
                    "rel": rel_str if rel_str else "dofollow",
                    "is_dofollow": is_dofollow,
                    "is_exact_page": href.lower() == clean_target
                })

        if found_links:
            primary = found_links[0]
            return {
                "source_url": source_url,
                "final_source_url": final_url,
                "target_domain": clean_target,
                "status": "verified_active",
                "http_status": status_code,
                "link_found": True,
                "links_count": len(found_links),
                "primary_href": primary["href"],
                "anchor_text": primary["anchor_text"],
                "rel": primary["rel"],
                "is_dofollow": primary["is_dofollow"],
                "page_noindexed": is_noindexed,
                "all_matches": found_links
            }
        else:
            # Check if this could be client-rendered SPA / JS heavy
            script_count = len(soup.find_all("script"))
            body_text_len = len(soup.get_text(strip=True))
            if script_count > 5 and body_text_len < 300:
                probable_status = "unverifiable_js (requires Playwright/headless browser)"
            else:
                probable_status = "link_removed_or_not_found"

            return {
                "source_url": source_url,
                "final_source_url": final_url,
                "target_domain": clean_target,
                "status": probable_status,
                "http_status": status_code,
                "link_found": False,
                "page_noindexed": is_noindexed
            }

    except requests.exceptions.Timeout:
        return {
            "source_url": source_url,
            "target_domain": clean_target,
            "status": "timeout",
            "link_found": False,
            "error": "Request timed out"
        }
    except Exception as e:
        return {
            "source_url": source_url,
            "target_domain": clean_target,
            "status": "connection_error",
            "link_found": False,
            "error": str(e)
        }

def run_verification(records):
    results = []
    print(f"[VERIFY] Starting verification for {len(records)} backlink target(s)...")
    for idx, r in enumerate(records, 1):
        s_url = r.get("source_url")
        t_dom = r.get("target_domain")
        print(f"[{idx}/{len(records)}] Probing {s_url} -> {t_dom} ...")
        res = verify_single_backlink(s_url, t_dom)
        status_sym = "[OK]" if res["link_found"] else "[!]"
        print(f"       {status_sym} Status: {res['status']} | Anchor: '{res.get('anchor_text', 'N/A')}' | Rel: {res.get('rel', 'N/A')}")
        results.append(res)
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deterministic Live Backlink Verification Crawler")
    parser.add_argument("--source", help="Single source URL to inspect")
    parser.add_argument("--target", help="Target domain or URL to find on the source page")
    parser.add_argument("--file", help="JSON file containing [{'source_url': '...', 'target_domain': '...'}]")
    parser.add_argument("--output", help="Path to write JSON results")
    args = parser.parse_args()

    if args.source and args.target:
        res = verify_single_backlink(args.source, args.target)
        print(json.dumps(res, indent=2))
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump([res], f, indent=2)
    elif args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            records = json.load(f)
        results = run_verification(records)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2)
    else:
        # Demonstrate with sample check
        print("[INFO] No parameters provided. Running verification test probe...")
        probe = verify_single_backlink("https://github.com/Infrasity-Labs", "github.com")
        print(json.dumps(probe, indent=2))
