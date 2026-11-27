import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls = [
    'https://labelitsolutions.co.uk/product/cardboard-cores-13mm-internal-diameter/',
    'https://labelitsolutions.co.uk/product/thermal-transfer-labels-100mm-x-50mm/',
    'https://labelitsolutions.co.uk/product/60mm-round-labels-12-labels-per-sheet/',
    'https://labelitsolutions.co.uk/product/200mm-x-144mm-rectangular-labels-2-labels-per-sheet/'
]

for u in urls:
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='replace')
        prices = re.findall(r'woocommerce-Price-currencySymbol">&pound;</span>([0-9\.]+)', html)
        has_add_to_cart = 'single_add_to_cart_button' in html
        print(u)
        print('  Prices found:', prices)
        print('  Has Add to Cart button:', has_add_to_cart)
