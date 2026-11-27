import requests
from bs4 import BeautifulSoup
import json
from playwright.sync_api import sync_playwright

pdp_url = "https://makemealabel.com/products/100mm-x-152mm-6-by-4-direct-thermal-roll-labels"
col_url = "https://makemealabel.com/collections/direct-thermal-roll-labels-blank"

print("=== 1. PRODUCT PAGE (PDP) RAW HTML INSPECTION ===")
r_pdp = requests.get(pdp_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
soup_pdp = BeautifulSoup(r_pdp.text, "html.parser")

print("PDP Title:", soup_pdp.title.string if soup_pdp.title else "[NONE]")
m_desc = soup_pdp.find("meta", attrs={"name": "description"})
print("PDP Meta Desc:", m_desc["content"] if m_desc else "[NONE]")
h1s = [h.get_text(" ", strip=True) for h in soup_pdp.find_all("h1")]
print(f"PDP H1 Count: {len(h1s)} | Text: {h1s}")
h2s = [h.get_text(" ", strip=True) for h in soup_pdp.find_all("h2")]
print(f"PDP H2 Count: {len(h2s)} | Text: {h2s[:5]}")

# Schema LD+JSON
pdp_schemas = []
for s in soup_pdp.find_all("script", type="application/ld+json"):
    try:
        d = json.loads(s.string or "{}")
        pdp_schemas.append(d)
    except:
        pdp_schemas.append("INVALID_JSON")

print(f"PDP Schema count: {len(pdp_schemas)}")
for idx, s in enumerate(pdp_schemas):
    if isinstance(s, dict):
        print(f" Schema {idx}: @type = {s.get('@type')}")
        if s.get("@type") == "Product":
            print(f"   Product Name: {s.get('name')}")
            print(f"   SKU: {s.get('sku')} | GTIN/Barcode: {s.get('gtin') or s.get('gtin12') or s.get('gtin13') or s.get('barcode')}")
            print(f"   Brand: {s.get('brand')}")
            offers = s.get("offers", {})
            if isinstance(offers, list): offers = offers[0] if offers else {}
            print(f"   Offers: Price = {offers.get('price')} {offers.get('priceCurrency')}, Availability = {offers.get('availability')}")
            print(f"   AggregateRating: {s.get('aggregateRating')}")
            print(f"   Reviews: {len(s.get('review', [])) if isinstance(s.get('review'), list) else s.get('review')}")

# Breadcrumbs
breadcrumbs = soup_pdp.find("nav", attrs={"aria-label": "Breadcrumb"}) or soup_pdp.find(class_=lambda x: x and "breadcrumb" in x.lower())
print("Breadcrumbs found:", "YES" if breadcrumbs else "NO")

# Images
imgs = soup_pdp.find_all("img")
print(f"PDP Image count: {len(imgs)}")
no_alt = [img for img in imgs if not img.get("alt") or not img.get("alt").strip()]
print(f"PDP Images missing alt text: {len(no_alt)}")

print("\n=== 2. PLAYWRIGHT INTERACTIVE E-COMMERCE AUDIT (PDP & CART) ===")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    page.goto(pdp_url, wait_until="networkidle")
    
    # Check Price display
    price_el = page.query_selector(".price, [data-price], .product__price")
    print("Price text on screen:", price_el.inner_text().strip() if price_el else "[Not found]")
    
    # Check VAT notice
    body_text = page.inner_text("body")
    has_vat = "vat" in body_text.lower()
    print("VAT mentioned on page (inc/ex VAT):", has_vat)
    
    # Check Variant selectors
    variants = page.query_selector_all("select, [role='radiogroup'], fieldset, .product-form__input")
    print(f"Variant selector blocks: {len(variants)}")
    for v in variants:
        print("  Variant block:", v.inner_text().replace("\n", " ")[:80])
        
    # Check Quantity Breaks / Bulk Tier Pricing
    has_bulk = any(term in body_text.lower() for term in ["bulk", "quantity discount", "buy more", "tier", "pack of"])
    print("Bulk / Tier Pricing table visible:", has_bulk)
    
    # Check Compatibility info
    has_zebra = "zebra" in body_text.lower()
    print("Printer compatibility (Zebra/Citizen/etc.) mentioned:", has_zebra)
    
    # Check Reviews widget
    has_reviews = any(term in body_text.lower() for term in ["customer reviews", "star rating", "write a review", "based on"])
    print("Reviews section visible:", has_reviews)
    
    # Check Add to Cart button
    atc_btn = page.query_selector("button[name='add'], button:has-text('Add to cart')")
    print("Add to Cart button found:", "YES" if atc_btn else "NO")
    if atc_btn:
        print("Add to Cart button text:", atc_btn.inner_text().strip())
        
    # Check UK Shipping notice
    has_shipping_notice = any(term in body_text.lower() for term in ["delivery", "shipping", "royal mail", "dpd", "next day"])
    print("Shipping / UK Delivery notice on PDP:", has_shipping_notice)
    
    # Mobile Viewport Check (390px)
    print("\n=== 3. MOBILE VIEWPORT (390px) PDP AUDIT ===")
    page_m = browser.new_page(viewport={"width": 390, "height": 844})
    page_m.goto(pdp_url, wait_until="networkidle")
    
    atc_m = page_m.query_selector("button[name='add'], button:has-text('Add to cart')")
    if atc_m:
        box = atc_m.bounding_box()
        print("Mobile Add to Cart Button Bounding Box:", box)
        
    # Sticky Add to Cart
    page_m.evaluate("window.scrollTo(0, 1500)")
    page_m.wait_for_timeout(500)
    sticky_atc = page_m.query_selector(".sticky-cart, [data-sticky-cart], button:has-text('Add to cart'):visible")
    print("Sticky Add to Cart present on scroll:", "YES" if sticky_atc else "NO")

    browser.close()

print("\nPDP audit complete.")
