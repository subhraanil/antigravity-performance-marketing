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
    'https://labelitsolutions.co.uk/product/thermal-transfer-labels-100mm-x-152mm/'
]

for url in urls:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='replace')
            print(f"=== {url} ===")
            
            # Check price
            price_match = re.findall(r'<span class="woocommerce-Price-amount amount">(.*?)</span>', html)
            print("  Price amounts:", price_match[:5])
            
            # Check for reviews / rating
            has_reviews = 'star-rating' in html or 'woocommerce-Reviews' in html
            print("  Has WooCommerce review section:", has_reviews)
            review_count = re.findall(r'(\d+)\s+customer review', html)
            print("  Review count match:", review_count)
            
            # Check for volume discount / tiered pricing table
            has_tier = any(k in html.lower() for k in ['bulk price', 'volume discount', 'quantity discount', 'tier', 'per roll', 'per pack', 'save '])
            print("  Mentions volume discount/bulk:", has_tier)
            
            # Check for printer compatibility
            printers = [p for p in ['zebra', 'citizen', 'tsc', 'brother', 'dymo', 'sato', 'toshiba'] if p in html.lower()]
            print("  Printer brand mentions:", printers)
            
            # Check description length
            desc_match = re.search(r'<div class="woocommerce-product-details__short-description">(.*?)</div>', html, re.DOTALL)
            if desc_match:
                desc_text = re.sub(r'<[^>]+>', ' ', desc_match.group(1)).strip()
                print("  Short desc word count:", len(desc_text.split()), f"('{desc_text[:60]}...')")
            else:
                print("  Short desc: NOT FOUND")
                
            tab_desc = re.search(r'<div class="[^"]*woocommerce-Tabs-panel--description[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL)
            if tab_desc:
                t_text = re.sub(r'<[^>]+>', ' ', tab_desc.group(1)).strip()
                print("  Tab desc word count:", len(t_text.split()), f"('{t_text[:60]}...')")
            else:
                print("  Tab desc: NOT FOUND")
                
    except Exception as e:
        print(f"Error {url}: {e}")
