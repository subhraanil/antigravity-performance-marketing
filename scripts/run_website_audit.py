#!/usr/bin/env python3
"""
Automated Technical SEO & Website Audit Engine
Universal CLI tool for executing evidence-based audits on any client website.

Usage:
  python scripts/run_website_audit.py --url https://example.com/ --service https://example.com/service/ --country India --out "website audit/example.com"
"""

import argparse
import csv
import datetime
import json
import os
import re
import socket
import ssl
import sys
import time
from urllib.parse import urljoin, urlparse, urldefrag
import requests
from bs4 import BeautifulSoup

try:
    import docx
    from docx.shared import Inches, Pt, RGBColor
    from docx.enum.table import WD_TABLE_ALIGNMENT
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False

HEADERS = {"User-Agent": "SEO-Audit-Bot/1.0 (+contact: client-audit)"}
DELAY = 0.5


def normalize_url(u):
    u, _ = urldefrag(u)
    return u.rstrip("/") if urlparse(u).path not in ("", "/") else u


def run_audit(target_url, service_url, target_country, crawl_cap, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    parsed_root = urlparse(target_url)
    root_host = parsed_root.netloc
    audit_date = datetime.datetime.now().strftime("%B %d, %Y")

    print(f"\n=======================================================")
    print(f" Starting Technical SEO Audit for: {target_url}")
    print(f" Primary Service Focus: {service_url}")
    print(f" Target Country: {target_country} | Crawl Cap: {crawl_cap}")
    print(f" Output Directory: {output_dir}")
    print(f"=======================================================\n")

    # 1. Robots & Sitemaps Discovery
    print("[Phase 1] Probing robots.txt & Sitemaps...")
    robots_url = urljoin(target_url, "/robots.txt")
    sitemap_urls = set()
    robots_status = "Not Checked"
    robots_redirects = False

    try:
        r_rob = requests.get(robots_url, headers=HEADERS, allow_redirects=False, timeout=10)
        robots_status = r_rob.status_code
        if r_rob.is_redirect or r_rob.is_permanent_redirect:
            robots_redirects = True
            print(f"  [!] robots.txt redirects ({r_rob.status_code}) to: {r_rob.headers.get('Location')}")
    except Exception as e:
        print(f"  [!] robots.txt fetch error: {e}")

    # Common sitemap paths
    sitemap_probes = ["/sitemap.xml", "/sitemap_index.xml", "/wp-sitemap.xml", "/page-sitemap.xml"]
    for sp in sitemap_probes:
        sm_url = urljoin(target_url, sp)
        try:
            r_sm = requests.get(sm_url, headers=HEADERS, timeout=10)
            if r_sm.status_code == 200 and ("xml" in r_sm.headers.get("Content-Type", "") or "text" in r_sm.headers.get("Content-Type", "")):
                soup_sm = BeautifulSoup(r_sm.content, "xml")
                # Check for sitemap index
                sub_sms = [s.find("loc").text.strip() for s in soup_sm.find_all("sitemap") if s.find("loc")]
                if sub_sms:
                    for sub in sub_sms:
                        try:
                            r_sub = requests.get(sub, headers=HEADERS, timeout=10)
                            soup_sub = BeautifulSoup(r_sub.content, "xml")
                            for u_node in soup_sub.find_all("url"):
                                loc = u_node.find("loc")
                                if loc: sitemap_urls.add(loc.text.strip())
                        except:
                            pass
                for u_node in soup_sm.find_all("url"):
                    loc = u_node.find("loc")
                    if loc: sitemap_urls.add(loc.text.strip())
                print(f"  [+] Found active sitemap: {sm_url} (Found {len(sitemap_urls)} URLs)")
                break
        except Exception:
            pass

    # 2. REST API probe
    api_urls = set()
    wp_api = urljoin(target_url, "/wp-json/wp/v2/pages?per_page=100")
    try:
        r_api = requests.get(wp_api, headers=HEADERS, timeout=10)
        if r_api.status_code == 200:
            for item in r_api.json():
                if item.get("link"): api_urls.add(item.get("link"))
            print(f"  [+] Discovered {len(api_urls)} URLs via WordPress REST API")
    except Exception:
        pass

    # 3. Security & SSL Inspection
    print("\n[Phase 3] Checking SSL, TLS & Security Headers...")
    ssl_info = {}
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=root_host) as s:
            s.connect((root_host, 443))
            cert = s.getpeercert()
            ssl_info["tls_version"] = s.version()
            ssl_info["cipher"] = s.cipher()[0]
            ssl_info["issuer"] = dict(x[0] for x in cert.get("issuer", []))
            ssl_info["expiry"] = cert.get("notAfter")
            exp_date = datetime.datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
            ssl_info["days_left"] = (exp_date - datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)).days
            print(f"  [+] TLS Version: {ssl_info['tls_version']} | Expiry in {ssl_info['days_left']} days")
    except Exception as e:
        print(f"  [!] SSL Check error: {e}")

    # Security headers on homepage
    sec_headers = {}
    server_tokens = {}
    try:
        r_home = requests.get(target_url, headers=HEADERS, timeout=15)
        for h in ["Strict-Transport-Security", "Content-Security-Policy", "X-Frame-Options", "X-Content-Type-Options", "Referrer-Policy"]:
            sec_headers[h] = r_home.headers.get(h, "[MISSING]")
        server_tokens["Server"] = r_home.headers.get("Server", "Unknown")
        server_tokens["X-Powered-By"] = r_home.headers.get("X-Powered-By", "None")
    except Exception as e:
        print(f"  [!] Header check error: {e}")

    # 4. Crawl Execution
    print(f"\n[Phase 2] Crawling internal pages (Cap: {crawl_cap})...")
    seeds = sorted(list(set([normalize_url(target_url), normalize_url(service_url)] | sitemap_urls | api_urls)))
    queue = list(seeds)
    crawled_data = {}
    crawled_urls = set()
    link_graph = []

    while queue and len(crawled_urls) < crawl_cap:
        curr = queue.pop(0)
        if curr in crawled_urls: continue
        crawled_urls.add(curr)

        t0 = time.time()
        try:
            resp = requests.get(curr, headers=HEADERS, timeout=15, allow_redirects=True)
            ttfb = round(time.time() - t0, 3)
        except Exception as e:
            crawled_data[curr] = {"url": curr, "final_url": curr, "status": f"ERR: {e}", "resp_time": 0}
            continue

        ct = resp.headers.get("Content-Type", "")
        row = {
            "url": curr, "final_url": resp.url, "status": resp.status_code,
            "resp_time": ttfb, "content_type": ct, "html_bytes": len(resp.content),
            "title": "", "meta_desc": "", "canonical": "", "h1_count": 0, "h1": "",
            "h2_count": 0, "words": 0, "imgs": 0, "imgs_no_alt": 0, "forms": 0
        }

        if "text/html" in ct:
            soup = BeautifulSoup(resp.text, "lxml")
            if soup.title: row["title"] = soup.title.get_text(strip=True)
            m_desc = soup.find("meta", attrs={"name": re.compile(r"^description$", re.I)})
            if m_desc and m_desc.get("content"): row["meta_desc"] = m_desc["content"].strip()
            canon = soup.find("link", rel="canonical")
            if canon and canon.get("href"): row["canonical"] = canon["href"].strip()

            h1s = [h.get_text(" ", strip=True) for h in soup.find_all("h1")]
            row["h1_count"] = len(h1s)
            row["h1"] = " | ".join(h1s)
            row["h2_count"] = len(soup.find_all("h2"))

            for s in soup(["script", "style", "noscript", "svg"]): s.decompose()
            body_txt = soup.get_text(" ", strip=True)
            row["words"] = len(re.findall(r"\w+", body_txt))

            imgs = soup.find_all("img")
            row["imgs"] = len(imgs)
            row["imgs_no_alt"] = sum(1 for i in imgs if not i.get("alt") or not i.get("alt").strip())
            row["forms"] = len(soup.find_all("form"))

            for a in soup.find_all("a", href=True):
                target_norm = normalize_url(urljoin(curr, a["href"].strip()))
                link_graph.append({
                    "source": curr, "target": target_norm,
                    "anchor": a.get_text(" ", strip=True),
                    "follow": "nofollow" if "nofollow" in a.get("rel", []) else "follow"
                })
                if urlparse(target_norm).netloc == root_host and target_norm not in crawled_urls and target_norm not in queue:
                    ext = target_norm.split(".")[-1].lower() if "." in target_norm.split("/")[-1] else ""
                    if ext not in ["jpg", "jpeg", "png", "gif", "pdf", "zip", "css", "js", "svg", "webp"]:
                        queue.append(target_norm)

        crawled_data[curr] = row
        print(f"  [{row['status']}] {curr} (H1s: {row['h1_count']}, Words: {row['words']}, Forms: {row['forms']})")
        time.sleep(DELAY)

    # 5. Output Deliverables
    print(f"\n[Phase 4] Writing deliverables to: {output_dir}...")

    # 01_url_inventory.csv
    with open(os.path.join(output_dir, "01_url_inventory.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["url", "final_url", "status_code", "in_sitemap", "in_crawl"])
        w.writeheader()
        for u, d in crawled_data.items():
            w.writerow({
                "url": u, "final_url": d.get("final_url", u), "status_code": d.get("status", ""),
                "in_sitemap": u in sitemap_urls, "in_crawl": u in crawled_data
            })

    # 02_page_data.csv
    with open(os.path.join(output_dir, "02_page_data.csv"), "w", newline="", encoding="utf-8") as f:
        fields = ["url", "final_url", "status", "resp_time", "html_bytes", "title", "meta_desc", "canonical", "h1_count", "h1", "h2_count", "words", "imgs", "imgs_no_alt", "forms"]
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for d in crawled_data.values():
            w.writerow(d)

    # 03_link_graph.csv
    with open(os.path.join(output_dir, "03_link_graph.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["source", "target", "anchor", "follow"])
        w.writeheader()
        w.writerows(link_graph)

    print("\n[+] Technical SEO Audit Engine completed successfully!")
    print(f"    Total inventoried pages: {len(crawled_data)}")
    print(f"    Total internal link edges: {len(link_graph)}")
    print(f"    Deliverables ready in: {output_dir}")


def main():
    parser = argparse.ArgumentParser(description="Automated Technical SEO & Website Audit Engine")
    parser.add_argument("--url", required=True, help="Target client homepage URL (e.g. https://example.com/)")
    parser.add_argument("--service", required=True, help="Target primary service/conversion page URL")
    parser.add_argument("--country", default="India", help="Target country market (default: India)")
    parser.add_argument("--cap", type=int, default=500, help="Maximum crawl depth/cap (default: 500)")
    parser.add_argument("--out", default="website audit/output", help="Output directory path")
    args = parser.parse_args()

    run_audit(args.url, args.service, args.country, args.cap, args.out)


if __name__ == "__main__":
    main()
