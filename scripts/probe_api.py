import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

api_urls = [
    'https://api.storiai.ai/',
    'https://api.storiai.ai/health',
    'https://api.storiai.ai/docs',
    'https://api.storiai.ai/api/v1/health'
]

for u in api_urls:
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            print(f"{u} -> Status {resp.status} | Content-Type: {resp.headers.get('Content-Type')}")
            body = resp.read().decode('utf-8', errors='ignore')
            print(f"  Body: {body[:200]}")
    except urllib.error.HTTPError as e:
        print(f"{u} -> Status {e.code} | {e.reason}")
    except Exception as e:
        print(f"{u} -> Error: {e}")
