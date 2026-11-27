import urllib.request
import json
import ssl
import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 1. Fetch products.json from Shopify
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(
    'https://petmode.co.uk/products.json?limit=250',
    headers={'User-Agent': 'Mozilla/5.0'}
)
with urllib.request.urlopen(req, context=ctx) as resp:
    data = json.loads(resp.read().decode('utf-8'))

products = data.get('products', [])

# 2. Load Shopify orders export
df_orders = pd.read_csv(r'c:\Users\test\Videos\Office\data\Pet Mode\orders_export.csv', low_memory=False)
order_items = df_orders.groupby('Lineitem name').agg(
    orders=('Lineitem quantity', 'count'),
    units=('Lineitem quantity', lambda x: pd.to_numeric(x, errors='coerce').fillna(1).sum()),
    revenue=('Total', lambda x: pd.to_numeric(x, errors='coerce').fillna(0).sum())
).reset_index().sort_values(by='units', ascending=False)

print(f"Total live products on petmode.co.uk: {len(products)}")
print(f"Top 15 ordered lineitems in history:")
print(order_items.head(15).to_string(index=False))

# Match orders with live products
print("\n=== MATCHING TOP PRODUCTS WITH LIVE SHOPPE CATALOG ===")
for p in products:
    t = p['title'].lower()
    h = p['handle'].lower()
    for kw in ['tooth', 'molar', 'chew', 'bark', 'car seat', 'steam', 'scratch', 'cooling', 'roller', 'gps', 'necklace', 'fountain', 'bed']:
        if kw in t or kw in h:
            in_stock = any(v['available'] for v in p['variants'])
            prices = [float(v['price']) for v in p['variants']]
            min_p = min(prices) if prices else 0
            max_p = max(prices) if prices else 0
            print(f"- Title: {p['title']}")
            print(f"  Handle: {p['handle']} | InStock: {in_stock} | Price: £{min_p:.2f} - £{max_p:.2f} | Variants: {len(p['variants'])}")
            break
