import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls = [
    'https://labelitsolutions.co.uk/product/thermal-transfer-labels-100mm-x-152mm/',
    'https://labelitsolutions.co.uk/product/60mm-round-labels-12-labels-per-sheet/'
]

for u in urls:
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='replace')
        print(u)
        has_prod = 'Product' in html and ('@type' in html or 'itemtype' in html)
        print('  Contains Product schema string:', has_prod)
        og = re.findall(r'<meta property="og:[^"]+"', html)
        print('  OG tags count:', len(og))
        tw = re.findall(r'<meta name="twitter:[^"]+"', html)
        print('  Twitter tags count:', len(tw))
        all_ld = re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', html, re.DOTALL)
        for idx, ld in enumerate(all_ld):
            print(f'  JSON-LD block {idx+1}:', ld.strip()[:150])
