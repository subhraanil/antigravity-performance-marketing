# -*- coding: utf-8 -*-
"""
check_and_index_sitemap.py
--------------------------
1. Fetches all URLs from a given sitemap XML.
2. Checks each URL's indexing status via the Google Search Console URL Inspection API.
3. Submits any URL that is NOT indexed to the Google Indexing API.

Usage:
    python scripts/check_and_index_sitemap.py --sitemap "https://example.com/post-sitemap.xml" --site-url "https://example.com/"
    python scripts/check_and_index_sitemap.py --sitemap "https://example.com/post-sitemap.xml" --site-url "https://example.com/" --dry-run
"""

import argparse
import json
import os
import sys
import time
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

# Force UTF-8 output on Windows to avoid cp1252 encoding errors
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

# ── Auth scopes ──────────────────────────────────────────────────────────────
INDEXING_SCOPES = ["https://www.googleapis.com/auth/indexing"]
GSC_SCOPES      = ["https://www.googleapis.com/auth/webmasters.readonly"]

# ── API endpoints ─────────────────────────────────────────────────────────────
INDEXING_ENDPOINT   = "https://indexing.googleapis.com/v3/urlNotifications:publish"
INSPECTION_ENDPOINT = "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect"

# ── Delay between API calls (seconds) to avoid rate-limiting ─────────────────
API_DELAY = 1.5


def get_credentials(service_account_file: str, scopes: list):
    """Return refreshed service-account credentials for the given scopes."""
    if not os.path.exists(service_account_file):
        print(f"[ERROR] Service account file not found: {service_account_file}")
        sys.exit(1)
    creds = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=scopes
    )
    creds.refresh(Request())
    return creds


