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
INDEXNOW_KEY = os.getenv("INDEXNOW_KEY", "b3901b0f5be84a7e8e58a2d3c905d41f")
SERVICE_ACCOUNT_PATH = r"C:\Users\test\Videos\Personal\service_account.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://paidmediaworld.com/",
}

NEW_EN_POSTS = [
    {
        "id": 9988,
        "title": "Wiring Marketing MCP Servers to Google Ads, Meta Ads & GA4 Safely",
        "slug": "wiring-marketing-mcp-servers-google-ads-meta-ga4-safety",
        "date": "2026-11-25T09:45:00",
        "date_label": "Nov 25, 2026",
        "read_time": "10 min read",
        "excerpt": "Connect Google Ads MCP, GA4 MCP, and Meta Ads MCP to Claude, Cursor, or n8n for instant cross-channel diagnostics with strict read-only and human-in-the-loop budget guardrails.",
        "featured_image": "/uploads/2026/11/mcp_marketing_automation_banner.jpg",
        "image": "/uploads/2026/11/mcp_marketing_automation_banner.jpg",
        "categories": [252, 9],
        "tags": [252, 9],
        "meta_title": "Wiring Marketing MCP Servers to Google Ads, Meta Ads & GA4 Safely",
        "meta_description": "Connect Google Ads MCP, GA4 MCP, and Meta Ads MCP to Claude, Cursor, or n8n for instant cross-channel diagnostics with strict budget guardrails.",
        "primary_keyword": "MCP marketing automation Google Ads",
        "content": "",
    },
    {
        "id": 9987,
        "title": "Decoding GSC Generative AI Reports & Optimizing Pages for GEO / AI Overviews",
        "slug": "gsc-generative-ai-report-geo-ai-overviews-optimization",
        "date": "2026-11-25T09:30:00",
        "date_label": "Nov 25, 2026",
        "read_time": "9 min read",
        "excerpt": "Learn what Google Search Console's Generative AI Performance Report tracks (and hides), and structure pages to earn citations in AI Overviews and AI Mode.",
        "featured_image": "/uploads/2026/11/geo_ai_overview_banner.jpg",
        "image": "/uploads/2026/11/geo_ai_overview_banner.jpg",
        "categories": [252, 9],
        "tags": [252, 9],
        "meta_title": "Decoding GSC Generative AI Reports & Optimizing Pages for GEO / AI Overviews",
        "meta_description": "Learn what Google Search Console's Generative AI Performance Report tracks and how to optimize pages for AI Overviews.",
        "primary_keyword": "GSC generative AI report GEO",
        "content": "",
    },
    {
        "id": 9986,
        "title": "Google November 2026 Core Update Completed + Chrome 158 XSLT Sitemap Fix",
        "slug": "google-november-2026-core-update-chrome-158-xslt-sitemap-fix",
        "date": "2026-11-25T09:15:00",
        "date_label": "Nov 25, 2026",
        "read_time": "8 min read",
        "excerpt": "Google's November 2026 Core Update finished on Nov 24 right alongside Chrome 158 dropping XSLT sitemap rendering. Separate real ranking shifts from BFCM seasonality.",
        "featured_image": "/uploads/2026/11/seo_core_update_banner.jpg",
        "image": "/uploads/2026/11/seo_core_update_banner.jpg",
        "categories": [252, 9],
        "tags": [252, 9],
        "meta_title": "Google November 2026 Core Update Completed + Chrome 158 XSLT Sitemap Fix",
        "meta_description": "Google's November 2026 Core Update finished on Nov 24 alongside Chrome 158 dropping XSLT sitemap rendering.",
        "primary_keyword": "Google November 2026 core update",
        "content": "",
    },
    {
        "id": 9985,
        "title": "Princeton KDD 2024 GEO Framework: The 3 Empirical Levers Boosting AI Overviews Visibility by +40%",
        "slug": "princeton-kdd-generative-engine-optimization-tactics",
        "date": "2026-11-24T17:00:00",
        "date_label": "Nov 24, 2026",
        "read_time": "9 min read",
        "excerpt": "Empirical Generative Engine Optimization (GEO) tactics from Princeton KDD 2024: Statistics Addition, Cite Sources, and Quotation Addition for +30% to +40% AI visibility.",
        "featured_image": "/uploads/2026/11/seo_core_update_banner.jpg",
        "image": "/uploads/2026/11/seo_core_update_banner.jpg",
        "categories": [252, 9],
        "tags": [252, 9],
        "meta_title": "Princeton KDD 2024 GEO Framework: +40% AI Overviews Visibility",
        "meta_description": "Empirical GEO tactics from Princeton KDD 2024 boosting AI Overviews visibility by +40%.",
        "primary_keyword": "Princeton KDD generative engine opt",
        "content": "",
    },
    {
        "id": 9984,
        "title": "Autonomous Google Ads Spend Anomaly Detector: Python Sentinel Guarding Holiday Budgets Every 60 Minutes",
        "slug": "automate-google-ads-spend-anomaly-detection-python-script",
        "date": "2026-11-24T16:00:00",
        "date_label": "Nov 24, 2026",
        "read_time": "8 min read",
        "excerpt": "Open-source Python script querying the Google Ads API hourly to calculate intraday spend velocity derivatives and fire Slack alerts before runaway CPCs burn daily caps.",
        "featured_image": "/uploads/2026/07/target_roas_break_even_cac_1785341700955.jpg",
        "image": "/uploads/2026/07/target_roas_break_even_cac_1785341700955.jpg",
        "categories": [252, 9],
        "tags": [252, 9],
        "meta_title": "Autonomous Google Ads Spend Anomaly Detector Python Script",
        "meta_description": "Python sentinel guarding Google Ads holiday budgets every 60 minutes.",
        "primary_keyword": "Google Ads spend anomaly Python",
        "content": "",
    },
    {
        "id": 9983,
        "title": "Meta Andromeda Retrieval Architecture: Structuring Consolidated CBO Accounts for 1 Billion Ad Scans/Sec",
        "slug": "meta-andromeda-algorithm-creative-targeting-setup",
        "date": "2026-11-24T15:00:00",
        "date_label": "Nov 24, 2026",
        "read_time": "9 min read",
        "excerpt": "How Meta's Andromeda GPU retrieval engine shifts targeting from narrow interest stacks to creative-led indexing in consolidated CBO and Advantage+ accounts.",
        "featured_image": "/uploads/2026/08/meta_cost_cap_vs_bid_cap_opt.jpg",
        "image": "/uploads/2026/08/meta_cost_cap_vs_bid_cap_opt.jpg",
        "categories": [252, 9],
        "tags": [252, 9],
        "meta_title": "Meta Andromeda Retrieval Architecture: Consolidated CBO Setup",
        "meta_description": "Structuring consolidated CBO accounts for Meta's Andromeda retrieval engine.",
        "primary_keyword": "Meta Andromeda creative targeting",
        "content": "",
    },
    {
        "id": 9982,
        "title": "Google Search Console Generative AI Report: De-Anonymizing the Impressions-Only Trap",
        "slug": "google-search-console-generative-ai-report-metrics",
        "date": "2026-11-24T14:00:00",
        "date_label": "Nov 24, 2026",
        "read_time": "7 min read",
        "excerpt": "How to normalize GSC Generative AI Performance Report anomalies and diagnose zero-click cannibalization across AI Overviews.",
        "featured_image": "/uploads/2026/11/seo_core_update_banner.jpg",
        "image": "/uploads/2026/11/seo_core_update_banner.jpg",
        "categories": [252, 9],
        "tags": [252, 9],
        "meta_title": "Google Search Console Generative AI Report Metrics Guide",
        "meta_description": "De-anonymizing the GSC Generative AI Performance Report impressions-only trap.",
        "primary_keyword": "GSC generative AI report metrics",
        "content": "",
    },
    {
        "id": 9981,
        "title": "LLM Semantic Negative Keyword Miner: Real-Time Python Agent Neutralizing Wasted Holiday PPC Spend",
        "slug": "llm-semantic-negative-keyword-miner-google-ads-python",
        "date": "2026-11-24T13:00:00",
        "date_label": "Nov 24, 2026",
        "read_time": "8 min read",
        "excerpt": "Deploy an LLM-powered Python agent that classifies Google Ads search term intent in real time and quarantines wasted holiday PPC spend.",
        "featured_image": "/uploads/autonomous_negative_keyword_miner_banner.jpg",
        "image": "/uploads/autonomous_negative_keyword_miner_banner.jpg",
        "categories": [252, 9],
        "tags": [252, 9],
        "meta_title": "LLM Semantic Negative Keyword Miner for Google Ads",
        "meta_description": "Real-time Python agent neutralizing wasted holiday PPC spend.",
        "primary_keyword": "LLM negative keyword miner PPC",
        "content": "",
    },
    {
        "id": 9980,
        "title": "Autonomous Google Ads Invalid Traffic (IVT) Audit: Open-Source Python Agent for Automated Refund Claims",
        "slug": "automate-google-ads-invalid-traffic-audit-python-script",
        "date": "2026-11-24T12:00:00",
        "date_label": "Nov 24, 2026",
        "read_time": "8 min read",
        "excerpt": "Automate Google Ads Invalid Traffic (IVT) audits with an open-source Python agent to detect bot click spikes and document automated refund claims.",
        "featured_image": "/uploads/2026/11/mcp_marketing_automation_banner.jpg",
        "image": "/uploads/2026/11/mcp_marketing_automation_banner.jpg",
        "categories": [252, 9],
        "tags": [252, 9],
        "meta_title": "Autonomous Google Ads Invalid Traffic (IVT) Audit Python Agent",
        "meta_description": "Open-source Python agent for Google Ads IVT audits and refund claims.",
        "primary_keyword": "Google Ads invalid traffic audit",
        "content": "",
    },
]

