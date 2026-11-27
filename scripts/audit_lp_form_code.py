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

# Extract forms
forms = re.findall(r'<form[\s\S]*?</form>', html, re.IGNORECASE)
print(f"Total forms on landing page: {len(forms)}")
for i, f in enumerate(forms):
    print(f"\n--- Form {i+1} ---")
    inputs = re.findall(r'<input[\s\S]*?>', f, re.IGNORECASE)
    buttons = re.findall(r'<button[\s\S]*?>[\s\S]*?</button>', f, re.IGNORECASE)
    print("Inputs:", [re.search(r'name=[\"\'](.*?)[\"\']', inp).group(1) if re.search(r'name=[\"\'](.*?)[\"\']', inp) else inp[:30] for inp in inputs])
    print("Buttons:", [b[:60] for b in buttons])
    # check script / AJAX submit handlers
    scripts = re.findall(r'<script[\s\S]*?</script>', f, re.IGNORECASE)
    if scripts:
        print("Inline scripts in form:", len(scripts))

# Check script tags referencing form or crm
all_scripts = re.findall(r'<script[\s\S]*?</script>', html, re.IGNORECASE)
print(f"\nTotal scripts on page: {len(all_scripts)}")
for s in all_scripts:
    if any(k in s.lower() for k in ['submit', 'ajax', 'lead', 'crm', 'thanks', 'contact']):
        print("\nRelevant script snippet:")
        print(s[:300].strip())
