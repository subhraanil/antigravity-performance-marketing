#!/usr/bin/env python3
"""
Inspect directory form fields for automated submission
"""
import sys
from playwright.sync_api import sync_playwright

test_urls = [
    ("techbehemoths", "https://techbehemoths.com/companies/get-listed"),
    ("sortlist", "https://www.sortlist.com/claim/agency"),
    ("callupcontact", "https://www.callupcontact.com/active/register/register.php?"),
    ("brownbook", "https://www.brownbook.net/register/"),
    ("cybo", "https://www.cybo.com/add-business/")
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    )

    for name, url in test_urls:
        try:
            print(f"\n==========================================")
            print(f"Testing {name}: {url}")
            print(f"==========================================")
            page.goto(url, timeout=30000, wait_until="domcontentloaded")
            page.wait_for_timeout(3000)
            print("Page title:", page.title())
            inputs = page.locator("input, textarea, select").all()
            print(f"Total interactive fields found: {len(inputs)}")
            for inp in inputs[:10]:
                tag = inp.evaluate("el => el.tagName.toLowerCase()")
                itype = inp.get_attribute("type") or ""
                iname = inp.get_attribute("name") or inp.get_attribute("id") or inp.get_attribute("placeholder") or ""
                print(f"  [{tag}:{itype}] name/id/placeholder: '{iname}'")
        except Exception as e:
            print(f"Error testing {name}: {e}")

    browser.close()
