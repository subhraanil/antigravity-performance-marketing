import urllib.request
import ssl
import json
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(
    'https://labelitsolutions.co.uk/',
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
)

print("--- PROBING HOMEPAGE ---")
try:
    with urllib.request.urlopen(req, context=ctx, timeout=12) as resp:
        print('Status:', resp.status)
        headers = dict(resp.getheaders())
        for k in ['Server', 'server', 'Strict-Transport-Security', 'X-Frame-Options', 
                  'X-Content-Type-Options', 'Content-Security-Policy', 'Referrer-Policy']:
            if k in headers:
                print(f'{k}: {headers[k]}')
            else:
                print(f'{k}: MISSING')
        
        html = resp.read().decode('utf-8', errors='replace')
        print('HTML length:', len(html))
        
        # Check theme & plugins
        theme_matches = set(re.findall(r'/wp-content/themes/([^/]+)/', html))
        print('Themes detected:', theme_matches)
        plugin_matches = set(re.findall(r'/wp-content/plugins/([^/]+)/', html))
        print('Plugins detected:', sorted(list(plugin_matches)))
        
        # Check generator
        gen = re.findall(r'<meta name="generator" content="([^"]+)"', html)
        print('Generator:', gen)
        
        # Check schema
        schemas = re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', html, re.DOTALL)
        print('JSON-LD count:', len(schemas))
        for idx, s in enumerate(schemas):
            print(f'Schema {idx+1}:', s[:200].strip())
            
        # Check canonical
        canon = re.findall(r'<link rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']', html)
        print('Canonical tag on live homepage:', canon)
        
        # Check title
        title = re.findall(r'<title>(.*?)</title>', html)
        print('Title tag on live homepage:', title)
        
        # Check meta description
        meta_d = re.findall(r'<meta name="description" content="([^"]*)"', html)
        print('Meta description on live homepage:', meta_d)

except Exception as e:
    print('Error probing live site:', e)

print("\n--- PROBING ROBOTS.TXT ---")
try:
    req_rob = urllib.request.Request('https://labelitsolutions.co.uk/robots.txt', headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req_rob, context=ctx, timeout=10) as resp:
        print('Robots.txt status:', resp.status)
        rob_text = resp.read().decode('utf-8', errors='replace')
        print(rob_text.strip()[:500])
except Exception as e:
    print('Robots.txt error:', e)

print("\n--- PROBING SITEMAP.XML ---")
try:
    req_sm = urllib.request.Request('https://labelitsolutions.co.uk/sitemap.xml', headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req_sm, context=ctx, timeout=10) as resp:
        print('Sitemap.xml status:', resp.status)
        sm_text = resp.read().decode('utf-8', errors='replace')
        print(sm_text.strip()[:400])
except Exception as e:
    print('Sitemap.xml error:', e)
