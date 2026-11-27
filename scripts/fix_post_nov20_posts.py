import os
import sys
import json
import re
import requests
import urllib3
from dotenv import load_dotenv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv(r"C:\Users\test\Videos\Personal\.env")

CP_HOST = os.getenv("CPANEL_HOST", "paidmediaworld.com")
CP_PORT = int(os.getenv("CPANEL_PORT", 2083))
CP_USER = os.getenv("CPANEL_USER", "twofouti")
CP_PASS = os.getenv("CPANEL_PASS")
CACHE_DIR = r"C:\Users\test\.gemini\antigravity\brain\5f0255b6-8e8f-4cdc-af55-f41f67748555\scratch\pmw_cache"

sys.path.insert(0, r"C:\Users\test\Videos\Personal\scripts")
import deploy_three_articles as d3
import deploy_nov24_articles as d24
import deploy_nov25_articles as d25
import update_blog_index as ubi

IMAGE_MAP = {
    "automate-google-ads-invalid-traffic-audit-python-script": "/uploads/2026/06/google_ads_pillar_new_16_9.jpg",
    "llm-semantic-negative-keyword-miner-google-ads-python": "/uploads/autonomous_negative_keyword_miner_banner.jpg",
    "google-search-console-generative-ai-report-metrics": "/uploads/2026/09/geo_ai_search_visibility_banner.jpg",
    "meta-andromeda-algorithm-creative-targeting-setup": "/uploads/2026/08/meta_cost_cap_vs_bid_cap_opt.jpg",
    "automate-google-ads-spend-anomaly-detection-python-script": "/uploads/2026/07/target_roas_break_even_cac_1785341700955.jpg",
    "princeton-kdd-generative-engine-optimization-tactics": "/uploads/2026/09/geo_ai_search_visibility_banner.jpg",
    "google-november-2026-core-update-chrome-158-xslt-sitemap-fix": "/uploads/2026/11/seo_core_update_banner.jpg",
    "gsc-generative-ai-report-geo-ai-overviews-optimization": "/uploads/2026/11/geo_ai_overview_banner.jpg",
    "wiring-marketing-mcp-servers-google-ads-meta-ga4-safety": "/uploads/2026/11/mcp_marketing_automation_banner.jpg",
}


def load_en_shell():
    with open(os.path.join(CACHE_DIR, "en_whatsapp.html"), "r", encoding="utf-8") as f:
        html = f.read()
    h_start = html.find("<header ")
    h_end = html.find("</header>") + len("</header>")
    f_start = html.find("<footer ")
    f_end = html.find("</footer>") + len("</footer>")
    return html[h_start:h_end], html[f_start:f_end]


def extract_fields(old_html):
    t = re.search(r"<h1[^>]*>(.*?)</h1>", old_html, re.S)
    d = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]*)"', old_html, re.S)
    kw = re.search(r'<span class="truncate max-w-\[260px\] text-gray-800">(.*?)</span>', old_html, re.S)
    cat = re.search(r'<div class="inline-flex items-center gap-2[^>]*>\s*(.*?)\s*</div>', old_html, re.S)
    rt = re.search(r'<span>(\d+ min read)</span>', old_html)
    dt = re.search(r'<span>(November \d+, 2026)</span>', old_html)
    body_m = re.search(r'<article class="article-body">\s*(.*?)\s*</article>', old_html, re.S)
    return {
        "title": t.group(1).strip() if t else "",
        "desc": d.group(1).strip() if d else "",
        "kw": kw.group(1).strip() if kw else "performance marketing",
        "cat": cat.group(1).strip() if cat else "Performance Marketing",
        "read_time": rt.group(1) if rt else "8 min read",
        "pub_date": dt.group(1) if dt else "November 25, 2026",
        "body": body_m.group(1).strip() if body_m else "",
    }


