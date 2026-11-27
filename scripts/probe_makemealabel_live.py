import requests
from bs4 import BeautifulSoup
import json
import ssl
import socket
import datetime

BASE_URL = "https://makemealabel.com"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

print("=== 1. ROBOTS.TXT & SITEMAPS ===")
try:
    r_rob = requests.get(f"{BASE_URL}/robots.txt", headers=HEADERS, timeout=10)
    print("robots.txt Status:", r_rob.status_code)
    print("robots.txt Content Preview:\n", "\n".join(r_rob.text.splitlines()[:25]))
except Exception as e:
    print("robots.txt Error:", e)

try:
    r_sm = requests.get(f"{BASE_URL}/sitemap.xml", headers=HEADERS, timeout=10)
    print("\nsitemap.xml Status:", r_sm.status_code)
    if r_sm.status_code == 200:
        soup_sm = BeautifulSoup(r_sm.content, "xml")
        sitemaps = [s.text.strip() for s in soup_sm.find_all("loc")]
        print("Sitemaps referenced:", sitemaps)
except Exception as e:
    print("sitemap.xml Error:", e)

print("\n=== 2. HTTP HEADERS & SSL ===")
try:
    r_home = requests.get(BASE_URL, headers=HEADERS, timeout=10)
    print("Homepage Status:", r_home.status_code)
    for h in ["Strict-Transport-Security", "X-Frame-Options", "X-Content-Type-Options", "Referrer-Policy", "Content-Security-Policy", "X-ShopId", "Server"]:
        print(f"  {h}: {r_home.headers.get(h, '[MISSING]')}")
except Exception as e:
    print("Homepage Headers Error:", e)

# SSL Certificate
try:
    ctx = ssl.create_default_context()
    with ctx.wrap_socket(socket.socket(), server_hostname="makemealabel.com") as s:
        s.connect(("makemealabel.com", 443))
        cert = s.getpeercert()
        exp_date = datetime.datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
        days_left = (exp_date - datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)).days
        print(f"  SSL Issuer: {dict(x[0] for x in cert.get('issuer', []))}")
        print(f"  SSL Expiry: {cert['notAfter']} ({days_left} days left)")
except Exception as e:
    print("SSL Check Error:", e)

print("\n=== 3. HOMEPAGE SCHEMA & METADATA ===")
try:
    soup = BeautifulSoup(r_home.text, "html.parser")
    print("Title:", soup.title.string if soup.title else "[NONE]")
    m_desc = soup.find("meta", attrs={"name": "description"})
    print("Meta Description:", m_desc["content"] if m_desc else "[NONE]")
    
    # Check H1s
    h1s = [h.get_text(" ", strip=True) for h in soup.find_all("h1")]
    print(f"H1 Count: {len(h1s)} | H1s: {h1s}")
    
    # Check Schema scripts
    schemas = []
    for s in soup.find_all("script", type="application/ld+json"):
        try:
            d = json.loads(s.string or "{}")
            if isinstance(d, list):
                for item in d: schemas.append(item.get("@type", "Unknown"))
            elif isinstance(d, dict):
                if "@graph" in d:
                    for item in d["@graph"]: schemas.append(item.get("@type", "Unknown"))
                else:
                    schemas.append(d.get("@type", "Unknown"))
        except:
            schemas.append("INVALID_JSON")
    print("Homepage Structured Data (@type):", schemas)
except Exception as e:
    print("Homepage Parse Error:", e)

print("\nLive probing complete.")
