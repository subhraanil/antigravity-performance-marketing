import os
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

TIER2_UPDATES = [
    {
        "slug": "maximizing-roi-with-healthcare-ppc-a-blueprint-for-doctors-and-hospitals-in-kolkata",
        "new_title": "Healthcare PPC Services in Kolkata (2026): Google Ads for Doctors & Hospitals",
        "new_desc": "2026 healthcare PPC blueprint for Kolkata doctors, clinics, and hospitals: high-intent Google Search keywords, NMC-compliant ad copy, and patient-booking CPL benchmarks.",
    },
    {
        "slug": "best-business-credit-cards-ad-spend",
        "new_title": "Best Business Credit Cards for Agency Ad Spend (2026): High Limits & Cashback",
        "new_desc": "Compare the best high-limit corporate and business credit cards for Meta & Google ad spend in 2026: 2%-4% cashback, $1M+ agency limits, and zero FX fees.",
    },
    {
        "slug": "g2-vs-capterra-advertising-b2b-buyer-intent-guide",
        "new_title": "G2 vs. Capterra Advertising (2026): Pricing, Buyer Intent & SaaS Pipeline ROI",
        "new_desc": "Compare G2 vs. Capterra ads for B2B SaaS in 2026: category CPCs, buyer-intent data pricing, and CRM pipeline attribution to lower software SQL costs.",
    },
    {
        "slug": "linkedin-ads-cost-in-india-benchmarks",
        "new_title": "LinkedIn Ads Cost in India (2026): CPC, CPM & B2B CPL Benchmarks",
        "new_desc": "2026 LinkedIn Ads pricing in India: Rs 180-480 CPC, Rs 450-1,200 CPM, and Rs 1,400-4,500 CPL by ad format. Lower B2B SaaS & enterprise lead costs.",
    },
    {
        "slug": "meta-ads-cost-cap-vs-bid-cap-scaling-guide",
        "new_title": "Meta Ads Cost Cap vs. Bid Cap (2026): Bidding Floors & Safe Scaling Guide",
        "new_desc": "When to use Meta Ads Cost Cap vs. Bid Cap in 2026: set profitable CPA/ROAS floors, survive Q4 CPM spikes, and scale without resetting learning phase.",
    },
]

NEW_REDIRECTS = [
    (
        "meta-conversions-api-capi-gateway-guide",
        "https://paidmediaworld.com/facebook-conversion-api-gateway-setup/",
    ),
    (
        "bnpl-provider-comparison-klarna-afterpay-affirm",
        "https://paidmediaworld.com/buy-now-pay-later-bnpl-ecommerce-klarna-afterpay-affirm-sezzle/",
    ),
    (
        "google-demand-gen-vs-performance-max-scaling-guide",
        "https://paidmediaworld.com/google-demand-gen-vs-performance-max/",
    ),
    (
        "marketing-attribution-modeling-touchpoints",
        "https://paidmediaworld.com/fractional-attribution-marketing-attribution-modeling-guide/",
    ),
]


def main():
    os.makedirs("scratch/backups", exist_ok=True)
    s, sec_token = get_cpanel_session()
    upload_url = f"https://paidmediaworld.com:2083{sec_token}/execute/Fileman/upload_files"

    # 1. Update Tier 2 pages
    results = []
    for item in TIER2_UPDATES:
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
        up = s.post(
            upload_url,
            data={"dir": f"public_html/paidmediaworld/{slug}", "overwrite": "1"},
            files={"file-0": ("index.html", updated_html.encode("utf-8"))},
            verify=False,
            timeout=25,
        ).json()
        if up.get("status") == 1:
            print(f"[OK] Uploaded Tier 2: {slug} ({len(updated_html.encode('utf-8')):,} bytes)")
            results.append({"slug": slug, "title": item["new_title"], "url": url, "status": "LIVE"})
        else:
            print(f"[FAIL] {slug}: {up.get('errors')}")
            results.append({"slug": slug, "title": item["new_title"], "url": url, "status": "FAILED"})

    # 2. Update .htaccess with 4 cannibalization 301s
    with open("scratch/htaccess_public_html_paidmediaworld.bak", "r", encoding="utf-8") as hf:
        ht = hf.read()

    anchor = "  # Enforce trailing slash for directory style URLs"
    if anchor not in ht:
        raise RuntimeError("Could not find anchor in .htaccess")

    rules_to_add = []
    for src, dst in NEW_REDIRECTS:
        rule = f"  RewriteRule ^{src}/?$ {dst} [R=301,L]"
        if f"^{src}/?$" not in ht:
            rules_to_add.append(rule)

    if rules_to_add:
        block = (
            "  # --- GSC Cannibalization Consolidation (Nov 26, 2026 Audit) ---\n"
            + "\n".join(rules_to_add)
            + "\n\n"
        )
        new_ht = ht.replace(anchor, block + anchor, 1)
        up_ht = s.post(
            upload_url,
            data={"dir": "public_html/paidmediaworld", "overwrite": "1"},
            files={"file-0": (".htaccess", new_ht.encode("utf-8"))},
            verify=False,
            timeout=25,
        ).json()
        print(f"[OK] Uploaded .htaccess (+{len(rules_to_add)} 301 rules): status={up_ht.get('status')}")
    else:
        print("[INFO] All 4 cannibalization rules already present in .htaccess")

    # 3. Verify Tier 2 live URLs & 301 redirects
    verify_live_urls(results)
    print("\n[VERIFY 301 REDIRECTS]")
    for src, dst in NEW_REDIRECTS:
        resp = requests.get(f"https://paidmediaworld.com/{src}/", headers=HEADERS, allow_redirects=False, timeout=15)
        loc = resp.headers.get("Location", "")
        print(f"  [{resp.status_code}] /{src}/ -> {loc} (match={loc == dst})")

    # 4. Submit Tier 2 URLs for indexing
    live_urls = [r["url"] for r in results if r.get("verified")]
    if live_urls:
        submit_indexnow(live_urls)
        submit_google_indexing(live_urls)


if __name__ == "__main__":
    main()