NEW_ES_POSTS = [
    {
        "translationKey": "track-whatsapp-leads-ga4-google-tag-manager",
        "sourceSlug": "track-whatsapp-leads-ga4-google-tag-manager",
        "status": "published",
        "reviewedBy": "Carlos Mendoza",
        "reviewerProfile": "Senior Growth Lead & Native Localization Reviewer",
        "lastReviewedDate": "2026-11-25",
        "slug": "rastrear-leads-whatsapp-ga4-google-tag-manager",
        "title": "Cómo Rastrear Leads y Clics de WhatsApp en GA4 con Google Tag Manager (2026)",
        "meta_title": "Cómo Rastrear Leads de WhatsApp en GA4 con GTM (Guía 2026)",
        "meta_description": "Tutorial paso a paso para medir clics a WhatsApp como Eventos Clave en Google Analytics 4 usando Google Tag Manager e importarlos a Google Ads.",
        "primary_keyword": "rastrear leads whatsapp ga4 gtm",
        "secondary_keywords": ["medir clics whatsapp google analytics 4", "evento clave whatsapp gtm"],
        "excerpt": "Tutorial paso a paso para medir clics a WhatsApp como Eventos Clave en GA4 con Google Tag Manager e importarlos a Google Ads.",
        "image": "/uploads/2026/07/track_whatsapp_ga4_gtm_1785341422971.jpg",
        "read_time": "7 min lectura",
    },
    {
        "translationKey": "meta-ads-payment-method-verification-failed-fix",
        "sourceSlug": "meta-ads-payment-method-verification-failed-fix",
        "status": "published",
        "reviewedBy": "Carlos Mendoza",
        "reviewerProfile": "Senior Growth Lead & Native Localization Reviewer",
        "lastReviewedDate": "2026-11-25",
        "slug": "error-verificacion-metodo-pago-meta-ads-solucion",
        "title": "Cómo Solucionar el Error de Verificación de Método de Pago en Meta Ads (2026)",
        "meta_title": "Error de Verificación de Método de Pago en Meta Ads: Solución (2026)",
        "meta_description": "Soluciona el error de verificación de tarjeta en Meta Ads. Resuelve bloqueos 3D Secure, retenciones temporales bancarias y evita suspensiones de cuenta.",
        "primary_keyword": "error verificacion metodo pago meta ads",
        "secondary_keywords": ["meta ads tarjeta rechazada verificacion", "solucion pago meta ads"],
        "excerpt": "Soluciona el error de verificación de tarjeta en Meta Ads: bloqueos 3D Secure, retenciones temporales bancarias y respaldo seguro.",
        "image": "/uploads/meta_ads_payment_method_verification_failed_banner.jpg",
        "read_time": "6 min lectura",
    },
    {
        "translationKey": "3-2-2-dynamic-creative-testing-meta-flexible-ads",
        "sourceSlug": "3-2-2-dynamic-creative-testing-meta-flexible-ads",
        "status": "published",
        "reviewedBy": "Carlos Mendoza",
        "reviewerProfile": "Senior Growth Lead & Native Localization Reviewer",
        "lastReviewedDate": "2026-11-25",
        "slug": "metodo-3-2-2-testing-creativo-meta-ads-anuncios-flexibles",
        "title": "El Motor 3:2:2 de Testing Creativo (DCT) vs. Anuncios Flexibles en Meta Ads (2026)",
        "meta_title": "Método 3:2:2 de Testing Creativo en Meta Ads vs. Anuncios Flexibles (2026)",
        "meta_description": "Domina el framework 3:2:2 en Meta Ads para probar ganchos, visuales y copys sin reiniciar el aprendizaje, extraer Post IDs ganadores y escalar en ASC.",
        "primary_keyword": "metodo 3 2 2 meta ads testing creativo",
        "secondary_keywords": ["testing creativo meta ads", "post id ganador meta ads"],
        "excerpt": "Domina el framework 3:2:2 en Meta Ads para probar ganchos, visuales y copys sin reiniciar el aprendizaje y escalar con Post IDs.",
        "image": "/uploads/2026/10/dct_322_engine_banner.jpg",
        "read_time": "8 min lectura",
    },
    {
        "translationKey": "marketing-attribution-meta-google-amazon-guide",
        "sourceSlug": "marketing-attribution-meta-google-amazon-guide",
        "status": "published",
        "reviewedBy": "Carlos Mendoza",
        "reviewerProfile": "Senior Growth Lead & Native Localization Reviewer",
        "lastReviewedDate": "2026-11-25",
        "slug": "guia-atribucion-marketing-meta-google-amazon",
        "title": "Atribución de Marketing entre Meta, Google y Amazon: Guía Completa (2026)",
        "meta_title": "Atribución de Marketing en Meta, Google y Amazon: Guía 2026",
        "meta_description": "Elimina la doble atribución entre Meta Ads, Google Ads y Amazon. Compara GA4, Triple Whale, Northbeam y Marketing Mix Modeling (MMM) paso a paso.",
        "primary_keyword": "atribucion marketing meta google amazon",
        "secondary_keywords": ["triple whale vs northbeam vs ga4", "mer blended roas atribucion"],
        "excerpt": "Elimina la doble atribución entre Meta Ads, Google Ads y Amazon comparando GA4, Triple Whale, Northbeam y MER/MMM.",
        "image": "/uploads/marketing_attribution_modeling_touchpoints_banner.jpg",
        "read_time": "8 min lectura",
    },
]


