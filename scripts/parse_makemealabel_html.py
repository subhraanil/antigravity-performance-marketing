import csv
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

sf_internal_path = r'website audit/makemealabel.com/internal_all.csv'

html_pages = []

with open(sf_internal_path, 'r', encoding='utf-8-sig', errors='ignore') as f:
    reader = csv.DictReader(f)
    for row in reader:
        ct = row.get("Content Type", "")
        if "text/html" in ct:
            html_pages.append(row)

print(f"Total HTML Pages: {len(html_pages)}")

# Categorize URLs
products = []
collections = []
policies = []
pages = []
blogs = []
other = []

for p in html_pages:
    u = p.get("Address", "")
    if "/products/" in u:
        products.append(p)
    elif "/collections/" in u:
        collections.append(p)
    elif "/policies/" in u:
        policies.append(p)
    elif "/pages/" in u:
        pages.append(p)
    elif "/blogs/" in u:
        blogs.append(p)
    else:
        other.append(p)

print(f"\nBreakdown by Type:")
print(f"  Products: {len(products)}")
print(f"  Collections: {len(collections)}")
print(f"  Policies: {len(policies)}")
print(f"  Pages: {len(pages)}")
print(f"  Blogs: {len(blogs)}")
print(f"  Other (Home, Cart, etc.): {len(other)}")

print("\n--- SAMPLE PRODUCTS ---")
for p in products[:8]:
    print(f"URL: {p.get('Address')}")
    print(f"  Title ({p.get('Title 1 Length')} ch): {p.get('Title 1')}")
    print(f"  Meta Desc ({p.get('Meta Description 1 Length')} ch): {p.get('Meta Description 1')[:60]}...")
    print(f"  H1: {p.get('H1-1')}")
    print(f"  Words: {p.get('Word Count')} | Status: {p.get('Status Code')} | Indexability: {p.get('Indexability')}")
    print(f"  Canonical: {p.get('Canonical Link Element 1')}")

print("\n--- COLLECTIONS ---")
for c in collections:
    print(f"URL: {c.get('Address')}")
    print(f"  Title: {c.get('Title 1')}")
    print(f"  H1: {c.get('H1-1')} | Words: {c.get('Word Count')}")

print("\n--- PAGES & POLICIES ---")
for pg in pages + policies:
    print(f"URL: {pg.get('Address')} | Title: {pg.get('Title 1')} | Words: {pg.get('Word Count')}")

print("\n--- OTHER ---")
for o in other:
    print(f"URL: {o.get('Address')} | Title: {o.get('Title 1')}")
