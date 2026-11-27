import requests
import xml.etree.ElementTree as ET

sitemaps = [
    'https://www.promotionalproductsnow.au/sitemap.xml',
    'https://www.promotionalproductsnow.au/sitemap-products.xml',
    'https://www.promotionalproductsnow.au/sitemap-categories.xml',
    'https://www.promotionalproductsnow.au/sitemap_index.xml'
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

print("=== VERIFYING LIVE SITEMAPS ===")

for sm in sitemaps:
    print(f"\nChecking sitemap: {sm}")
    try:
        resp = requests.get(sm, headers=headers, timeout=10)
        print(f"HTTP Status: {resp.status_code}")
        if resp.status_code == 200:
            root = ET.fromstring(resp.content)
            locs = [el.text.strip() for el in root.findall('.//{*}loc') if el.text]
            print(f"Total <loc> entries: {len(locs)}")
            if locs:
                www_count = sum(1 for u in locs if u.startswith('https://www.promotionalproductsnow.au'))
                non_www_count = sum(1 for u in locs if u.startswith('https://promotionalproductsnow.au') and not u.startswith('https://www.'))
                other_count = len(locs) - www_count - non_www_count
                
                print(f"  - URLs starting with 'https://www.': {www_count}")
                print(f"  - URLs starting with 'https://' (non-www): {non_www_count}")
                if other_count > 0:
                    print(f"  - Other domain URLs: {other_count}")
                    
                print(f"  Sample URLs (first 3):")
                for u in locs[:3]:
                    print(f"    * {u}")
                    
                # Check specific issues
                if 'https://www.promotionalproductsnow.au/unsubscribe' in locs:
                    print("  ⚠️ Found /unsubscribe in sitemap!")
                else:
                    print("  ✅ /unsubscribe is NOT in sitemap.")
                    
                if any('forgot-password' in u.lower() for u in locs):
                    print("  ⚠️ Found forgot-password in sitemap!")
                else:
                    print("  ✅ /Forgot-Password is NOT in sitemap.")
        else:
            print(f"  Failed to retrieve (Status {resp.status_code})")
    except Exception as e:
        print(f"  Error: {e}")

# Check robots.txt
print("\nChecking robots.txt:")
try:
    resp = requests.get('https://www.promotionalproductsnow.au/robots.txt', headers=headers, timeout=10)
    print(f"HTTP Status: {resp.status_code}")
    print("Content:")
    print(resp.text)
except Exception as e:
    print(f"Error checking robots.txt: {e}")