def make_en_card_html(p):
    kw = p["primary_keyword"][:30]
    return (
        f'<article class="group rounded-2xl border border-[#E7E7E7] bg-white p-5 sm:p-6 shadow-sm hover:shadow-md hover:border-[#0E56A8] transition-all flex flex-col justify-between">'
        f'<div class="space-y-3"><div class="flex items-center justify-between text-xs text-[#6B7280] font-mono">'
        f'<span class="text-[11px] font-bold text-[#0E56A8] bg-[#F0F6FF] px-2.5 py-0.5 rounded-full border border-[#D0E2FF]">{kw}</span>'
        f'<span class="flex items-center space-x-1"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-clock h-3 w-3 text-[#7E8492]"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg><span>{p["read_time"]}</span></span></div>'
        f'<h3 class="text-lg font-bold text-[#062649] group-hover:text-[#FF6600] transition-colors line-clamp-2 leading-snug"><a href="/{p["slug"]}/">{p["title"]}</a></h3>'
        f'<p class="text-xs text-[#4B5563] line-clamp-3 leading-relaxed">{p["excerpt"]}</p></div>'
        f'<div class="pt-4 border-t border-[#F0F0F0] mt-4 flex items-center justify-between text-xs">'
        f'<div class="flex items-center space-x-1.5 text-[#7E8492] font-mono"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-calendar h-3.5 w-3.5 text-[#0E56A8]"><path d="M8 2v4"></path><path d="M16 2v4"></path><rect width="18" height="18" x="3" y="4" rx="2"></rect><path d="M3 10h18"></path></svg><span>{p["date_label"]}</span></div>'
        f'<a class="inline-flex items-center font-bold text-xs text-[#0E56A8] group-hover:text-[#FF6600] group-hover:translate-x-0.5 transition-all" href="/{p["slug"]}/"><span>Read Playbook</span><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-arrow-right h-3.5 w-3.5 ml-1"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg></a></div></article>'
    )


