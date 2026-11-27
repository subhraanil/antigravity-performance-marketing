import os
import re
import sys
import json
import requests
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deploy_nov24_articles import (
    get_cpanel_session,
    verify_live_urls,
    submit_indexnow,
    submit_google_indexing,
)

load_dotenv(r"C:\Users\test\Videos\Personal\.env")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://paidmediaworld.com/",
}

UPDATES = [
    {
        "slug": "youtube-shorts-ads-scaling-blueprint",
        "new_title": "YouTube Shorts Creative Scaling Blueprint (2026): 3-Sec Hook & Demand Gen Guide",
        "new_desc": "Rank-tested 2026 YouTube Shorts creative scaling playbook: 3-second hook formulas, Demand Gen asset specs, and CPA benchmarks to stop creative fatigue.",
    },
    {
        "slug": "google-ads-cpc-benchmarks-by-country",
        "new_title": "Google Ads CPC Benchmarks by Country (2026): US, UK, India & UAE Rates",
        "new_desc": "Compare 2026 Google Ads CPC, CPM, and CVR benchmarks across 50+ countries including US, UK, India, and UAE. See high-CPC niches and bidding targets.",
    },
    {
        "slug": "buy-now-pay-later-bnpl-ecommerce-klarna-afterpay-affirm-sezzle",
        "new_title": "Best BNPL for eCommerce (2026): Klarna vs. Afterpay vs. Affirm vs. Sezzle",
        "new_desc": "2026 merchant comparison of Klarna, Afterpay, Affirm, and Sezzle: transaction fees, checkout CVR lift, and AOV benchmarks for fashion and omnichannel retail.",
    },
    {
        "slug": "google-ads-cpl-benchmarks-report-2026",
        "new_title": "Google Ads CPL Benchmarks by Industry (2026): CPC, CVR & CPA Data",
        "new_desc": "2026 Google Ads CPL, CPC, and conversion rate benchmarks across 16 industries (B2B SaaS, Real Estate, Healthcare, Home Services). Audit your account CPA.",
    },
    {
        "slug": "g2-software-review-site-ads-pricing-cpc-roi",
        "new_title": "How G2 Ads Work for B2B SaaS (2026): Pricing, CPC & Pipeline ROI",
        "new_desc": "How G2 Ads work for B2B software vendors in 2026: sponsored listing costs, CPC benchmarks, buyer-intent ROI, and G2 vs. Capterra vs. Google Search.",
    },
]


def esc_html(s: str) -> str:
    return s.replace("&", "&amp;")


def patch_html(html: str, new_title: str, new_desc: str) -> str:
    title_html = esc_html(new_title)
    desc_html = esc_html(new_desc)

    # Extract old title/desc so we can also sync Next.js RSC payload occurrences if present
    old_t_m = re.search(r"<title>(.*?)</title>", html, re.S)
    old_d_m = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', html, re.I | re.S)

    html = re.sub(r"<title>.*?</title>", f"<title>{title_html}</title>", html, count=1, flags=re.S)
    html = re.sub(
        r'(<meta[^>]+name=["\']description["\'][^>]+content=["\'])(.*?)(["\'])',
        rf"\g<1>{desc_html}\g<3>",
        html,
        count=1,
        flags=re.I | re.S,
    )
    html = re.sub(
        r'(<meta[^>]+property=["\']og:title["\'][^>]+content=["\'])(.*?)(["\'])',
        rf"\g<1>{title_html}\g<3>",
        html,
        count=1,
        flags=re.I | re.S,
    )
    html = re.sub(
        r'(<meta[^>]+property=["\']og:description["\'][^>]+content=["\'])(.*?)(["\'])',
        rf"\g<1>{desc_html}\g<3>",
        html,
        count=1,
        flags=re.I | re.S,
    )
    html = re.sub(
        r'(<meta[^>]+name=["\']twitter:title["\'][^>]+content=["\'])(.*?)(["\'])',
        rf"\g<1>{title_html}\g<3>",
        html,
        count=1,
        flags=re.I | re.S,
    )
    html = re.sub(
        r'(<meta[^>]+name=["\']twitter:description["\'][^>]+content=["\'])(.*?)(["\'])',
        rf"\g<1>{desc_html}\g<3>",
        html,
        count=1,
        flags=re.I | re.S,
    )
    html = re.sub(
        r'("dateModified"\s*:\s*")\d{4}-\d{2}-\d{2}(")',
        r"\g<1>2026-11-26\g<2>",
        html,
    )

    if old_t_m:
        old_t_raw = old_t_m.group(1).strip().replace("&amp;", "&")
        if old_t_raw and old_t_raw in html:
            head_end = html.find("</head>")
            if head_end != -1:
                html = html[:head_end] + html[head_end:].replace(old_t_raw, new_title)
    if old_d_m:
        old_d_raw = old_d_m.group(1).strip().replace("&amp;", "&")
        if old_d_raw and old_d_raw in html:
            head_end = html.find("</head>")
            if head_end != -1:
                html = html[:head_end] + html[head_end:].replace(old_d_raw, new_desc)

    return html


def main():
    os.makedirs("scratch/backups", exist_ok=True)
    s, sec_token = get_cpanel_session()
    upload_url = f"https://paidmediaworld.com:2083{sec_token}/execute/Fileman/upload_files"
    results = []

    for item in UPDATES:
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
        remote_dir = f"public_html/paidmediaworld/{slug}"
        files = {"file-0": ("index.html", updated_html.encode("utf-8"))}
        data = {"dir": remote_dir, "overwrite": "1"}
        up = s.post(upload_url, data=data, files=files, verify=False, timeout=25).json()

        if up.get("status") == 1:
            print(f"[OK] Uploaded {slug} ({len(updated_html.encode('utf-8')):,} bytes)")
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
