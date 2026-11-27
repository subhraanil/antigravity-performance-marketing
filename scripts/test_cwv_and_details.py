import requests
from bs4 import BeautifulSoup
import re
import json

HEADERS = {"User-Agent": "SEO-Audit-Bot/1.0 (+contact: client-audit)"}

print("=== 1. ANALYTICS & TRACKING SCRIPTS ===")
r_home = requests.get("https://victoryhcspl.com/", headers=HEADERS, timeout=15)
home_text = r_home.text

# Check GA4 (G-XXXX), UA (UA-XXXX), GTM (GTM-XXXX), Meta Pixel, Clarity
ga4_matches = re.findall(r"G-[A-Z0-9]{8,12}", home_text)
ua_matches = re.findall(r"UA-\d+-\d+", home_text)
gtm_matches = re.findall(r"GTM-[A-Z0-9]{5,10}", home_text)
meta_pixel = re.findall(r"fbq\('init',\s*['\"](\d+)['\"]", home_text)
clarity_matches = re.findall(r"clarity\.ms/tag/([a-zA-Z0-9]+)", home_text)

print(f"GA4 Measurement IDs: {set(ga4_matches)}")
print(f"Universal Analytics IDs: {set(ua_matches)}")
print(f"Google Tag Manager IDs: {set(gtm_matches)}")
print(f"Meta Pixel IDs: {set(meta_pixel)}")
print(f"Microsoft Clarity IDs: {set(clarity_matches)}")

# Check search console verification
gsc_verify = re.findall(r'<meta[^>]*name=["\']google-site-verification["\'][^>]*content=["\']([^"\']+)["\']', home_text, re.I)
bing_verify = re.findall(r'<meta[^>]*name=["\']msvalidate\.01["\'][^>]*content=["\']([^"\']+)["\']', home_text, re.I)
print(f"Google Search Console meta verification: {gsc_verify}")
print(f"Bing Webmaster Tools meta verification: {bing_verify}")

# Check chaty plugin
chaty_matches = re.findall(r'chaty', home_text, re.I)
print(f"Chaty plugin mentions: {len(chaty_matches)}")

print("\n=== 2. PRIMARY SERVICE PAGE DEEP-DIVE: /healthcare-training/ ===")
r_ht = requests.get("https://victoryhcspl.com/healthcare-training/", headers=HEADERS, timeout=15)
soup_ht = BeautifulSoup(r_ht.text, "lxml")

print("Page Title:", soup_ht.title.get_text(strip=True) if soup_ht.title else "None")
meta_d = soup_ht.find("meta", attrs={"name": re.compile(r"^description$", re.I)})
print("Meta Description:", meta_d.get("content") if meta_d else "None")

canonical = soup_ht.find("link", rel="canonical")
print("Canonical:", canonical.get("href") if canonical else "None")

h1s = [h.get_text(" ", strip=True) for h in soup_ht.find_all("h1")]
print(f"H1 tags count: {len(h1s)}")
for idx, h in enumerate(h1s):
    print(f"  H1 #{idx+1}: {h}")

h2s = [h.get_text(" ", strip=True) for h in soup_ht.find_all("h2")]
print(f"H2 tags count: {len(h2s)}")
for idx, h in enumerate(h2s):
    print(f"  H2 #{idx+1}: {h}")

h3s = [h.get_text(" ", strip=True) for h in soup_ht.find_all("h3")]
print(f"H3 tags count: {len(h3s)}")
for idx, h in enumerate(h3s):
    print(f"  H3 #{idx+1}: {h}")

# Word count & text inspection
for s in soup_ht(["script", "style", "noscript", "svg"]):
    s.decompose()
body_text = soup_ht.get_text(" ", strip=True)
words = re.findall(r"\w+", body_text)
print(f"Total word count on /healthcare-training/: {len(words)}")

print("\nContent excerpt (first 500 chars):")
print(body_text[:500])

# Images on /healthcare-training/
imgs_ht = soup_ht.find_all("img")
print(f"\nImages on /healthcare-training/: {len(imgs_ht)}")
for img in imgs_ht:
    src = img.get("src", "")
    alt = img.get("alt", "")
    width = img.get("width", "")
    height = img.get("height", "")
    loading = img.get("loading", "")
    print(f" - Src: {src} | Alt: '{alt}' | Dimensions: {width}x{height} | Loading: {loading}")

# CTAs and Forms on /healthcare-training/
forms = soup_ht.find_all("form")
print(f"\nForms on /healthcare-training/: {len(forms)}")
for f in forms:
    print(" - Form Action:", f.get("action"), "Method:", f.get("method"))
    inputs = [inp.get("name") or inp.get("type") for inp in f.find_all(["input", "select", "textarea"])]
    print("   Fields:", inputs)

# Links on /healthcare-training/
in_links = []
out_links = []
for a in soup_ht.find_all("a", href=True):
    href = a["href"].strip()
    txt = a.get_text(" ", strip=True)
    if "victoryhcspl.com" in href or href.startswith("/"):
        in_links.append((href, txt))
    else:
        out_links.append((href, txt))

print(f"Internal links count on page: {len(in_links)}")
for l, t in in_links[:10]:
    print(f"   Internal: {l} (Anchor: '{t}')")
print(f"External links count on page: {len(out_links)}")
for l, t in out_links[:10]:
    print(f"   External: {l} (Anchor: '{t}')")

print("\n=== 3. ASSET & WEIGHT PROFILING FOR CWV ===")
# Fetch assets referenced on /healthcare-training/
scripts = [s.get("src") for s in soup_ht.find_all("script", src=True)]
css_links = [l.get("href") for l in soup_ht.find_all("link", rel=lambda r: r and "stylesheet" in r)]
print(f"Total External Scripts: {len(scripts)}")
print(f"Total Stylesheets: {len(css_links)}")
print(f"HTML Size: {len(r_ht.content)} bytes ({len(r_ht.content)/1024:.1f} KB)")
