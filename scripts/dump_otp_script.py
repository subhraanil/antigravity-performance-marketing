import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://iaol.co.in/french-google-nm/nm-french-lpg/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

# Find the script containing sumbitForm
scripts = re.findall(r'<script[\s\S]*?</script>', html, re.IGNORECASE)
for s in scripts:
    if 'sumbitForm' in s or 'sendOTP' in s:
        print("=== OTP / SUBMIT SCRIPT ===")
        print(s)
