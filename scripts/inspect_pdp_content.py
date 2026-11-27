import requests
from bs4 import BeautifulSoup
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

pdp_url = "https://makemealabel.com/products/100mm-x-152mm-6-by-4-direct-thermal-roll-labels"
r = requests.get(pdp_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
soup = BeautifulSoup(r.text, "html.parser")

# Product description
desc = soup.find(class_=lambda x: x and "description" in x.lower()) or soup.find("div", class_="product__description")
print("=== PRODUCT MAIN DESCRIPTION ===")
if desc:
    print(desc.get_text("\n", strip=True))
else:
    print("[No specific product description container found]")

# Inspect accordion details
print("\n=== DETAILS / ACCORDIONS ===")
for d in soup.find_all("details"):
    summary = d.find("summary")
    sum_text = summary.get_text(strip=True) if summary else "No summary"
    body_text = d.get_text(" ", strip=True)
    print(f"Summary: '{sum_text}'")
    print(f"  Body: '{body_text}'\n")

# Check product form inputs
print("=== PRODUCT ADD TO CART FORM ===")
cart_add_form = soup.find("form", action="/cart/add")
if cart_add_form:
    for inp in cart_add_form.find_all(["input", "select", "button"]):
        print(f"<{inp.name}> name='{inp.get('name')}', type='{inp.get('type')}', value='{inp.get('value')}', text='{inp.get_text(strip=True)}'")
