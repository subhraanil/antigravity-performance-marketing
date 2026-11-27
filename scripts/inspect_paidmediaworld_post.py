import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://paidmediaworld.com/cost-of-facebook-ads-in-india-guide-benchmarks-for-leads-sales/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none'
}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, context=ctx, timeout=12) as resp:
        print('Status:', resp.status)
        html = resp.read().decode('utf-8', errors='replace')
        print('HTML length:', len(html))
        
        # Title
        print('Title:', re.findall(r'<title>(.*?)</title>', html))
        # Meta desc
        print('Meta desc:', re.findall(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', html, re.I))
        # Canonical
        print('Canonical:', re.findall(r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']', html, re.I))
        # H1
        print('H1:', re.findall(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL))
        # H2s
        h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', html, re.DOTALL)
        print(f'H2 count: {len(h2s)}')
        for h in h2s[:5]:
            print('  H2:', re.sub(r'<[^>]+>', ' ', h).strip())
        
        # Schema
        schemas = re.findall(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html, re.DOTALL)
        print(f'Schema blocks: {len(schemas)}')
        for idx, s in enumerate(schemas):
            print(f'  Schema {idx+1}:', s.strip()[:250])
            
except Exception as e:
    print('Error probing post:', e)