def make_es_card_html(p):
    kw = p["primary_keyword"][:30]
    return (
        f'<article class="group rounded-2xl border border-[#E7E7E7] bg-white p-5 sm:p-6 shadow-sm hover:shadow-md hover:border-[#0E56A8] transition-all flex flex-col justify-between">'
        f'<div class="space-y-3"><div class="flex items-center justify-between text-xs text-[#6B7280] font-mono">'
        f'<span class="text-[11px] font-bold text-[#0E56A8] bg-[#F0F6FF] px-2.5 py-0.5 rounded-full border border-[#D0E2FF]">{kw}</span>'
        f'<span class="flex items-center space-x-1"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-clock h-3 w-3 text-[#7E8492]"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg><span>{p["read_time"]}</span></span></div>'
        f'<h3 class="text-lg font-bold text-[#062649] group-hover:text-[#FF6600] transition-colors line-clamp-2 leading-snug"><a href="/es/{p["slug"]}/">{p["title"]}</a></h3>'
        f'<p class="text-xs text-[#4B5563] line-clamp-3 leading-relaxed">{p["excerpt"]}</p></div>'
        f'<div class="pt-4 border-t border-[#F0F0F0] mt-4 flex items-center justify-between text-xs">'
        f'<div class="flex items-center space-x-1.5 text-[#7E8492] font-mono"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-calendar h-3.5 w-3.5 text-[#0E56A8]"><path d="M8 2v4"></path><path d="M16 2v4"></path><rect width="18" height="18" x="3" y="4" rx="2"></rect><path d="M3 10h18"></path></svg><span>25 Nov 2026</span></div>'
        f'<a class="inline-flex items-center font-bold text-xs text-[#0E56A8] group-hover:text-[#FF6600] group-hover:translate-x-0.5 transition-all" href="/es/{p["slug"]}/"><span>Leer Guía</span><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-arrow-right h-3.5 w-3.5 ml-1"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg></a></div></article>'
    )


