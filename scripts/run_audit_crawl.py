import csv
import json
import re
import time
from urllib.parse import urljoin, urlparse, urldefrag
import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "SEO-Audit-Bot/1.0 (+contact: client-audit)"}
DELAY = 0.6
HOST = "victoryhcspl.com"

# 1. Fetch robots.txt and sitemaps
print("Step 1: Checking robots.txt & Sitemaps...")
robots_url = "https://victoryhcspl.com/robots.txt"
r_robots = requests.get(robots_url, headers=HEADERS, allow_redirects=False)
print(f"robots.txt status: {r_robots.status_code}, Location: {r_robots.headers.get('Location')}")

sitemap_root = "https://victoryhcspl.com/sitemap.xml"
r_sitemap = requests.get(sitemap_root, headers=HEADERS, timeout=15)
soup_sitemap = BeautifulSoup(r_sitemap.content, "xml")

sitemap_urls = set()
# check if it's index or urlset
for sm in soup_sitemap.find_all("sitemap"):
    loc = sm.find("loc")
    if loc:
        sub_url = loc.text.strip()
        print(f"Fetching sub-sitemap: {sub_url}")
        r_sub = requests.get(sub_url, headers=HEADERS, timeout=15)
        soup_sub = BeautifulSoup(r_sub.content, "xml")
        for u in soup_sub.find_all("url"):
            l = u.find("loc")
            if l:
                sitemap_urls.add(l.text.strip())

for u in soup_sitemap.find_all("url"):
    l = u.find("loc")
    if l:
        sitemap_urls.add(l.text.strip())

print(f"Discovered {len(sitemap_urls)} URLs from XML sitemaps:")
for u in sorted(sitemap_urls):
    print(" -", u)

# 2. Get WP REST API URLs
print("\nStep 2: Checking WordPress REST API...")
wp_urls = set()
try:
    r_pages = requests.get("https://victoryhcspl.com/wp-json/wp/v2/pages?per_page=100", headers=HEADERS, timeout=15)
    if r_pages.status_code == 200:
        for p in r_pages.json():
            wp_urls.add(p.get("link"))
except Exception as e:
    print(f"WP API error: {e}")
print(f"Discovered {len(wp_urls)} URLs from WP REST API")

