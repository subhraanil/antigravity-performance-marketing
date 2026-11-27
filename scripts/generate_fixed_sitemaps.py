import xml.etree.ElementTree as ET
import os

os.makedirs('reports/fixed_sitemaps', exist_ok=True)

SITEMAPS = [
    'sitemap.xml',
    'sitemap-products.xml',
    'sitemap-categories.xml'
]

REMOVE_URLS = {
    'https://www.promotionalproductsnow.au/unsubscribe',
    'https://www.promotionalproductsnow.au/Forgot-Password'
}

for sm in SITEMAPS:
    src_path = f"https://www.promotionalproductsnow.au/{sm}"
    import urllib.request
    req = urllib.request.Request(src_path, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        content = resp.read()
        
    root = ET.fromstring(content)
    
    # Register namespace to keep xml tags clean
    ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    
    modified_count = 0
    removed_count = 0
    
    urls_to_remove = []
    for url_elem in root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
        loc = url_elem.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
        if loc is not None and loc.text:
            url_text = loc.text.strip()
            
            if url_text in REMOVE_URLS:
                urls_to_remove.append(url_elem)
                removed_count += 1
                continue
                
            if url_text.startswith('https://promotionalproductsnow.au/'):
                new_url = url_text.replace('https://promotionalproductsnow.au/', 'https://www.promotionalproductsnow.au/')
                loc.text = new_url
                modified_count += 1
                
    for url_elem in urls_to_remove:
        root.remove(url_elem)
        
    out_path = f"reports/fixed_sitemaps/{sm}"
    tree = ET.ElementTree(root)
    tree.write(out_path, encoding='utf-8', xml_declaration=True)
    print(f"Generated {out_path}: Modified {modified_count} non-www URLs, Removed {removed_count} problematic URLs.")

# Also generate a master sitemap_index.xml
sitemap_index_content = """<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://www.promotionalproductsnow.au/sitemap.xml</loc>
  </sitemap>
  <sitemap>
    <loc>https://www.promotionalproductsnow.au/sitemap-products.xml</loc>
  </sitemap>
  <sitemap>
    <loc>https://www.promotionalproductsnow.au/sitemap-categories.xml</loc>
  </sitemap>
</sitemapindex>
"""

with open('reports/fixed_sitemaps/sitemap_index.xml', 'w', encoding='utf-8') as f:
    f.write(sitemap_index_content)
print("Generated reports/fixed_sitemaps/sitemap_index.xml")