def fetch_sitemap_urls(sitemap_url: str) -> list:
    """Parse a sitemap XML and return a list of <loc> URLs."""
    print(f"\n[INFO] Fetching sitemap: {sitemap_url}")
    headers = {"User-Agent": "Mozilla/5.0 (compatible; SitemapChecker/1.0)"}
    try:
        resp = requests.get(sitemap_url, headers=headers, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[ERROR] Could not fetch sitemap: {e}")
        sys.exit(1)

    # Strip namespace for simpler parsing
    content = resp.text
    root = ET.fromstring(content)
    # Handle both <urlset> and <sitemapindex>
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [loc.text.strip() for loc in root.findall(".//sm:loc", ns) if loc.text]
    print(f"[INFO] Found {len(urls)} URLs in sitemap.")
    return urls


def check_indexing_status(url: str, site_url: str, creds) -> str:
    """
    Call the URL Inspection API and return the verdict:
      PASS  → indexed
      FAIL  → not indexed / has issues
      ERROR → API call failed
    """
    headers = {
        "Authorization": f"Bearer {creds.token}",
        "Content-Type": "application/json",
    }
    payload = {
        "inspectionUrl": url,
        "siteUrl": site_url,
    }
    try:
        resp = requests.post(INSPECTION_ENDPOINT, headers=headers, json=payload, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            verdict = (
                data.get("inspectionResult", {})
                    .get("indexStatusResult", {})
                    .get("verdict", "UNKNOWN")
            )
            return verdict  # e.g. "PASS", "FAIL", "NEUTRAL"
        else:
            print(f"  [WARN] Inspection API returned {resp.status_code}: {resp.text[:200]}")
            return "ERROR"
    except Exception as e:
        print(f"  [WARN] Inspection request failed: {e}")
        return "ERROR"


def submit_url_for_indexing(url: str, creds_indexing) -> bool:
    """Submit a URL to the Google Indexing API and Bing/IndexNow. Returns True on Google success."""
    headers = {
        "Authorization": f"Bearer {creds_indexing.token}",
        "Content-Type": "application/json",
    }
    payload = {"url": url, "type": "URL_UPDATED"}
    success = False
    try:
        resp = requests.post(INDEXING_ENDPOINT, headers=headers, json=payload, timeout=30)
        if resp.status_code == 200:
            success = True
        else:
            print(f"  [ERROR] Indexing API {resp.status_code}: {resp.text[:200]}")
    except Exception as e:
        print(f"  [ERROR] Indexing request failed: {e}")

    # IndexNow submission
    indexnow_key = os.getenv("INDEXNOW_KEY")
    if indexnow_key:
        try:
            parsed = urlparse(url)
            host = parsed.netloc
            indexnow_url = "https://api.indexnow.org/indexnow"
            in_payload = {
                "host": host,
                "key": indexnow_key,
                "keyLocation": f"https://{host}/{indexnow_key}.txt",
                "urlList": [url]
            }
            res = requests.post(indexnow_url, json=in_payload, headers={"Content-Type": "application/json; charset=utf-8"})
            if res.status_code not in (200, 202):
                print(f"  [WARN] IndexNow API {res.status_code}: {res.text[:200]}")
        except Exception as e:
            print(f"  [WARN] IndexNow request failed: {e}")

    return success


def main():
    parser = argparse.ArgumentParser(
        description="Check GSC indexing status for all sitemap URLs and submit unindexed ones."
    )
    parser.add_argument("--sitemap",      required=True,  help="Full URL of the sitemap XML.")
    parser.add_argument("--site-url",     required=True,  help="GSC property URL (e.g. https://example.com/).")
    parser.add_argument("--key-file",     default="service_account.json",
                        help="Path to service account JSON. Default: service_account.json")
    parser.add_argument("--dry-run",      action="store_true",
                        help="Check status only; do NOT submit to Indexing API.")
    parser.add_argument("--delay",        type=float, default=API_DELAY,
                        help=f"Seconds to wait between API calls. Default: {API_DELAY}")
    args = parser.parse_args()

    # ── Credentials ───────────────────────────────────────────────────────────
    creds_gsc      = get_credentials(args.key_file, GSC_SCOPES)
    creds_indexing = get_credentials(args.key_file, INDEXING_SCOPES) if not args.dry_run else None

    # ── Fetch URLs ────────────────────────────────────────────────────────────
    urls = fetch_sitemap_urls(args.sitemap)
    if not urls:
        print("[INFO] No URLs found. Exiting.")
        return

    # ── Inspect each URL ──────────────────────────────────────────────────────
    results = {"indexed": [], "not_indexed": [], "error": []}

    print(f"\n{'='*60}")
    print(f"{'URL':<55} {'STATUS'}")
    print(f"{'='*60}")

    for url in urls:
        # Refresh token if close to expiry
        if creds_gsc.expiry and creds_gsc.token_state.name != "FRESH":
            creds_gsc.refresh(Request())

        verdict = check_indexing_status(url, args.site_url, creds_gsc)

        if verdict == "PASS":
            status_label = "[INDEXED]"
            results["indexed"].append(url)
        elif verdict in ("FAIL", "NEUTRAL", "UNKNOWN"):
            status_label = "[NOT INDEXED]"
            results["not_indexed"].append(url)
        else:
            status_label = "[ERROR]"
            results["error"].append(url)

        short_url = url.replace("https://", "").replace("http://", "")
        print(f"  {short_url:<53} {status_label}")
        time.sleep(args.delay)

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"[SUMMARY]")
    print(f"  Total URLs   : {len(urls)}")
    print(f"  Indexed      : {len(results['indexed'])}")
    print(f"  Not Indexed  : {len(results['not_indexed'])}")
    print(f"  Errors       : {len(results['error'])}")

    # ── Submit unindexed URLs ─────────────────────────────────────────────────
    if results["not_indexed"]:
        if args.dry_run:
            print(f"\n[DRY-RUN] Would submit {len(results['not_indexed'])} URL(s) to Indexing API:")
            for u in results["not_indexed"]:
                print(f"  -> {u}")
        else:
            print(f"\n[INFO] Submitting {len(results['not_indexed'])} unindexed URL(s) to Google Indexing API...")
            # Refresh indexing creds
            creds_indexing.refresh(Request())
            submitted, failed = [], []
            for url in results["not_indexed"]:
                success = submit_url_for_indexing(url, creds_indexing)
                if success:
                    print(f"  [OK] Submitted: {url}")
                    submitted.append(url)
                else:
                    print(f"  [FAIL] Failed : {url}")
                    failed.append(url)
                time.sleep(args.delay)

            print(f"\n[DONE] Submitted: {len(submitted)} | Failed: {len(failed)}")
    else:
        print("\n[INFO] All URLs are already indexed. Nothing to submit.")

    # ── Save report ───────────────────────────────────────────────────────────
    report_path = "reports/indexing_report.json"
    os.makedirs("reports", exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\n[INFO] Full report saved to: {report_path}")


if __name__ == "__main__":
    main()