# 3. Read Screaming Frog internal_html.csv
sf_urls = set()
sf_path = r"website audit\victoryhcspl.com\internal_html.csv"
try:
    with open(sf_path, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        for r in reader:
            addr_key = [k for k in r.keys() if "Address" in k][0]
            sf_urls.add(r.get(addr_key))
except Exception as e:
    print(f"Error reading SF csv: {e}")
print(f"Discovered {len(sf_urls)} URLs from Screaming Frog export")

# 4. Master URL crawl queue
all_seeds = set(sitemap_urls) | set(wp_urls) | set(sf_urls) | {
    "https://victoryhcspl.com/",
    "https://victoryhcspl.com/healthcare-training/",
    "https://victoryhcspl.com/home/"
}

# Crawl all seeds and discover internal links
def norm(u):
    u, _ = urldefrag(u)
    return u

crawled_data = {}
link_graph = []
crawled_urls = set()
queue = list(all_seeds)

print(f"\nStep 3: Crawling {len(queue)} seed URLs + discovering links...")

while queue:
    current_url = queue.pop(0)
    if current_url in crawled_urls:
        continue
    crawled_urls.add(current_url)

    t0 = time.time()
    try:
        resp = requests.get(current_url, headers=HEADERS, timeout=20, allow_redirects=True)
        resp_time = round(time.time() - t0, 3)
    except Exception as e:
        print(f"Error fetching {current_url}: {e}")
        crawled_data[current_url] = {
            "url": current_url,
            "final_url": current_url,
            "status": f"ERR: {e}",
            "resp_time": 0,
            "redirects": "",
            "html_bytes": 0
        }
        continue

    final_url = resp.url
    status_code = resp.status_code
    redirects = " > ".join([f"{h.status_code}:{h.url}" for h in resp.history]) if resp.history else "None"
    content_type = resp.headers.get("Content-Type", "")
    html_bytes = len(resp.content)

    row = {
        "url": current_url,
        "final_url": final_url,
        "status": status_code,
        "redirects": redirects,
        "resp_time": resp_time,
        "content_type": content_type,
        "html_bytes": html_bytes,
        "title": "",
        "title_len": 0,
        "meta_desc": "",
        "meta_desc_len": 0,
        "canonical": "",
        "robots_meta": "",
        "x_robots": resp.headers.get("X-Robots-Tag", ""),
        "h1_count": 0,
        "h1": "",
        "h2_count": 0,
        "h2_list": "",
        "h3_count": 0,
        "words": 0,
        "lang": "",
        "hreflang": 0,
        "og_title": "",
        "og_desc": "",
        "og_image": "",
        "viewport": "",
        "imgs": 0,
        "imgs_no_alt": 0,
        "schema_types": "",
        "phone_count": 0,
        "email_count": 0,
        "whatsapp_present": False,
        "form_count": 0,
        "cta_text": ""
    }

    if "text/html" in content_type:
        soup = BeautifulSoup(resp.text, "lxml")
        title_el = soup.find("title")
        if title_el:
            row["title"] = title_el.get_text(strip=True)
            row["title_len"] = len(row["title"])

        meta_desc = soup.find("meta", attrs={"name": re.compile(r"^description$", re.I)})
        if meta_desc and meta_desc.get("content"):
            row["meta_desc"] = meta_desc["content"].strip()
            row["meta_desc_len"] = len(row["meta_desc"])

        canon = soup.find("link", attrs={"rel": "canonical"})
        if canon and canon.get("href"):
            row["canonical"] = canon["href"].strip()

        rmeta = soup.find("meta", attrs={"name": re.compile(r"^robots$", re.I)})
        if rmeta and rmeta.get("content"):
            row["robots_meta"] = rmeta["content"].strip()

        h1s = [h.get_text(" ", strip=True) for h in soup.find_all("h1")]
        row["h1_count"] = len(h1s)
        row["h1"] = " | ".join(h1s)

        h2s = [h.get_text(" ", strip=True) for h in soup.find_all("h2")]
        row["h2_count"] = len(h2s)
        row["h2_list"] = " | ".join(h2s[:10])

        h3s = [h.get_text(" ", strip=True) for h in soup.find_all("h3")]
        row["h3_count"] = len(h3s)

        # Main content words
        # Remove scripts, styles
        for s in soup(["script", "style", "noscript", "svg"]):
            s.decompose()
        main = soup.find("main") or soup.find("article") or soup.body or soup
        body_text = main.get_text(" ", strip=True) if main else ""
        row["words"] = len(re.findall(r"\w+", body_text))

        row["lang"] = soup.html.get("lang", "") if soup.html else ""
        row["hreflang"] = len(soup.find_all("link", rel="alternate", hreflang=True))

        og_t = soup.find("meta", property="og:title")
        row["og_title"] = og_t["content"].strip() if og_t and og_t.get("content") else ""

        og_d = soup.find("meta", property="og:description")
        row["og_desc"] = og_d["content"].strip() if og_d and og_d.get("content") else ""

        og_i = soup.find("meta", property="og:image")
        row["og_image"] = og_i["content"].strip() if og_i and og_i.get("content") else ""

        vp = soup.find("meta", attrs={"name": "viewport"})
        row["viewport"] = vp["content"].strip() if vp and vp.get("content") else ""

        imgs = soup.find_all("img")
        row["imgs"] = len(imgs)
        row["imgs_no_alt"] = sum(1 for i in imgs if not i.get("alt") or not i.get("alt").strip())

        # Schema JSON-LD
        schemas = []
        for s in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(s.string or "{}")
                items = data if isinstance(data, list) else data.get("@graph", [data])
                for it in items:
                    if isinstance(it, dict) and "@type" in it:
                        schemas.append(it["@type"])
            except Exception:
                schemas.append("INVALID_JSON")
        row["schema_types"] = "|".join(schemas)

        # CTAs, contact
        page_str = resp.text
        phones = re.findall(r"(?:\+91[\s-]?)?[6-9]\d{9}", page_str)
        emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", page_str)
        row["phone_count"] = len(set(phones))
        row["email_count"] = len(set(emails))
        row["whatsapp_present"] = "wa.me" in page_str or "api.whatsapp.com" in page_str or "whatsapp" in page_str.lower()
        forms = soup.find_all("form")
        row["form_count"] = len(forms)

        # Links extraction
        for a in soup.find_all("a", href=True):
            raw_href = a["href"].strip()
            anchor_text = a.get_text(" ", strip=True)
            rel = a.get("rel", [])
            follow = "nofollow" if "nofollow" in rel else "follow"
            target_full = urljoin(current_url, raw_href)
            target_norm = norm(target_full)

            link_graph.append({
                "source": current_url,
                "target": target_norm,
                "anchor": anchor_text,
                "follow": follow
            })

            # Check if internal and new
            parsed_t = urlparse(target_norm)
            if parsed_t.netloc == HOST or parsed_t.netloc == f"www.{HOST}":
                if target_norm not in crawled_urls and target_norm not in queue:
                    # ignore non-html static resources or fragments
                    ext = target_norm.split(".")[-1].lower() if "." in target_norm.split("/")[-1] else ""
                    if ext not in ["jpg", "jpeg", "png", "gif", "pdf", "zip", "css", "js", "svg", "webp"]:
                        queue.append(target_norm)

    crawled_data[current_url] = row
    print(f"[{status_code}] {current_url} -> Title: {row['title'][:30]} | H1s: {row['h1_count']} | Words: {row['words']}")
    time.sleep(DELAY)

# 5. Build 01_url_inventory.csv
print("\nStep 4: Writing 01_url_inventory.csv...")
all_inventory_urls = sorted(list(crawled_urls | set(crawled_data.keys())))
inventory_rows = []
for u in all_inventory_urls:
    in_sitemap = u in sitemap_urls
    in_crawl = u in crawled_data
    source = "both" if (in_sitemap and in_crawl) else ("sitemap-only" if in_sitemap else "crawl-only")
    
    cd = crawled_data.get(u, {})
    sc = cd.get("status", "Not Crawled")
    final_u = cd.get("final_url", u)
    content_t = cd.get("content_type", "")
    
    # URL type classification
    url_p = urlparse(u).path
    if u.endswith("/#!"):
        url_type = "AJAX Crawling Scheme / Fragment"
    elif url_p in ["", "/"]:
        url_type = "Homepage"
    elif "wp-content" in u or "cht-front-script" in u:
        url_type = "Asset / Script"
    elif "/healthcare-training" in u:
        url_type = "Primary Service Page"
    elif url_p.startswith("/category") or url_p.startswith("/tag") or url_p.startswith("/author"):
        url_type = "Archive"
    else:
        url_type = "Supporting Page"

    inventory_rows.append({
        "url": u,
        "final_url": final_u,
        "status_code": sc,
        "url_type": url_type,
        "source": source,
        "in_sitemap": in_sitemap,
        "in_crawl": in_crawl
    })

# Save files in website audit/victoryhcspl.com/ and root
out_dirs = [r"website audit\victoryhcspl.com", "."]

for d in out_dirs:
    p_inv = f"{d}/01_url_inventory.csv"
    with open(p_inv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["url", "final_url", "status_code", "url_type", "source", "in_sitemap", "in_crawl"])
        writer.writeheader()
        writer.writerows(inventory_rows)

    # 6. Build 02_page_data.csv
    p_data = f"{d}/02_page_data.csv"
    field_order = [
        "url", "final_url", "status", "redirects", "resp_time", "html_bytes",
        "title", "title_len", "meta_desc", "meta_desc_len", "canonical",
        "robots_meta", "x_robots", "h1_count", "h1", "h2_count", "h2_list",
        "h3_count", "words", "lang", "hreflang", "og_title", "og_desc", "og_image",
        "viewport", "imgs", "imgs_no_alt", "schema_types", "phone_count",
        "email_count", "whatsapp_present", "form_count"
    ]
    with open(p_data, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=field_order, extrasaction="ignore")
        writer.writeheader()
        for u in all_inventory_urls:
            if u in crawled_data:
                writer.writerow(crawled_data[u])

    # 7. Build 03_link_graph.csv
    p_graph = f"{d}/03_link_graph.csv"
    with open(p_graph, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["source", "target", "anchor", "follow"])
        writer.writeheader()
        writer.writerows(link_graph)

print("Finished Crawl & Data Extraction successfully!")
print(f"Total inventory URLs: {len(inventory_rows)}")
print(f"Total link edges: {len(link_graph)}")
