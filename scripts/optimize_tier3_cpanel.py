import os
import json
import sys
import requests
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deploy_nov24_articles import (
    get_cpanel_session,
    verify_live_urls,
    submit_indexnow,
    submit_google_indexing,
)
from optimize_tier1_cpanel import patch_html, HEADERS

load_dotenv(r"C:\Users\test\Videos\Personal\.env")

TIER3_UPDATES = [
    {
        "slug": "rank-tracker",
        "new_title": "Free Google SERP Rank Tracker (2026): Real-Time Keyword Position Checker",
        "new_desc": "Free real-time Google SERP rank tracker: check live keyword positions 1-100 across desktop and mobile, monitor rank volatility, and export SERP reports.",
        "add_software_schema": True,
        "app_name": "Paid Media World Free Google SERP Rank Tracker",
    },
    {
        "slug": "google-ads-for-construction-companies",
        "new_title": "PPC & Google Ads for Construction Companies & Contractors (2026 Guide)",
        "new_desc": "2026 PPC & Google Ads playbook for construction companies, builders, and contractors: high-intent keywords, negative keyword lists, and CPL benchmarks.",
        "add_software_schema": False,
    },
    {
        "slug": "best-payment-gateway-international-payments-india",
        "new_title": "Best Payment Gateway for International Payments in India (2026 Fees & e-FIRC)",
        "new_desc": "Compare the best payment gateways to receive international payments in India (2026): RazorpayX, Stripe, PayGlocal, Payoneer, and Wise fees, forex markup, and e-FIRC.",
        "add_software_schema": False,
    },
    {
        "slug": "keyword-match-type-tool",
        "new_title": "Free Keyword Match Type Tool & Google Ads Wrapper (Exact, Phrase, Broad)",
        "new_desc": "Free Google Ads keyword match type tool and wrapper: convert keywords into [exact], \"phrase\", broad, and negative match lists for Google Ads Editor in 1 click.",
        "add_software_schema": True,
        "app_name": "Paid Media World Free Keyword Match Type Tool",
    },
]


def inject_software_schema(html: str, name: str, url: str, desc: str) -> str:
    if '"SoftwareApplication"' in html:
        return html
    schema = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": name,
            "operatingSystem": "Web",
            "applicationCategory": "BusinessApplication",
            "url": url,
            "description": desc,
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
            "publisher": {"@type": "Organization", "name": "Paid Media World", "url": "https://paidmediaworld.com/"},
        }
    )
    tag = f'<script type="application/ld+json">{schema}</script></head>'
    return html.replace("</head>", tag, 1)


def main():
    os.makedirs("scratch/backups", exist_ok=True)
    s, sec_token = get_cpanel_session()
    upload_url = f"https://paidmediaworld.com:2083{sec_token}/execute/Fileman/upload_files"
    results = []

    for item in TIER3_UPDATES:
        slug = item["slug"]
        url = f"https://paidmediaworld.com/{slug}/"
        r = requests.get(url, headers=HEADERS, timeout=20)
        r.encoding = "utf-8"
        if r.status_code != 200:
            print(f"[SKIP] {slug} returned HTTP {r.status_code}")
            continue

        with open(f"scratch/backups/{slug}.html", "w", encoding="utf-8") as bf:
            bf.write(r.text)

        updated_html = patch_html(r.text, item["new_title"], item["new_desc"])
        if item.get("add_software_schema"):
            updated_html = inject_software_schema(updated_html, item["app_name"], url, item["new_desc"])

        up = s.post(
            upload_url,
            data={"dir": f"public_html/paidmediaworld/{slug}", "overwrite": "1"},
            files={"file-0": ("index.html", updated_html.encode("utf-8"))},
            verify=False,
            timeout=25,
        ).json()
        if up.get("status") == 1:
            print(f"[OK] Uploaded Tier 3: {slug} ({len(updated_html.encode('utf-8')):,} bytes, SoftwareApp={'SoftwareApplication' in updated_html})")
            results.append({"slug": slug, "title": item["new_title"], "url": url, "status": "LIVE"})
        else:
            print(f"[FAIL] {slug}: {up.get('errors')}")
            results.append({"slug": slug, "title": item["new_title"], "url": url, "status": "FAILED"})

    verify_live_urls(results)
    live_urls = [r["url"] for r in results if r.get("verified")]
    if live_urls:
        submit_indexnow(live_urls)
        submit_google_indexing(live_urls)


if __name__ == "__main__":
    main()
