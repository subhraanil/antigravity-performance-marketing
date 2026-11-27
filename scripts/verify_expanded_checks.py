import requests
from bs4 import BeautifulSoup

urls = [
    'https://www.panelright.com/robots.txt',
    'https://www.panelright.com/',
    'https://www.panelright.com/efficiency',
    'https://www.panelright.com/faq',
    'https://www.panelright.com/privacy',
    'https://www.panelright.com/terms',
    'https://solutions.panelright.com/contact',
    'https://solutions.panelright.com/'
]

print("=== 1. ROBOTS.TXT CONTENT ===")
try:
    r = requests.get('https://www.panelright.com/robots.txt', timeout=10)
    print("Status:", r.status_code)
    print("Content:\n", r.text)
except Exception as e:
    print("Error fetching robots.txt:", e)

print("\n=== 2. HEADERS AUDIT ===")
for u in ['https://www.panelright.com/', 'https://solutions.panelright.com/contact']:
    try:
        res = requests.get(u, timeout=10)
        print(f"-- {u} (Status: {res.status_code}) --")
        for k in ['Strict-Transport-Security', 'X-Content-Type-Options', 'X-Frame-Options', 'Referrer-Policy', 'Content-Security-Policy', 'X-Robots-Tag']:
            val = res.headers.get(k, "[MISSING]")
            print(f"  {k}: {val}")
    except Exception as e:
        print(f"Error fetching {u}:", e)

print("\n=== 3. EXPOSED DEV ARTIFACTS TEST ===")
dev_probes = [
    'https://www.panelright.com/.env',
    'https://www.panelright.com/.git/config',
    'https://www.panelright.com/api/',
    'https://www.panelright.com/_next/static/'
]
for dp in dev_probes:
    try:
        resp = requests.get(dp, timeout=10)
        print(f"{dp} -> Status: {resp.status_code} (Length: {len(resp.content)})")
    except Exception as e:
        print(f"{dp} -> Error:", e)

print("\n=== 4. META ROBOTS ON ALL PAGES ===")
for u in urls[1:]:
    try:
        res = requests.get(u, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        meta_robots = soup.find('meta', attrs={'name': 'robots'})
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        title = soup.find('title')
        print(f"{u}:")
        print(f"  Meta Robots: {meta_robots['content'] if meta_robots and meta_robots.has_attr('content') else '[NONE]'}")
        print(f"  Viewport: {viewport['content'] if viewport and viewport.has_attr('content') else '[NONE]'}")
        print(f"  Title: {title.text if title else '[NONE]'}")
    except Exception as e:
        print(f"{u} -> Error:", e)
