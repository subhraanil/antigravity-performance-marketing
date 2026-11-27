import os
import re
import json
import requests
from dotenv import load_dotenv

load_dotenv(r"C:\Users\test\Videos\Personal\.env")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://paidmediaworld.com/",
}
CACHE_DIR = r"C:\Users\test\.gemini\antigravity\brain\5f0255b6-8e8f-4cdc-af55-f41f67748555\scratch\pmw_cache"

ARTICLE_CSS = """
    .article-content h2 { font-size: 1.6rem; font-weight: 800; color: #062649; margin-top: 2.25rem; margin-bottom: 0.85rem; line-height: 1.3; border-bottom: 2px solid #F0F6FF; padding-bottom: 0.5rem; }
    .article-content h3 { font-size: 1.25rem; font-weight: 700; color: #0E56A8; margin-top: 1.75rem; margin-bottom: 0.65rem; line-height: 1.4; }
    .article-content p { margin-bottom: 1.15rem; line-height: 1.8; color: #374151; font-size: 1.02rem; }
    .article-content ul, .article-content ol { margin-bottom: 1.25rem; padding-left: 1.5rem; color: #374151; line-height: 1.75; }
    .article-content ul { list-style-type: disc; }
    .article-content ol { list-style-type: decimal; }
    .article-content li { margin-bottom: 0.5rem; }
    .article-content pre { background: #0B1120; color: #E2E8F0; padding: 1.15rem; border-radius: 0.75rem; overflow-x: auto; margin: 1.5rem 0; font-size: 0.875rem; line-height: 1.6; }
    .article-content code { font-family: 'JetBrains Mono', monospace; background: #F1F5F9; color: #0E56A8; padding: 0.15rem 0.35rem; border-radius: 0.25rem; font-size: 0.9em; }
    .article-content pre code { background: transparent; color: inherit; padding: 0; }
    .article-content table { width: 100%; border-collapse: collapse; margin: 1.5rem 0; background: #fff; border-radius: 0.75rem; overflow: hidden; border: 1px solid #E7E7E7; }
    .article-content th { background: #F0F6FF; color: #062649; font-weight: 700; padding: 0.85rem 1rem; text-align: left; border-bottom: 2px solid #D0E2FF; font-size: 0.92rem; }
    .article-content td { padding: 0.85rem 1rem; border-bottom: 1px solid #E5E7EB; color: #374151; font-size: 0.92rem; }
    .callout-box { padding: 1.35rem; border-radius: 1rem; background: #F0F6FF; border: 1px solid #D0E2FF; margin-bottom: 1.75rem; }
"""


def get_site_chrome(lang="en"):
    """Load PaidMediaWorld header and footer from local cache or live site."""
    cache_file = os.path.join(CACHE_DIR, "en_whatsapp.html" if lang == "en" else "es_cost_cap.html")
    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            html = f.read()
    else:
        src_url = (
            "https://paidmediaworld.com/track-whatsapp-leads-ga4-google-tag-manager/"
            if lang == "en"
            else "https://paidmediaworld.com/es/meta-ads-cost-cap-vs-bid-cap-estrategia-escala/"
        )
        r = requests.get(src_url, headers=HEADERS, timeout=20)
        r.encoding = "utf-8"
        html = r.text
        os.makedirs(CACHE_DIR, exist_ok=True)
        with open(cache_file, "w", encoding="utf-8") as f:
            f.write(html)

    h_start = html.find("<header ")
    h_end = html.find("</header>") + len("</header>")
    f_start = html.find("<footer ")
    f_end = html.find("</footer>") + len("</footer>")
    return html[h_start:h_end], html[f_start:f_end]