def build_pmw_en_html(slug, fields, img_path, header_html, footer_html):
    url = f"https://paidmediaworld.com/{slug}/"
    full_img = f"https://paidmediaworld.com{img_path}"
    title = fields["title"]
    desc = fields["desc"]
    kw = fields["kw"]
    cat = fields["cat"]
    read_time = fields["read_time"]
    pub_date = fields["pub_date"]
    iso_date = "2026-11-24T09:00:00+00:00" if "24" in pub_date else "2026-11-25T09:00:00+00:00"
    body = fields["body"]

    tech_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": title,
        "description": desc,
        "inLanguage": "en",
        "image": full_img,
        "datePublished": iso_date,
        "dateModified": iso_date,
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "author": {"@type": "Person", "name": "Subhranil Naskar", "jobTitle": "Senior Performance Marketing Director", "url": "https://paidmediaworld.com/about-us/"},
        "publisher": {"@type": "Organization", "name": "Paid Media World", "url": "https://paidmediaworld.com/", "logo": {"@type": "ImageObject", "url": "https://paidmediaworld.com/pmw_logo_light_2026.png"}},
    }, ensure_ascii=False)

    bc_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://paidmediaworld.com/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://paidmediaworld.com/blog/"},
            {"@type": "ListItem", "position": 3, "name": title, "item": url},
        ],
    }, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <link rel="stylesheet" href="/_next/static/css/088cbaf21f389878.css"/>
  <title>{title} | Paid Media World</title>
  <meta name="description" content="{desc}"/>
  <link rel="canonical" href="{url}"/>
  <meta name="google-adsense-account" content="ca-pub-4871015401102715"/>
  <meta property="og:title" content="{title} | Paid Media World"/>
  <meta property="og:description" content="{desc}"/>
  <meta property="og:url" content="{url}"/>
  <meta property="og:site_name" content="Paid Media World"/>
  <meta property="og:locale" content="en_US"/>
  <meta property="og:image" content="{full_img}"/>
  <meta property="og:type" content="article"/>
  <meta name="twitter:card" content="summary_large_image"/>
  <meta name="twitter:title" content="{title}"/>
  <meta name="twitter:description" content="{desc}"/>
  <meta name="twitter:image" content="{full_img}"/>
  <link rel="shortcut icon" href="/favicon-2026.ico?v=20261028"/>
  <link rel="icon" href="/icon-2026.png?v=20261028" type="image/png" sizes="32x32"/>
  <link rel="apple-touch-icon" href="/apple-icon-2026.png?v=20261028" sizes="180x180" type="image/png"/>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;family=JetBrains+Mono:wght@400;500;600;700&amp;display=swap" rel="stylesheet"/>
  <style>
    .article-content h2 {{ font-size: 1.6rem; font-weight: 800; color: #062649; margin-top: 2.25rem; margin-bottom: 0.85rem; line-height: 1.3; border-bottom: 2px solid #F0F6FF; padding-bottom: 0.5rem; }}
    .article-content h3 {{ font-size: 1.25rem; font-weight: 700; color: #0E56A8; margin-top: 1.75rem; margin-bottom: 0.65rem; line-height: 1.4; }}
    .article-content p {{ margin-bottom: 1.15rem; line-height: 1.8; color: #374151; font-size: 1.02rem; }}
    .article-content ul, .article-content ol {{ margin-bottom: 1.25rem; padding-left: 1.5rem; color: #374151; line-height: 1.75; }}
    .article-content ul {{ list-style-type: disc; }}
    .article-content ol {{ list-style-type: decimal; }}
    .article-content li {{ margin-bottom: 0.5rem; }}
    .article-content pre {{ background: #0B1120; color: #E2E8F0; padding: 1.15rem; border-radius: 0.75rem; overflow-x: auto; margin: 1.5rem 0; font-size: 0.875rem; line-height: 1.6; }}
    .article-content code {{ font-family: 'JetBrains Mono', monospace; background: #F1F5F9; color: #0E56A8; padding: 0.15rem 0.35rem; border-radius: 0.25rem; font-size: 0.9em; }}
    .article-content pre code {{ background: transparent; color: inherit; padding: 0; }}
    .article-content table {{ width: 100%; border-collapse: collapse; margin: 1.5rem 0; background: #fff; border-radius: 0.75rem; overflow: hidden; border: 1px solid #E7E7E7; }}
    .article-content th {{ background: #F0F6FF; color: #062649; font-weight: 700; padding: 0.85rem 1rem; text-align: left; border-bottom: 2px solid #D0E2FF; font-size: 0.92rem; }}
    .article-content td {{ padding: 0.85rem 1rem; border-bottom: 1px solid #E5E7EB; color: #374151; font-size: 0.92rem; }}
    .callout-box {{ padding: 1.35rem; border-radius: 1rem; background: #F0F6FF; border: 1px solid #D0E2FF; margin-bottom: 1.75rem; }}
  </style>
</head>
<body class="min-h-screen flex flex-col bg-white text-[#242C2B] antialiased selection:bg-[#FFE4CC] selection:text-[#062649]">
{header_html}
<main class="flex-grow w-full max-w-full overflow-x-hidden">
  <article class="pb-24">
    <script type="application/ld+json">{tech_schema}</script>
    <script type="application/ld+json">{bc_schema}</script>
    <header class="pt-10 pb-8 border-b border-[#E7E7E7] bg-gradient-to-b from-[#F0F6FF]/60 via-white to-white">
      <div class="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8 space-y-6">
        <nav class="flex items-center space-x-2 text-xs font-mono text-[#6B7280]">
          <a class="hover:text-[#FF6600]" href="/">Home</a>
          <span>/</span>
          <a class="hover:text-[#FF6600]" href="/blog/">Blog</a>
          <span>/</span>
          <span class="text-[#062649] font-bold line-clamp-1">{kw}</span>
        </nav>
        <div class="flex flex-wrap items-center gap-3">
          <span class="font-mono font-bold text-xs text-[#0E56A8] bg-[#F0F6FF] px-3 py-1 rounded-full border border-[#0E56A8]/20">{cat}</span>
          <div class="inline-flex items-center space-x-1.5 text-xs text-[#0EB972] font-mono font-bold bg-[#0EB972]/10 px-3 py-1 rounded-full border border-[#0EB972]/20">
            <span>✓ Verified Technical Guide</span>
          </div>
          <div class="flex items-center space-x-1 text-xs text-[#6B7280] font-mono ml-auto">
            <span>{read_time}</span>
          </div>
        </div>
        <h1 class="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-[#062649] tracking-tight leading-[1.2]">{title}</h1>
        <div class="pt-4 border-t border-[#E7E7E7] flex flex-wrap items-center justify-between gap-4 text-xs sm:text-sm text-[#6B7280]">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 rounded-full bg-[#062649] text-white flex items-center justify-center font-bold text-sm">SN</div>
            <div>
              <div class="font-bold text-[#062649]">Subhranil Naskar</div>
              <div class="text-xs text-[#7E8492]">Principal Performance Strategist &amp; System Architect</div>
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <span>{pub_date}</span>
          </div>
        </div>
      </div>
    </header>
    <div class="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8 pt-10">
      <div class="mb-10 rounded-2xl overflow-hidden border border-[#E7E7E7] shadow-lg">
        <img src="{img_path}" alt="{title}" class="w-full h-auto object-cover max-h-[480px]"/>
      </div>
      <div class="article-content space-y-6 text-slate-700 leading-relaxed text-base">
{body}
      </div>
      <section class="mt-16 rounded-3xl border border-[#E7E7E7] bg-[#F8F8F9] p-8 space-y-4 shadow-sm">
        <div class="flex items-center space-x-4">
          <div class="w-14 h-14 rounded-2xl bg-[#062649] text-white flex items-center justify-center font-bold text-xl flex-shrink-0">SN</div>
          <div>
            <h3 class="text-lg font-bold text-[#062649]">Subhranil Naskar</h3>
            <p class="text-xs font-mono text-[#0E56A8]">Principal Growth Architect &amp; Founder of Paid Media World</p>
          </div>
        </div>
        <p class="text-sm text-[#374151] leading-relaxed">Senior performance marketing engineer with over a decade managing multi-region Google Ads and Meta Ads accounts, specializing in POAS unit economics, server-side CAPI tracking, and Generative Engine Optimization (GEO).</p>
      </section>
      <section class="mt-12 rounded-3xl border border-[#E7E7E7] bg-gradient-to-r from-[#0E1D3B] via-[#14305F] to-[#0E1D3B] p-8 sm:p-12 shadow-2xl text-center space-y-6">
        <h2 class="text-2xl sm:text-3xl font-extrabold text-white tracking-tight max-w-2xl mx-auto">Struggling with High CPA or Tracking Blind Spots?</h2>
        <p class="text-sm sm:text-base text-slate-200 max-w-2xl mx-auto leading-relaxed">We audit your Google Ads search terms, Meta CAPI deduplication, and GA4 attribution pipeline to eliminate wasted spend.</p>
        <div class="pt-2">
          <a href="/contact-us/" class="inline-flex items-center justify-center px-8 py-4 rounded-xl bg-[#FF6600] hover:bg-[#EE3400] text-white font-bold text-sm shadow-xl shadow-[#FF6600]/30 transition-all">
            <span>Book Free Diagnostic Audit →</span>
          </a>
        </div>
      </section>
    </div>
  </article>
</main>
{footer_html}
</body>
</html>"""


def main():
    s = requests.Session()
    r = s.post(f"https://{CP_HOST}:{CP_PORT}/login/?login_only=1",
               data={"user": CP_USER, "pass": CP_PASS}, verify=False, timeout=20)
    tok = r.json().get("security_token")
    if not tok:
        raise RuntimeError(f"cPanel auth failed: {r.text}")
    upload_url = f"https://{CP_HOST}:{CP_PORT}{tok}/execute/Fileman/upload_files"

    # 1. Upload the 2 generated banners
    banners = [
        (r"C:\Users\test\.gemini\antigravity\brain\5f0255b6-8e8f-4cdc-af55-f41f67748555\seo_core_update_banner_1795582523160.jpg", "seo_core_update_banner.jpg"),
        (r"C:\Users\test\.gemini\antigravity\brain\5f0255b6-8e8f-4cdc-af55-f41f67748555\mcp_marketing_automation_banner_1795582601496.jpg", "mcp_marketing_automation_banner.jpg"),
    ]
    for local_p, remote_name in banners:
        with open(local_p, "rb") as f:
            res = s.post(upload_url, data={"dir": "public_html/paidmediaworld/uploads/2026/11", "overwrite": "1"},
                         files={"file-0": (remote_name, f.read())}, verify=False, timeout=30).json()
        print(f"Uploaded banner {remote_name}: status={res.get('status')}")

    # 2. Rebuild all 9 post-Nov 20 English articles
    header_html, footer_html = load_en_shell()
    all_articles = d3.generate_articles() + d24.generate_articles() + d25.generate_articles()
    for art in all_articles:
        slug = art["slug"]
        fields = extract_fields(art["html"])
        img_path = IMAGE_MAP.get(slug, "/uploads/2026/09/geo_ai_search_visibility_banner.jpg")
        new_html = build_pmw_en_html(slug, fields, img_path, header_html, footer_html)
        res = s.post(upload_url, data={"dir": f"public_html/paidmediaworld/{slug}", "overwrite": "1"},
                     files={"file-0": ("index.html", new_html.encode("utf-8"))}, verify=False, timeout=25).json()
        print(f"Rebuilt {slug}: status={res.get('status')} img={img_path}")

    # 3. Also update update_blog_index.py remaining 2026/08 paths via live sync
    ubi.NEW_EN_POSTS[3]["featured_image"] = ubi.NEW_EN_POSTS[3]["image"] = "/uploads/2026/09/geo_ai_search_visibility_banner.jpg"
    ubi.NEW_EN_POSTS[4]["featured_image"] = ubi.NEW_EN_POSTS[4]["image"] = "/uploads/2026/06/google_ads_pillar_new_16_9.jpg"
    ubi.NEW_EN_POSTS[6]["featured_image"] = ubi.NEW_EN_POSTS[6]["image"] = "/uploads/2026/09/geo_ai_search_visibility_banner.jpg"
    ubi.NEW_EN_POSTS[8]["featured_image"] = ubi.NEW_EN_POSTS[8]["image"] = "/uploads/2026/06/google_ads_pillar_new_16_9.jpg"

    # Re-fetch & replace any 404 image URLs already injected into /blog/
    headers = {"User-Agent": "Mozilla/5.0 Chrome/120.0.0.0", "Referer": "https://paidmediaworld.com/"}
    blog_r = requests.get("https://paidmediaworld.com/blog/", headers=headers, timeout=25)
    blog_r.encoding = "utf-8"
    blog_html = blog_r.text
    blog_html = blog_html.replace("/uploads/2026/08/google_ads_scripts_automation.jpg", "/uploads/2026/11/mcp_marketing_automation_banner.jpg")
    blog_html = blog_html.replace("/uploads/2026/08/seo_technical_audit_checklist.jpg", "/uploads/2026/11/seo_core_update_banner.jpg")
    res = s.post(upload_url, data={"dir": "public_html/paidmediaworld/blog", "overwrite": "1"},
                 files={"file-0": ("index.html", blog_html.encode("utf-8"))}, verify=False, timeout=30).json()
    print("Updated /blog/images:", res.get("status"))

    # 4. Verify all 9 pages + 2 new images
    for im in ["/uploads/2026/11/seo_core_update_banner.jpg", "/uploads/2026/11/mcp_marketing_automation_banner.jpg"]:
        hr = requests.head("https://paidmediaworld.com" + im, headers=headers, timeout=10)
        print(f"Verify IMG {hr.status_code}: {im}")
    for slug in IMAGE_MAP:
        pr = requests.get(f"https://paidmediaworld.com/{slug}/", headers=headers, timeout=15)
        has_css = "088cbaf21f389878.css" in pr.text
        has_img = IMAGE_MAP[slug] in pr.text
        print(f"Verify POST {pr.status_code} | css={has_css} | img={has_img} | /{slug}/")


if __name__ == "__main__":
    main()
