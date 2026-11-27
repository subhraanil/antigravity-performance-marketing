import requests
import json
from bs4 import BeautifulSoup

headers = {'User-Agent': 'SEO-Audit-Bot/1.0 (+contact: client-audit)'}

print("=== 1. SITEMAP.XML ===")
r_sitemap = requests.get('https://victoryhcspl.com/sitemap.xml', headers=headers, timeout=15)
print("Sitemap snippet:\n", r_sitemap.text[:600])

soup = BeautifulSoup(r_sitemap.text, 'xml')
locs = [loc.text.strip() for loc in soup.find_all('loc')]
print("Sitemap loc count:", len(locs))
for l in locs:
    print(" -", l)

print("\n=== 2. PAGE-SITEMAP.XML ===")
r_page_sitemap = requests.get('https://victoryhcspl.com/page-sitemap.xml', headers=headers, timeout=15)
soup_p = BeautifulSoup(r_page_sitemap.text, 'xml')
page_locs = [loc.text.strip() for loc in soup_p.find_all('loc')]
print("Page-sitemap loc count:", len(page_locs))
for l in page_locs:
    print(" -", l)

print("\n=== 3. WP-JSON PAGES ===")
r_pages = requests.get('https://victoryhcspl.com/wp-json/wp/v2/pages?per_page=100', headers=headers, timeout=15)
print("WP-JSON pages status:", r_pages.status_code)
if r_pages.status_code == 200:
    pages_data = r_pages.json()
    print("WP-JSON pages count:", len(pages_data))
    for p in pages_data:
        pid = p.get('id')
        slug = p.get('slug')
        link = p.get('link')
        title = p.get('title', {}).get('rendered', '')
        print(f" - ID: {pid} | Slug: {slug} | Title: {title} | Link: {link}")

print("\n=== 4. WP-JSON POSTS ===")
r_posts = requests.get('https://victoryhcspl.com/wp-json/wp/v2/posts?per_page=100', headers=headers, timeout=15)
print("WP-JSON posts status:", r_posts.status_code)
if r_posts.status_code == 200:
    posts_data = r_posts.json()
    print("WP-JSON posts count:", len(posts_data))
    for p in posts_data:
        print(" - Post:", p.get('id'), p.get('slug'), p.get('link'))

print("\n=== 5. WP-JSON USERS / AUTHORS ===")
r_users = requests.get('https://victoryhcspl.com/wp-json/wp/v2/users', headers=headers, timeout=15)
print("WP-JSON users status:", r_users.status_code)
if r_users.status_code == 200:
    users_data = r_users.json()
    print("WP-JSON users count:", len(users_data))
    for u in users_data:
        print(" - User:", u.get('id'), u.get('name'), u.get('slug'))
