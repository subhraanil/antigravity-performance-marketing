import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

variants = [
    'http://storiai.ai/',
    'http://www.storiai.ai/',
    'https://www.storiai.ai/',
    'https://storiai.ai/'
]

class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

opener = urllib.request.build_opener(NoRedirectHandler)

for v in variants:
    req = urllib.request.Request(v, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        resp = opener.open(req, timeout=5)
        print(f"{v} -> Status {resp.status}")
    except urllib.error.HTTPError as e:
        loc = e.headers.get('Location')
        print(f"{v} -> Status {e.code} -> Redirects to: {loc}")
    except Exception as e:
        print(f"{v} -> Error: {e}")
