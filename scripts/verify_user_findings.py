import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'SEO-Audit-Bot/1.0 (+contact: client-audit)'}
r = requests.get('https://victoryhcspl.com/', headers=headers, timeout=15)
soup = BeautifulSoup(r.text, 'lxml')

print("=== 1. TOP MENU EMAIL & PHONE ===")
for el in soup.find_all(attrs={"class": lambda c: c and any(k in str(c).lower() for k in ["top", "header", "info", "contact"])}):
    if "victoryantovijay" in el.get_text() or "99165" in el.get_text():
        print("Element HTML snippet:", str(el)[:300])

# Direct text search
for tag in soup.find_all(True):
    if tag.string and "victoryantovijay@gmail.com" in tag.string:
        print("Email parent:", tag.name, tag.attrs)
        print("Is inside <a> tag?", tag.find_parent("a") is not None)
        if tag.find_parent("a"):
            print("Link href:", tag.find_parent("a").get("href"))
    if tag.string and "+91 99165 09090" in tag.string:
        print("Phone parent:", tag.name, tag.attrs)
        print("Is inside <a> tag?", tag.find_parent("a") is not None)
        if tag.find_parent("a"):
            print("Link href:", tag.find_parent("a").get("href"))

print("\n=== 2. SOCIAL LINKS (HEADER & FOOTER) ===")
for a in soup.find_all("a"):
    href = a.get("href", "")
    txt = a.get_text(" ", strip=True)
    classes = " ".join(a.get("class", []))
    if any(k in href.lower() or k in txt.lower() or k in classes.lower() for k in ["facebook", "twitter", "linkedin", "instagram"]):
        print(f"Social link -> Text: '{txt}' | href: '{href}' | class: '{classes}'")

print("\n=== 3. BANNER BUTTON 'OUR SERVICES' ===")
for a in soup.find_all("a"):
    txt = a.get_text(" ", strip=True)
    if "service" in txt.lower():
        print(f"Service button/link -> Text: '{txt}' | href: '{a.get('href')}' | class: '{a.get('class')}'")
