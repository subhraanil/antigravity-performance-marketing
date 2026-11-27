import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://labelitsolutions.co.uk/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
    html = resp.read().decode('utf-8', errors='replace')
    
    # Extract all img tags
    img_tags = re.findall(r'<img\s+[^>]*>', html)
    print(f"Total img tags on homepage: {len(img_tags)}")
    
    missing_alt = 0
    missing_dims = 0
    png_count = 0
    webp_count = 0
    jpg_count = 0
    
    for tag in img_tags:
        src_match = re.search(r'src=["\']([^"\']+)["\']', tag)
        src = src_match.group(1) if src_match else ""
        alt_match = re.search(r'alt=["\']([^"\']*)["\']', tag)
        alt = alt_match.group(1) if alt_match else None
        
        has_w = 'width=' in tag
        has_h = 'height=' in tag
        
        if alt is None or alt.strip() == "":
            missing_alt += 1
            if missing_alt <= 5:
                print("  Missing alt:", src)
        if not (has_w and has_h):
            missing_dims += 1
            
        if '.png' in src.lower():
            png_count += 1
        elif '.webp' in src.lower():
            webp_count += 1
        elif '.jp' in src.lower():
            jpg_count += 1
            
    print(f"Homepage - Missing Alt: {missing_alt} / {len(img_tags)}")
    print(f"Homepage - Missing Dimensions: {missing_dims} / {len(img_tags)}")
    print(f"Formats: PNG={png_count}, JPG={jpg_count}, WebP={webp_count}")
