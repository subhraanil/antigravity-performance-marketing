import requests
from bs4 import BeautifulSoup

pdp_url = "https://makemealabel.com/products/100mm-x-152mm-6-by-4-direct-thermal-roll-labels"
r = requests.get(pdp_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
soup = BeautifulSoup(r.text, "html.parser")

print("=== PDP ACCORDIONS & SECTIONS ===")
for h2 in soup.find_all("h2"):
    parent = h2.find_parent("details") or h2.find_parent("div")
    text_content = parent.get_text(" ", strip=True) if parent else ""
    print(f"H2: '{h2.get_text(strip=True)}'")
    print(f"   Content Preview: {text_content[:150]}...\n")

print("=== PDP BUTTONS & FORMS ===")
for form in soup.find_all("form"):
    print(f"Form action: {form.get('action')}, method: {form.get('method')}")
    for btn in form.find_all(["button", "input"]):
        print(f"  Element: <{btn.name}> type='{btn.get('type')}', name='{btn.get('name')}', text='{btn.get_text(strip=True)}', value='{btn.get('value')}'")

print("=== CHECKOUT / CART LINKS ===")
for a in soup.find_all("a", href=True):
    if any(k in a["href"] for k in ["cart", "checkout", "account"]):
        print(f"Link: href='{a['href']}', text='{a.get_text(strip=True)}'")
