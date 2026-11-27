import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

url = "https://www.panelright.com/faq"
r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')

print("=== RAW HTML CHECK ===")
h3s = soup.find_all('h3')
print("Total H3 elements:", len(h3s))
for h in h3s[:3]:
    print("Question:", h.get_text(strip=True))
    sib = h.find_next_sibling()
    print("Sibling:", sib)

print("\n=== PLAYWRIGHT RENDERED DOM CHECK ===")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url, wait_until="load")
    # Click first question if accordion
    first_q = page.query_selector('h3')
    if first_q:
        first_q.click()
        page.wait_for_timeout(1000)
    html = page.content()
    soup_rendered = BeautifulSoup(html, 'lxml')
    print("Rendered body text length:", len(soup_rendered.get_text()))
    for p_el in soup_rendered.find_all('p'):
        print("P tag:", p_el.get_text(strip=True)[:100])
    browser.close()
