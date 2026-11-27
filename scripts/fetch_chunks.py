import urllib.request
import ssl
import os
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

chunks = [
    'App-XFfRbN91.js',
    'index-C765lMd0.js',
    'index-CwtSQNOk.js',
    'workbox-window.prod.es5-BBnX5xw4.js'
]

os.makedirs('data/storiai/chunks', exist_ok=True)

for chunk in chunks:
    url = f'https://storiai.ai/assets/{chunk}'
    print(f"Fetching {url}...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            path = f'data/storiai/chunks/{chunk}'
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Saved {chunk} ({len(content)} bytes)")
    except Exception as e:
        print(f"  Error fetching {chunk}: {e}")
