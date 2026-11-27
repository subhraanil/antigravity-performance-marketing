import requests
from bs4 import BeautifulSoup
import re
import csv

HEADERS = {"User-Agent": "SEO-Audit-Bot/1.0 (+contact: client-audit)"}

canonical_urls = [
    "https://victoryhcspl.com/",
    "https://victoryhcspl.com/healthcare-training/",
    "https://victoryhcspl.com/his-ris-pacs/",
    "https://victoryhcspl.com/infra-management/",
    "https://victoryhcspl.com/consulting/",
    "https://victoryhcspl.com/about-us/",
    "https://victoryhcspl.com/clientele/",
    "https://victoryhcspl.com/careers/",
    "https://victoryhcspl.com/gallery/",
    "https://victoryhcspl.com/contact-us/"
]

pages_summary = []

for u in canonical_urls:
    r = requests.get(u, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(r.text, "lxml")
    
    title = soup.title.get_text(strip=True) if soup.title else ""
    meta_d = soup.find("meta", attrs={"name": re.compile(r"^description$", re.I)})
    meta_desc = meta_d.get("content", "").strip() if meta_d else ""
    
    h1s = [h.get_text(" ", strip=True) for h in soup.find_all("h1")]
    h2s = [h.get_text(" ", strip=True) for h in soup.find_all("h2")]
    
    # Clean text for words
    for s in soup(["script", "style", "noscript", "svg"]):
        s.decompose()
    body_text = soup.get_text(" ", strip=True)
    words = len(re.findall(r"\w+", body_text))
    
    imgs = soup.find_all("img")
    imgs_no_alt = [img.get("src", "") for img in imgs if not img.get("alt") or not img.get("alt").strip()]
    
    pages_summary.append({
        "url": u,
        "title": title,
        "title_len": len(title),
        "meta_desc": meta_desc,
        "meta_len": len(meta_desc),
        "h1_count": len(h1s),
        "h1": " | ".join(h1s),
        "h2_count": len(h2s),
        "words": words,
        "imgs": len(imgs),
        "imgs_no_alt_count": len(imgs_no_alt)
    })

print(f"{'URL':<45} | {'Title Len':<9} | {'Meta Len':<8} | {'H1s':<3} | {'Words':<5} | {'NoAlt':<5}")
print("-" * 85)
for p in pages_summary:
    slug = p['url'].replace("https://victoryhcspl.com", "")
    if not slug: slug = "/"
    print(f"{slug:<45} | {p['title_len']:<9} | {p['meta_len']:<8} | {p['h1_count']:<3} | {p['words']:<5} | {p['imgs_no_alt_count']:<5}")
    print(f"   Title: {p['title']}")
    print(f"   H1: {p['h1'] if p['h1'] else '[MISSING H1]'}")
    print(f"   Meta: {p['meta_desc'][:70]}...")
    print()
