from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    # 1. Test Mobile Viewport (iPhone 13 / 390x844) on Homepage
    page = browser.new_page(viewport={"width": 390, "height": 844}, user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1")
    page.goto("https://www.panelright.com/", wait_until="networkidle")
    
    print("=== MOBILE AUDIT: HOMEPAGE (390px) ===")
    tabs = page.query_selector_all("button, [role='tab'], a")
    print("Interactive elements count:", len(tabs))
    
    # Check industry tabs
    industry_elements = page.query_selector_all("text=Aviation, text=Marine, text=Medical, text=Automotive, text=Industrial, text=Consumer")
    for el in industry_elements:
        box = el.bounding_box()
        text = el.inner_text()
        print(f"Tab/Item '{text[:20]}': Bounding Box: {box}")

    # 2. Test Mobile Viewport & A11y on FAQ
    page.goto("https://www.panelright.com/faq", wait_until="networkidle")
    print("\n=== MOBILE & A11Y AUDIT: FAQ (390px) ===")
    accordion_triggers = page.query_selector_all("[data-radix-collection-item], button")
    for idx, trigger in enumerate(accordion_triggers):
        aria_expanded = trigger.get_attribute("aria-expanded")
        aria_controls = trigger.get_attribute("aria-controls")
        text = trigger.inner_text()[:40].strip()
        if text:
            print(f"Trigger {idx}: text='{text}', aria-expanded={aria_expanded}, aria-controls={aria_controls}")
            
    # Check if clicking expands and reveals text
    if accordion_triggers:
        first = accordion_triggers[0]
        first.click()
        page.wait_for_timeout(500)
        print("After click, aria-expanded:", first.get_attribute("aria-expanded"))
        # Check if content is now in DOM and visible
        visible_text = page.inner_text("body")
        print("Body text length after opening accordion:", len(visible_text))

    # 3. Test Contact Form on Mobile
    page.goto("https://solutions.panelright.com/contact", wait_until="networkidle")
    print("\n=== MOBILE AUDIT: CONTACT FORM ===")
    inputs = page.query_selector_all("input, textarea, button")
    for inp in inputs:
        inp_type = inp.get_attribute("type")
        inp_name = inp.get_attribute("name") or inp.get_attribute("id") or inp.get_attribute("placeholder")
        inp_box = inp.bounding_box()
        print(f"Input '{inp_name}' (type={inp_type}): Box: {inp_box}")

    browser.close()
print("Mobile & A11y verification completed.")
