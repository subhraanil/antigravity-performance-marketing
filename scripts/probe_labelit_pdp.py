import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

pdp_url = 'https://labelitsolutions.co.uk/product/cardboard-cores-13mm-internal-diameter/'
cat_url = 'https://labelitsolutions.co.uk/product-category/printer-accessories/ribbon-ink/'

print("--- PROBING PRODUCT DETAIL PAGE (PDP) ---")
req = urllib.request.Request(pdp_url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='replace')
        print('PDP Status:', resp.status)
        print('Title:', re.findall(r'<title>(.*?)</title>', html))
        print('H1:', re.findall(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL))
        print('Canonicals:', re.findall(r'<link rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']', html))
        print('Meta desc:', re.findall(r'<meta name="description" content="([^"]*)"', html))
        print('JSON-LD:', len(re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', html, re.DOTALL)))
        # Check pricing, VAT, Add to Cart
        print('Contains "ex. VAT" or "inc. VAT"?:', 'vat' in html.lower())
        print('Contains "woocommerce-Price-amount"?:', 'woocommerce-price-amount' in html.lower())
        print('Contains Add to Cart button?:', 'add to cart' in html.lower() or 'single_add_to_cart_button' in html.lower())
except Exception as e:
    print('PDP probe error:', e)

print("\n--- PROBING CATEGORY PAGE ---")
req2 = urllib.request.Request(cat_url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req2, context=ctx, timeout=10) as resp:
        html2 = resp.read().decode('utf-8', errors='replace')
        print('Cat Status:', resp.status)
        print('Title:', re.findall(r'<title>(.*?)</title>', html2))
        print('H1:', re.findall(r'<h1[^>]*>(.*?)</h1>', html2, re.DOTALL))
        print('H2:', re.findall(r'<h2[^>]*>(.*?)</h2>', html2, re.DOTALL)[:5])
        print('Canonicals:', re.findall(r'<link rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']', html2))
        print('Meta desc:', re.findall(r'<meta name="description" content="([^"]*)"', html2))
except Exception as e:
    print('Cat probe error:', e)
