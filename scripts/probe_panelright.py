import requests
from bs4 import BeautifulSoup
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'}

urls = [
    'https://www.panelright.com/',
    'https://www.panelright.com/faq',
    'https://www.panelright.com/efficiency',
    'https://solutions.panelright.com/contact',
    'https://www.panelright.com/robots.txt',
    'https://www.panelright.com/sitemap.xml',
    'http://panelright.com/',
    'https://panelright.com/',
    'http://www.panelright.com/'
]

print("=== 1. STATUS & REDIRECTS ===")
for u in urls:
    try:
        r = requests.get(u, headers=headers, timeout=10, allow_redirects=False)
        loc = r.headers.get("Location", "")
        ct = r.headers.get("Content-Type", "")[:35]
        srv = r.headers.get("Server", "")
        print(f"[{r.status_code}] {u} -> Loc: {loc} | CT: {ct} | Server: {srv}")
    except Exception as e:
        print(f"[ERR] {u} -> {e}")

print("\n=== 2. ROBOTS.TXT CONTENT ===")
try:
    r_rob = requests.get('https://www.panelright.com/robots.txt', headers=headers, timeout=10)
    print(r_rob.text)
except Exception as e:
    print("robots.txt error:", e)

print("\n=== 3. SITEMAP.XML CONTENT ===")
try:
    r_sm = requests.get('https://www.panelright.com/sitemap.xml', headers=headers, timeout=10)
    print("Sitemap status:", r_sm.status_code)
    print(r_sm.text[:500])
except Exception as e:
    print("sitemap.xml error:", e)
