import os
import re
import sys
import requests
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import deploy_three_articles as d3
import deploy_nov24_articles as d24
import deploy_nov25_articles as d25
from pmw_article_template import build_pmw_article_html
from fix_post_nov20_posts import IMAGE_MAP

load_dotenv(r"C:\Users\test\Videos\Personal\.env")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://paidmediaworld.com/",
}


def rebuild_d3_article(art):
    html = art["html"]
    slug = art["slug"]
    title = art["title"]
    d_m = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)["\']', html, re.I)
    desc = d_m.group(1).strip() if d_m else title
    kw_m = re.search(r'<span class="truncate max-w-\[260px\] text-gray-800">(.*?)</span>', html, re.S)
    kw = kw_m.group(1).strip() if kw_m else "performance marketing"
    rt_m = re.search(r'<span>(\d+ min read)</span>', html)
    rt = rt_m.group(1) if rt_m else "8 min read"
    dt_m = re.search(r'<span>(November \d+, 2026)</span>', html)
    dt = dt_m.group(1) if dt_m else "November 24, 2026"
    body_m = re.search(r'<article class="article-body">\s*(.*?)\s*</article>', html, re.S)
    body = body_m.group(1).strip() if body_m else ""
    if not body:
        raise ValueError(f"Empty body in d3 article {slug}")
    img = IMAGE_MAP.get(slug, "/uploads/2026/09/geo_ai_search_visibility_banner.jpg")
    return build_pmw_article_html(
        title=title,
        slug=slug,
        primary_kw=kw,
        category="Performance Marketing",
        description=desc,
        read_time=rt,
        publish_date=dt,
        body_content=body,
        featured_image=img,
    )


def main():
    s, tok = d24.get_cpanel_session()
    upload_url = f"https://paidmediaworld.com:2083{tok}/execute/Fileman/upload_files"

    repaired = []
    for art in d3.generate_articles():
        repaired.append({"slug": art["slug"], "title": art["title"], "html": rebuild_d3_article(art)})

    for art in d24.generate_articles() + d25.generate_articles():
        slug = art["slug"]
        html = art["html"]
        # Ensure verified IMAGE_MAP banner is used
        target_img = IMAGE_MAP.get(slug)
        if target_img:
            html = re.sub(r'/uploads/[^"\']+\.jpg', target_img, html)
        repaired.append({"slug": slug, "title": art["title"], "html": html})

    print(f"Uploading {len(repaired)} repaired EN articles to cPanel...")
    for art in repaired:
        slug = art["slug"]
        res = s.post(
            upload_url,
            data={"dir": f"public_html/paidmediaworld/{slug}", "overwrite": "1"},
            files={"file-0": ("index.html", art["html"].encode("utf-8"))},
            verify=False,
            timeout=25,
        ).json()
        print(f"  Upload {slug}: status={res.get('status')}")

    print("\nVerifying all 9 repaired live pages...")
    for art in repaired:
        slug = art["slug"]
        url = f"https://paidmediaworld.com/{slug}/"
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.encoding = "utf-8"
        has_follow = "Follow:" in r.text
        m = re.search(r'<div class="article-content[^>]*>(.*?)</div>\s*<section', r.text, re.S)
        body_chars = len(m.group(1).strip()) if m else 0
        print(f"  [{r.status_code}] /{slug}/ | Follow_bug={has_follow} | body_chars={body_chars}")

    # Also check ES Nov 25 posts quickly
    for es_slug in [
        "rastrear-leads-whatsapp-ga4-google-tag-manager",
        "error-verificacion-metodo-pago-meta-ads-solucion",
        "metodo-3-2-2-testing-creativo-meta-ads-anuncios-flexibles",
        "guia-atribucion-marketing-meta-google-amazon",
    ]:
        r = requests.get(f"https://paidmediaworld.com/es/{es_slug}/", headers=HEADERS, timeout=15)
        m = re.search(r'<div class="article-content[^>]*>(.*?)</div>\s*<section', r.text, re.S)
        print(f"  [ES {r.status_code}] /es/{es_slug}/ | Follow_bug={'Follow:' in r.text} | body_chars={len(m.group(1).strip()) if m else 0}")


if __name__ == "__main__":
    main()