def build_pmw_article_html(
    title,
    slug,
    primary_kw,
    category,
    description,
    read_time,
    publish_date,
    body_content,
    featured_image="/uploads/2026/09/geo_ai_search_visibility_banner.jpg",
    iso_date=None,
    lang="en",
    en_counterpart_url=None,
):
    """Build a canonical PaidMediaWorld article HTML matching live site CSS, header, footer, and featured image."""
    header_html, footer_html = get_site_chrome(lang=lang)
    prefix = "/es" if lang == "es" else ""
    url = f"https://paidmediaworld.com{prefix}/{slug}/"
    full_img = featured_image if featured_image.startswith("http") else f"https://paidmediaworld.com{featured_image}"
    if not iso_date:
        iso_date = f"{publish_date[:10]}T09:00:00+00:00" if re.match(r"^\d{4}-\d{2}-\d{2}", publish_date) else "2026-11-25T09:00:00+00:00"

    if lang == "es" and en_counterpart_url:
        old_en = "https://paidmediaworld.com/meta-ads-cost-cap-vs-bid-cap-scaling-guide/"
        header_html = header_html.replace(old_en, en_counterpart_url)
        footer_html = footer_html.replace(old_en, en_counterpart_url)

    tech_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": title,
        "description": description,
        "inLanguage": lang,
        "image": full_img,
        "datePublished": iso_date,
        "dateModified": iso_date,
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "author": {"@type": "Person", "name": "Subhranil Naskar", "jobTitle": "Senior Performance Marketing Director", "url": "https://paidmediaworld.com/about-us/"},
        "publisher": {"@type": "Organization", "name": "Paid Media World", "url": "https://paidmediaworld.com/", "logo": {"@type": "ImageObject", "url": "https://paidmediaworld.com/pmw_logo_light_2026.png"}},
    }, ensure_ascii=False)

    bc_home = "Inicio" if lang == "es" else "Home"
    bc_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": bc_home, "item": f"https://paidmediaworld.com{prefix}/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"https://paidmediaworld.com{prefix}/blog/"},
            {"@type": "ListItem", "position": 3, "name": title, "item": url},
        ],
    }, ensure_ascii=False)

    hreflang_tags = ""
    if lang == "es" and en_counterpart_url:
        hreflang_tags = (
            f'\n  <link rel="alternate" hrefLang="en" href="{en_counterpart_url}"/>'
            f'\n  <link rel="alternate" hrefLang="es" href="{url}"/>'
            f'\n  <link rel="alternate" hrefLang="x-default" href="{en_counterpart_url}"/>'
        )

    og_locale = "es_ES" if lang == "es" else "en_US"
    verified_label = "✓ Verificado por Senior Partner" if lang == "es" else "✓ Verified Technical Guide"

    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <link rel="stylesheet" href="/_next/static/css/088cbaf21f389878.css"/>
  <title>{title} | Paid Media World</title>
  <meta name="description" content="{description}"/>
  <link rel="canonical" href="{url}"/>{hreflang_tags}
  <meta name="google-adsense-account" content="ca-pub-4871015401102715"/>
  <meta property="og:title" content="{title} | Paid Media World"/>
  <meta property="og:description" content="{description}"/>
  <meta property="og:url" content="{url}"/>
  <meta property="og:site_name" content="Paid Media World"/>
  <meta property="og:locale" content="{og_locale}"/>
  <meta property="og:image" content="{full_img}"/>
  <meta property="og:type" content="article"/>
  <meta name="twitter:card" content="summary_large_image"/>
  <meta name="twitter:title" content="{title}"/>
  <meta name="twitter:description" content="{description}"/>
  <meta name="twitter:image" content="{full_img}"/>
  <link rel="shortcut icon" href="/favicon-2026.ico?v=20261028"/>
  <link rel="icon" href="/icon-2026.png?v=20261028" type="image/png" sizes="32x32"/>
  <link rel="apple-touch-icon" href="/apple-icon-2026.png?v=20261028" sizes="180x180" type="image/png"/>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;family=JetBrains+Mono:wght@400;500;600;700&amp;display=swap" rel="stylesheet"/>
  <style>{ARTICLE_CSS}</style>
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
          <a class="hover:text-[#FF6600]" href="{prefix or '/'}">{bc_home}</a>
          <span>/</span>
          <a class="hover:text-[#FF6600]" href="{prefix}/blog/">Blog</a>
          <span>/</span>
          <span class="text-[#062649] font-bold line-clamp-1">{primary_kw}</span>
        </nav>
        <div class="flex flex-wrap items-center gap-3">
          <span class="font-mono font-bold text-xs text-[#0E56A8] bg-[#F0F6FF] px-3 py-1 rounded-full border border-[#0E56A8]/20">{category}</span>
          <div class="inline-flex items-center space-x-1.5 text-xs text-[#0EB972] font-mono font-bold bg-[#0EB972]/10 px-3 py-1 rounded-full border border-[#0EB972]/20">
            <span>{verified_label}</span>
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
            <span>{publish_date}</span>
          </div>
        </div>
      </div>
    </header>
    <div class="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8 pt-10">
      <div class="mb-10 rounded-2xl overflow-hidden border border-[#E7E7E7] shadow-lg">
        <img src="{featured_image}" alt="{title}" class="w-full h-auto object-cover max-h-[480px]"/>
      </div>
      <div class="article-content space-y-6 text-slate-700 leading-relaxed text-base">
{body_content}
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
