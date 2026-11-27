import urllib.request
import ssl
import re
import json
import os

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 1. Fetch JS bundle
js_url = 'https://storiai.ai/assets/index-CVHzEv9o.js'
print(f"Fetching {js_url}...")
req = urllib.request.Request(js_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
with urllib.request.urlopen(req, context=ctx) as resp:
    js_content = resp.read().decode('utf-8', errors='ignore')

print(f"JS Bundle Size: {len(js_content)} characters")

# Save bundle locally for inspection
os.makedirs("data/storiai", exist_ok=True)
with open("data/storiai/bundle.js", "w", encoding="utf-8") as f:
    f.write(js_content)

# Search for routes in React Router
# Typical patterns: path:"...", path:'...', createBrowserRouter, Route
route_patterns = [
    r'path\s*:\s*["\']([^"\']+)["\']',
    r'path\s*=\s*["\']([^"\']+)["\']',
    r'to\s*:\s*["\']([^"\']+)["\']',
    r'navigate\s*\(\s*["\']([^"\']+)["\']',
    r'href\s*:\s*["\']([^"\']+)["\']',
    r'["\'](/[\w\d\-_/]+)["\']'
]

all_paths = set()
for p in route_patterns:
    matches = re.findall(p, js_content)
    for m in matches:
        if m.startswith('/') and not m.startswith('//') and not m.startswith('/assets') and not m.startswith('/img') and not m.endswith('.png') and not m.endswith('.jpg') and not m.endswith('.svg') and not m.endswith('.json'):
            all_paths.add(m)

print(f"Discovered URL routes/paths ({len(all_paths)} found):")
for path in sorted(all_paths):
    print(" -", path)

# Look for text strings in the bundle: headings, titles, descriptions, features
print("\n--- Searching for Brand & Product Copy in React Bundle ---")
keywords = ["Where Your Child", "Emotions", "Stories", "Pricing", "Features", "About", "Contact", "Login", "Register", "Sign Up"]
for kw in keywords:
    count = len(re.findall(re.escape(kw), js_content, re.IGNORECASE))
    print(f"Keyword '{kw}': {count} occurrences")

# Find H1 / Hero section text
hero_match = re.findall(r'Where Your Child[\w\s\',.!?-]+', js_content)
print("\nHero match sample:", hero_match[:3])

# Check for API endpoints called by React
api_endpoints = set(re.findall(r'["\'](https?://[^"\']+|/api/[^"\']+)["\']', js_content))
print(f"\nAPI Endpoints or external URLs ({len(api_endpoints)}):")
for ep in sorted([e for e in api_endpoints if 'api' in e.lower() or 'backend' in e.lower() or 'storiai' in e.lower()]):
    print(" -", ep)
