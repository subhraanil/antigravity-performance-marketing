import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

opener = urllib.request.build_opener(NoRedirectHandler)

tests = [
    'https://storiai.ai/pricing',
    'https://storiai.ai/pricing/',
    'https://storiai.ai/about',
    'https://storiai.ai/about/',
    'https://storiai.ai/contact',
    'https://storiai.ai/contact/',
]

for t in tests:
    req = urllib.request.Request(t, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        resp = opener.open(req, timeout=5)
        print(f"{t} -> Status {resp.status}")
    except urllib.error.HTTPError as e:
        print(f"{t} -> Status {e.code} -> {e.headers.get('Location')}")
    except Exception as e:
        print(f"{t} -> Error: {e}")
