import urllib.request
import ssl
import json
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

print("=== PROBING HOMEPAGE ===")
try:
    req = urllib.request.Request('https://paidmediaworld.com/', headers=headers)
    with urllib.request.urlopen(req, context=ctx, timeout=12) as resp:
        print('Status:', resp.status)
        resp_headers = dict(resp.getheaders())
        for k in ['Server', 'server', 'Strict-Transport-Security', 'X-Frame-Options', 
                  'X-Content-Type-Options', 'Content-Security-Policy', 'Referrer-Policy', 'cf-ray', 'x-powered-by']:
            print(f'{k}: {resp_headers.get(k, "MISSING")}')
        
        html = resp.read().decode('utf-8', errors='replace')
        print('HTML length:', len(html))
        
        # Check generators / framework
        gen = re.findall(r'<meta[^>]*name=["\']generator["\'][^>]*content=["\']([^"\']+)["\']', html, re.I)
        print('Generators:', gen)
        
        # Next.js / Astro / WP checks
        if '__NEXT_DATA__' in html or '/_next/' in html:
            print('Detected: Next.js')
        if '/wp-content/' in html:
            print('Detected: WordPress')
        if 'ghost' in html.lower():
            print('Detected: Ghost')
            
        # Check title
        title = re.findall(r'<title>(.*?)</title>', html)
        print('Title tag:', title)
        
        # Check meta description
        meta_d = re.findall(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', html, re.I)
        print('Meta description:', meta_d)
        
        # Check H1
        h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
        print('H1 count:', len(h1s))
        for h in h1s:
            print('  H1 text:', re.sub(r'<[^>]+>', ' ', h).strip()[:100])
            
        # Check canonical
        canon = re.findall(r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']', html, re.I)
        print('Canonical:', canon)
        
        # Check schema
        schemas = re.findall(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html, re.DOTALL)
        print('JSON-LD blocks:', len(schemas))
        for idx, s in enumerate(schemas):
            print(f'  Schema {idx+1}:', s.strip()[:200])

except Exception as e:
    print('Homepage probe error:', e)

print("\n=== PROBING ROBOTS.TXT ===")
try:
    req_rob = urllib.request.Request('https://paidmediaworld.com/robots.txt', headers=headers)
    with urllib.request.urlopen(req_rob, context=ctx, timeout=10) as resp:
        print('Robots.txt status:', resp.status)
        text = resp.read().decode('utf-8', errors='replace')
        print(text.strip()[:600])
except Exception as e:
    print('Robots.txt error:', e)

print("\n=== PROBING SITEMAP.XML ===")
try:
    req_sm = urllib.request.Request('https://paidmediaworld.com/sitemap.xml', headers=headers)
    with urllib.request.urlopen(req_sm, context=ctx, timeout=10) as resp:
        print('Sitemap.xml status:', resp.status)
        text = resp.read().decode('utf-8', errors='replace')
        print(text.strip()[:600])
except Exception as e:
    print('Sitemap.xml error:', e)
