import urllib.request
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

assets_to_test = [
    'https://storiai.ai/',
    'https://storiai.ai/assets/index-CVHzEv9o.js',
    'https://storiai.ai/assets/App-XFfRbN91.js',
    'https://storiai.ai/assets/App-CsDpWzVI.css',
    'https://storiai.ai/manifest.webmanifest',
    'https://storiai.ai/hero-home.webp',
    'https://storiai.ai/pricing',
    'https://storiai.ai/about',
    'https://storiai.ai/faq',
    'https://storiai.ai/contact'
]

for url in assets_to_test:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, context=ctx) as resp:
            headers = dict(resp.info())
            print(f"URL: {url}")
            print(f"  Status: {resp.status}")
            print(f"  Content-Type: {headers.get('Content-Type')}")
            print(f"  Content-Length: {headers.get('Content-Length')}")
            print(f"  Cache-Control: {headers.get('Cache-Control')}")
            print(f"  ETag: {headers.get('ETag')}")
            print(f"  Content-Encoding: {headers.get('Content-Encoding')}")
            print()
    except Exception as e:
        print(f"URL: {url} -> Error: {e}\n")
