import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

pages = [
    'https://labelitsolutions.co.uk/contact-us/',
    'https://labelitsolutions.co.uk/about-us/',
    'https://labelitsolutions.co.uk/returns-refund-policy/',
    'https://labelitsolutions.co.uk/terms-conditions-of-sale/'
]

for url in pages:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='replace')
            text = re.sub(r'<[^>]+>', ' ', html)
            text = re.sub(r'\s+', ' ', text)
            print(f"=== {url} ===")
            phones = re.findall(r'(?:0\d{3,4}\s?\d{3,4}\s?\d{3,4}|\+44\s?\d{2,4}\s?\d{3,4}\s?\d{3,4})', text)
            emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)
            print("  Phone numbers found:", set(phones))
            print("  Emails found:", set(emails))
            reg = [s.strip() for s in text.split('.') if any(k in s.lower() for k in ['company registration', 'company no', 'reg no', 'vat no', 'registered in', 'registered office'])]
            print("  Company / VAT mentions:", reg[:3])
            addr = [s.strip() for s in text.split('.') if any(k in s.lower() for k in ['street', 'road', 'avenue', 'lane', 'leicester', 'birmingham', 'london', 'unit', 'industrial estate'])]
            print("  Address mentions:", addr[:3])
    except Exception as e:
        print(f"Error {url}: {e}")
