import socket
import ssl
import json
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import datetime

HEADERS = {"User-Agent": "SEO-Audit-Bot/1.0 (+contact: client-audit)"}

print("=== 1. VERSION CONSOLIDATION & REDIRECT TESTS ===")
test_urls = [
    "http://victoryhcspl.com/",
    "http://www.victoryhcspl.com/",
    "https://www.victoryhcspl.com/",
    "https://victoryhcspl.com/index.php",
    "https://victoryhcspl.com/index.html",
    "https://victoryhcspl.com/home/",
    "https://victoryhcspl.com/robots.txt",
    "https://victoryhcspl.com/sitemap.xml",
    "https://victoryhcspl.com/wp-sitemap.xml"
]

for u in test_urls:
    try:
        r = requests.get(u, headers=HEADERS, allow_redirects=False, timeout=10)
        chain = []
        curr = u
        r_temp = r
        while r_temp.is_redirect or r_temp.is_permanent_redirect:
            loc = r_temp.headers.get("Location")
            chain.append(f"{r_temp.status_code} -> {loc}")
            curr = loc
            try:
                r_temp = requests.get(loc, headers=HEADERS, allow_redirects=False, timeout=10)
            except:
                break
        print(f"URL: {u}")
        print(f"  Initial Status: {r.status_code} | Target: {r.headers.get('Location')}")
        if chain:
            print(f"  Full Chain: {' -> '.join(chain)}")
    except Exception as e:
        print(f"URL: {u} -> Error: {e}")

print("\n=== 2. SSL CERTIFICATE & TLS PROTOCOL ===")
hostname = "victoryhcspl.com"
ctx = ssl.create_default_context()
with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
    s.connect((hostname, 443))
    cert = s.getpeercert()
    cipher = s.cipher()
    version = s.version()
    print("TLS Version:", version)
    print("Cipher:", cipher)
    print("Subject:", dict(x[0] for x in cert['subject']))
    print("Issuer:", dict(x[0] for x in cert['issuer']))
    print("Not Before:", cert['notBefore'])
    print("Not After (Expiry):", cert['notAfter'])
    
    # Days until expiry
    exp_date = datetime.datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
    days_left = (exp_date - datetime.datetime.utcnow()).days
    print(f"Days until SSL expiry: {days_left} days")

print("\n=== 3. HOSTING IP & LOCATION ===")
ip = socket.gethostbyname(hostname)
print(f"Resolved IP: {ip}")
try:
    geo_r = requests.get(f"https://ipapi.co/{ip}/json/", headers=HEADERS, timeout=10)
    if geo_r.status_code == 200:
        g = geo_r.json()
        print(f"Server Location: {g.get('city')}, {g.get('region')}, {g.get('country_name')} (Org: {g.get('org')})")
    else:
        print("ipapi status:", geo_r.status_code)
except Exception as e:
    print(f"Geo lookup err: {e}")

print("\n=== 4. SECURITY HEADERS AUDIT ===")
r_home = requests.get("https://victoryhcspl.com/", headers=HEADERS, timeout=15)
headers_check = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
    "Permissions-Policy",
    "Server",
    "X-Powered-By"
]
for h in headers_check:
    val = r_home.headers.get(h)
    print(f"  {h}: {val if val else '[MISSING]'}")

print("\n=== 5. TECH STACK & GENERATOR DETECTION ===")
soup = BeautifulSoup(r_home.text, "lxml")
generator = soup.find("meta", attrs={"name": "generator"})
print("Generator meta tag:", generator.get("content") if generator else "None found")

# Look for plugins and themes
plugins = set()
for tag in soup.find_all(["link", "script", "img"], src=True):
    src = tag.get("src", "")
    if "wp-content/plugins/" in src:
        parts = src.split("wp-content/plugins/")[1].split("/")
        plugins.add(parts[0])
for tag in soup.find_all("link", href=True):
    href = tag.get("href", "")
    if "wp-content/plugins/" in href:
        parts = href.split("wp-content/plugins/")[1].split("/")
        plugins.add(parts[0])

theme = "Unknown"
for tag in soup.find_all(["link", "script"], src=True):
    src = tag.get("src", "")
    if "wp-content/themes/" in src:
        parts = src.split("wp-content/themes/")[1].split("/")
        theme = parts[0]
for tag in soup.find_all("link", href=True):
    href = tag.get("href", "")
    if "wp-content/themes/" in href:
        parts = href.split("wp-content/themes/")[1].split("/")
        theme = parts[0]

print(f"Detected Theme: {theme}")
print("Detected Plugins:", sorted(list(plugins)))

print("\n=== 6. STRUCTURED DATA ON HOMEPAGE & PRIMARY SERVICE PAGE ===")
for p_url in ["https://victoryhcspl.com/", "https://victoryhcspl.com/healthcare-training/"]:
    r_p = requests.get(p_url, headers=HEADERS, timeout=15)
    s_p = BeautifulSoup(r_p.text, "lxml")
    scripts = s_p.find_all("script", type="application/ld+json")
    print(f"\nURL: {p_url}")
    print(f"Found {len(scripts)} JSON-LD blocks:")
    for idx, s in enumerate(scripts):
        try:
            d = json.loads(s.string)
            print(f"  Block {idx+1}:")
            print(json.dumps(d, indent=2)[:500])
        except Exception as e:
            print(f"  Block {idx+1}: Parse error: {e}")
