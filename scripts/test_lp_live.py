import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://iaol.co.in/french-google-nm/nm-french-lpg/'
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        print('Status code:', resp.getcode())
        content = resp.read().decode('utf-8', errors='ignore')
        print('Content length:', len(content))
        print('Has form:', '<form' in content.lower())
        print('Has gtm / gtag:', 'googletagmanager' in content.lower() or 'gtag' in content.lower())
        title = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
        if title:
            print('Page Title:', title.group(1))
        form_actions = re.findall(r'action=[\"\'](.*?)[\"\']', content, re.IGNORECASE)
        print('Form actions:', form_actions)
        # Check if form submission points to thank you page
        print("Mentions of thank-you or thanks:")
        print([m for m in re.findall(r'https?://[^\s\"\'<>]+', content) if 'thank' in m.lower()])
except Exception as e:
    print('Error testing landing page:', e)
