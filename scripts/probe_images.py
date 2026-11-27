import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

img_urls = [
    'https://storiai.ai/img/Danger_md.png',
    'https://storiai.ai/img/illus/avatar-boy.png',
    'https://storiai.ai/img/illus/avatar-girl.png',
    'https://storiai.ai/img/illus/nav/star-left.png',
    'https://storiai.ai/hero-home.webp',
    'https://storiai.ai/img/hero-home.webp',
    'https://storiai.ai/assets/hero-home.webp',
    'https://storiai.ai/parent-child-illu-2.webp',
    'https://storiai.ai/img/parent-child-illu-2.webp',
    'https://storiai.ai/assets/parent-child-illu-2.webp',
    'https://storiai.ai/create-child2.webp'
]

for u in img_urls:
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            ct = resp.headers.get('Content-Type')
            cl = resp.headers.get('Content-Length')
            print(f"{u} -> Status {resp.status} | Content-Type: {ct} | Size: {cl}")
    except Exception as e:
        print(f"{u} -> Error: {e}")
