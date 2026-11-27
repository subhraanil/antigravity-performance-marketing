import requests
from bs4 import BeautifulSoup
import re
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'}

pages = [
    'https://www.panelright.com/',
    'https://www.panelright.com/faq',
    'https://www.panelright.com/efficiency',
    'https://solutions.panelright.com/contact'
]

results = []

for u in pages:
    print(f"\n==========================================")
    print(f"URL: {u}")
    print(f"==========================================")
    r = requests.get(u, headers=headers, timeout=15)
    soup = BeautifulSoup(r.text, 'lxml')
    
    # Title
    title = soup.title.get_text(strip=True) if soup.title else "[MISSING TITLE]"
    print(f"Title ({len(title)} chars): {title}")
    
    # Meta Description
    m_desc = soup.find('meta', attrs={'name': re.compile(r'^description$', re.I)})
    meta_desc = m_desc.get('content', '').strip() if m_desc else "[MISSING META DESCRIPTION]"
    print(f"Meta Description ({len(meta_desc)} chars): {meta_desc}")
    
    # Canonical
    canon = soup.find('link', rel='canonical')
    canonical = canon.get('href', '').strip() if canon else "[MISSING CANONICAL TAG]"
    print(f"Canonical: {canonical}")
    
    # Robots meta
    rmeta = soup.find('meta', attrs={'name': re.compile(r'^robots$', re.I)})
    print(f"Robots meta: {rmeta.get('content') if rmeta else 'None'}")
    
    # Headings
    h1s = [h.get_text(" ", strip=True) for h in soup.find_all('h1')]
    h2s = [h.get_text(" ", strip=True) for h in soup.find_all('h2')]
    h3s = [h.get_text(" ", strip=True) for h in soup.find_all('h3')]
    print(f"H1 Count: {len(h1s)}")
    for idx, h in enumerate(h1s):
        print(f"  H1 #{idx+1}: '{h}'")
    print(f"H2 Count: {len(h2s)}")
    for idx, h in enumerate(h2s[:5]):
        print(f"  H2 #{idx+1}: '{h}'")
    print(f"H3 Count: {len(h3s)}")
    
    # Word count
    for s in soup(["script", "style", "noscript", "svg"]):
        s.decompose()
    body_text = soup.get_text(" ", strip=True)
    words = len(re.findall(r'\w+', body_text))
    print(f"Word Count: {words}")
    print(f"Body text excerpt (first 300 chars):\n  {body_text[:300]}")
    
    # Images
    imgs = soup.find_all('img')
    imgs_no_alt = [img.get('src', '') for img in imgs if not img.get('alt') or not img.get('alt').strip()]
    print(f"Images: {len(imgs)} | Missing Alt: {len(imgs_no_alt)}")
    for img in imgs[:5]:
        print(f"  Img src: {img.get('src')[:60]} | alt: '{img.get('alt')}'")
        
    # Links
    links = soup.find_all('a', href=True)
    print(f"Total Links: {len(links)}")
    for l in links[:8]:
        print(f"  Link href: {l.get('href')} | text: '{l.get_text(strip=True)}'")
        
    # Structured data
    schemas = soup.find_all('script', type='application/ld+json')
    print(f"Schema JSON-LD Blocks: {len(schemas)}")
    for s in schemas:
        try:
            print("  Schema:", s.string[:200])
        except:
            pass

    # OpenGraph / Twitter
    og_title = soup.find('meta', property='og:title')
    og_desc = soup.find('meta', property='og:description')
    og_image = soup.find('meta', property='og:image')
    print(f"OG Title: {og_title.get('content') if og_title else '[MISSING]'}")
    print(f"OG Description: {og_desc.get('content') if og_desc else '[MISSING]'}")
    print(f"OG Image: {og_image.get('content') if og_image else '[MISSING]'}")
    
    # Response Headers
    print(f"Server: {r.headers.get('Server')}")
    print(f"X-Frame-Options: {r.headers.get('X-Frame-Options', '[MISSING]')}")
    print(f"X-Content-Type-Options: {r.headers.get('X-Content-Type-Options', '[MISSING]')}")
    print(f"Content-Security-Policy: {r.headers.get('Content-Security-Policy', '[MISSING]')}")
    print(f"Strict-Transport-Security: {r.headers.get('Strict-Transport-Security', '[MISSING]')}")
