import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://paidmediaworld.com/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, context=ctx, timeout=12) as resp:
        html = resp.read().decode('utf-8', errors='replace')
        imgs = re.findall(r'<img\s+[^>]*>', html)
        print(f"Total img tags on homepage: {len(imgs)}")
        
        missing_alt = 0
        missing_dims = 0
        formats = {}
        
        for img in imgs:
            src_m = re.search(r'src=["\']([^"\']+)["\']', img)
            src = src_m.group(1) if src_m else ""
            alt_m = re.search(r'alt=["\']([^"\']*)["\']', img)
            alt = alt_m.group(1) if alt_m else None
            
            ext = src.split('.')[-1].split('?')[0].lower() if '.' in src else 'unknown'
            formats[ext] = formats.get(ext, 0) + 1
            
            if alt is None or alt.strip() == "":
                missing_alt += 1
            if not ('width=' in img and 'height=' in img):
                missing_dims += 1
                
        print(f"Homepage missing alt: {missing_alt} / {len(imgs)}")
        print(f"Homepage missing dimensions: {missing_dims} / {len(imgs)}")
        print("Image formats:", formats)
except Exception as e:
    print('Homepage img error:', e)