def extract_post_meta_from_live(url, is_es=False):
    """Fetch live article HTML and extract metadata for /blog/ or /es/blog/ indexing."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.encoding = "utf-8"
        if r.status_code != 200:
            return None
        html = r.text
        slug = url.rstrip("/").split("/")[-1]
        t_m = re.search(r"<title>(.*?)</title>", html, re.S)
        d_m = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', html, re.I | re.S)
        img_m = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\'](.*?)["\']', html, re.I | re.S)
        dt_m = re.search(r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})"', html)
        kw_m = re.search(r'<meta[^>]+name=["\']keywords["\'][^>]+content=["\']([^,"\']+)', html, re.I)

        title = t_m.group(1).strip().replace("&amp;", "&") if t_m else slug.replace("-", " ").title()
        desc = d_m.group(1).strip().replace("&amp;", "&") if d_m else ""
        img = "/uploads/2026/11/seo_core_update_banner.jpg"
        if img_m:
            raw_img = img_m.group(1).strip()
            img = raw_img.replace("https://paidmediaworld.com", "")
        pub_date = dt_m.group(1) if dt_m else "2026-11-26"
        from datetime import datetime
        dt_obj = datetime.strptime(pub_date, "%Y-%m-%d")
        date_label = dt_obj.strftime("%b %d, %Y").replace(" 0", " ")
        words = len(re.sub(r"<[^>]+>", " ", html).split())
        mins = max(5, min(15, round(words / 220)))
        kw = kw_m.group(1).strip() if kw_m else ("Marketing Digital" if is_es else "Performance Marketing")

        return {
            "id": abs(hash(slug)) % 900000 + 10000,
            "title": title,
            "slug": slug,
            "date": f"{pub_date}T12:00:00",
            "date_label": date_label,
            "read_time": f"{mins} min lectura" if is_es else f"{mins} min read",
            "excerpt": desc or title,
            "featured_image": img,
            "image": img,
            "categories": [252, 9],
            "tags": [252, 9],
            "meta_title": title,
            "meta_description": desc or title,
            "primary_keyword": kw,
            "content": "",
        }
    except Exception:
        return None


def discover_posts_from_logs():
    """Auto-discover published EN and ES posts from reports/publishing-log-*.json."""
    import glob
    log_files = sorted(glob.glob(r"C:\Users\test\Videos\Personal\reports\publishing-log-*.json"), reverse=True)
    known_en = {p["slug"]: p for p in NEW_EN_POSTS}
    known_es = {p["slug"]: p for p in NEW_ES_POSTS}
    en_posts, es_posts = [], []
    seen_en, seen_es = set(), set()

    for lf in log_files:
        try:
            with open(lf, "r", encoding="utf-8") as f:
                data = json.load(f)
            for art in data.get("deployed_articles", []):
                if art.get("status") != "LIVE":
                    continue
                url = art.get("url", "")
                if not url:
                    continue
                is_es = "/es/" in url
                slug = url.rstrip("/").split("/")[-1]
                if is_es:
                    if slug in seen_es:
                        continue
                    seen_es.add(slug)
                    post = known_es.get(slug) or extract_post_meta_from_live(url, is_es=True)
                    if post:
                        es_posts.append(post)
                else:
                    if slug in seen_en:
                        continue
                    seen_en.add(slug)
                    post = known_en.get(slug) or extract_post_meta_from_live(url, is_es=False)
                    if post:
                        en_posts.append(post)
        except Exception:
            continue

    for p in NEW_EN_POSTS:
        if p["slug"] not in seen_en:
            en_posts.append(p)
            seen_en.add(p["slug"])
    for p in NEW_ES_POSTS:
        if p["slug"] not in seen_es:
            es_posts.append(p)
            seen_es.add(p["slug"])
    return en_posts, es_posts


def inject_into_rsc_posts(html, new_items, slug_key="slug"):
    marker = '\\"posts\\":['
    idx = html.find(marker)
    if idx == -1:
        return html, 0
    insert_at = idx + len(marker)
    existing_slice = html[insert_at:insert_at + 20000]
    to_add = [p for p in new_items if p[slug_key] not in existing_slice]
    if not to_add:
        return html, 0
    serialized = ",".join(
        json.dumps(
            {k: v for k, v in p.items() if k not in ("date_label", "read_time")} if slug_key == "slug" and "id" in p else p,
            ensure_ascii=False,
        ).replace('"', '\\"')
        for p in to_add
    )
    return html[:insert_at] + serialized + "," + html[insert_at:], len(to_add)


def update_en_blog_html(html, posts_list=None):
    posts_list = posts_list or NEW_EN_POSTS
    # 1. Update RSC posts payload
    html, added_rsc = inject_into_rsc_posts(html, posts_list)
    # 2. Update Featured Latest Release to latest post (sync ALL links, dates, read_time, title, excerpt, image)
    latest = posts_list[0]
    feat_s = html.find('<section class="space-y-3">')
    feat_e = html.find("</section>", feat_s) + len("</section>") if feat_s != -1 else -1
    if feat_s != -1 and feat_e != -1:
        feat_block = html[feat_s:feat_e]
        feat_block = re.sub(r"Published <!-- -->[A-Za-z]+ \d+, \d{4}", f'Published <!-- -->{latest["date_label"]}', feat_block, count=1)
        feat_block = re.sub(r'href="/[^"]+/"', f'href="/{latest["slug"]}/"', feat_block)
        feat_block = re.sub(r'src="/uploads/[^"]+"', f'src="{latest["featured_image"]}"', feat_block, count=1)
        feat_block = re.sub(r'alt="[^"]*"', f'alt="{latest["title"]}"', feat_block, count=1)
        feat_block = re.sub(r'(<rect[^>]+></rect><path[^>]+></path></svg><span>)([^<]+)(</span>)', rf'\g<1>{latest["date_label"]}\g<3>', feat_block, count=1)
        feat_block = re.sub(r'(<polyline[^>]+></polyline></svg><span>)([^<]+)(</span>)', rf'\g<1>{latest["read_time"]}\g<3>', feat_block, count=1)
        feat_block = feat_block.replace("â€¢", "&bull;")
        feat_block = re.sub(r'(<h2[^>]*>.*?<a[^>]*>)(.*?)(</a></h2>)', rf'\1{latest["title"]}\3', feat_block, count=1, flags=re.S)
        feat_block = re.sub(r'(<p class="text-xs sm:text-sm[^"]*">)(.*?)(</p>)', rf'\1{latest["excerpt"]}\3', feat_block, count=1, flags=re.S)
        html = html[:feat_s] + feat_block + html[feat_e:]
    # 3. Prepend new cards to SSR grid
    feat_end = html.find("</section>", html.find('<section class="space-y-3">'))
    grid_idx = html.find('<div class="grid grid-cols-1 md:grid-cols-2', feat_end)
    if grid_idx != -1:
        first_art = html.find("<article", grid_idx)
        to_prepend = [p for p in posts_list[1:] if f'href="/{p["slug"]}/"' not in html[grid_idx:grid_idx + 20000]]
        if to_prepend:
            cards = "".join(make_en_card_html(p) for p in to_prepend)
            html = html[:first_art] + cards + html[first_art:]
    return html, added_rsc


def update_es_blog_html(html, posts_list=None):
    posts_list = posts_list or NEW_ES_POSTS
    html, added_rsc = inject_into_rsc_posts(html, posts_list)
    first_art = html.find("<article")
    if first_art != -1:
        to_prepend = [p for p in posts_list if f'href="/es/{p["slug"]}/"' not in html[:first_art + 12000]]
        if to_prepend:
            cards = "".join(make_es_card_html(p) for p in to_prepend)
            html = html[:first_art] + cards + html[first_art:]
    return html, added_rsc


def sync_blog_indexes(new_en_posts=None, new_es_posts=None):
    auto_en, auto_es = discover_posts_from_logs()
    if new_en_posts:
        seen = {p["slug"] for p in new_en_posts}
        new_en_posts = list(new_en_posts) + [p for p in auto_en if p["slug"] not in seen]
    else:
        new_en_posts = auto_en
    if new_es_posts:
        seen = {p["slug"] for p in new_es_posts}
        new_es_posts = list(new_es_posts) + [p for p in auto_es if p["slug"] not in seen]
    else:
        new_es_posts = auto_es

    en_resp = requests.get("https://paidmediaworld.com/blog/", headers=HEADERS, timeout=25)
    en_resp.encoding = "utf-8"
    es_resp = requests.get("https://paidmediaworld.com/es/blog/", headers=HEADERS, timeout=25)
    es_resp.encoding = "utf-8"

    en_new, en_added = update_en_blog_html(en_resp.text, new_en_posts)
    es_new, es_added = update_es_blog_html(es_resp.text, new_es_posts)
    print(f"Prepared /blog/ (+{en_added} RSC posts, total pool {len(new_en_posts)}) and /es/blog/ (+{es_added} RSC posts)")

    s = requests.Session()
    r = s.post(
        f"https://{CP_HOST}:{CP_PORT}/login/?login_only=1",
        data={"user": CP_USER, "pass": CP_PASS},
        verify=False,
        timeout=20,
    )
    tok = r.json().get("security_token")
    if not tok:
        raise RuntimeError(f"cPanel auth failed: {r.text}")

    upload_url = f"https://{CP_HOST}:{CP_PORT}{tok}/execute/Fileman/upload_files"
    for remote_dir, content in [
        ("public_html/paidmediaworld/blog", en_new),
        ("public_html/paidmediaworld/es/blog", es_new),
    ]:
        res = s.post(
            upload_url,
            data={"dir": remote_dir, "overwrite": "1"},
            files={"file-0": ("index.html", content.encode("utf-8"))},
            verify=False,
            timeout=30,
        ).json()
        print(f"Uploaded {remote_dir}/index.html -> status={res.get('status')} err={res.get('errors')}")

    # Verify live
    for u, needle in [
        ("https://paidmediaworld.com/blog/", "wiring-marketing-mcp-servers-google-ads-meta-ga4-safety"),
        ("https://paidmediaworld.com/es/blog/", "rastrear-leads-whatsapp-ga4-google-tag-manager"),
    ]:
        chk = requests.get(u, headers=HEADERS, timeout=20)
        chk.encoding = "utf-8"
        print(f"Verify {u}: HTTP {chk.status_code} | contains latest? {needle in chk.text}")

    # Submit to IndexNow & Google Indexing
    urls = ["https://paidmediaworld.com/blog/", "https://paidmediaworld.com/es/blog/"]
    try:
        idx = requests.post(
            "https://api.indexnow.org/indexnow",
            json={"host": "paidmediaworld.com", "key": INDEXNOW_KEY, "keyLocation": f"https://paidmediaworld.com/{INDEXNOW_KEY}.txt", "urlList": urls},
            headers={"Content-Type": "application/json"},
            timeout=10,
        )
        print("IndexNow HTTP:", idx.status_code)
    except Exception as e:
        print("IndexNow err:", e)

    try:
        sys.path.append(r"C:\Users\test\Videos\Personal\scripts")
        from submit_indexing import submit_url
        for u in urls:
            submit_url(SERVICE_ACCOUNT_PATH, u, action="URL_UPDATED")
            print("Google Indexing OK:", u)
    except Exception as e:
        print("Google Indexing err:", e)


if __name__ == "__main__":
    sync_blog_indexes()
