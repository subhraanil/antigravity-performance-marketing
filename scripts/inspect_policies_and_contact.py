import requests
from bs4 import BeautifulSoup
import sys
if sys.stdout.encoding != 'utf-8': sys.stdout.reconfigure(encoding='utf-8')

urls = [
    "https://makemealabel.com/policies/shipping-policy",
    "https://makemealabel.com/policies/refund-policy",
    "https://makemealabel.com/policies/contact-information",
    "https://makemealabel.com/pages/contact",
    "https://makemealabel.com/pages/about-us"
]

for u in urls:
    r = requests.get(u, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    main = soup.find("main") or soup.body
    text = main.get_text(" ", strip=True) if main else ""
    print(f"=== {u} ===")
    print(f"Title: {soup.title.string if soup.title else '[None]'}")
    print(f"Content Preview (first 300 chars):")
    print(text[:300])
    print("-" * 50)
