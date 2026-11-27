import openpyxl
import csv
from collections import defaultdict, Counter

# 1. Load Google Ads Location report
wb = openpyxl.load_workbook('data/Pet Mode/Location report.xlsx', data_only=True)
ws = wb.active

google_locations = []
for r in range(4, ws.max_row + 1):
    loc = ws.cell(r, 1).value
    if not loc or loc.startswith('Total:'):
        continue
    clicks = float(ws.cell(r, 2).value or 0)
    impr = float(ws.cell(r, 3).value or 0)
    ctr = float(ws.cell(r, 4).value or 0)
    cpc = float(ws.cell(r, 6).value or 0)
    cost = float(ws.cell(r, 7).value or 0)
    conv_rate = float(ws.cell(r, 8).value or 0)
    conv = float(ws.cell(r, 9).value or 0)
    cpa = float(ws.cell(r, 10).value or 0)
    google_locations.append({
        'location': loc,
        'clicks': clicks,
        'impr': impr,
        'cost': cost,
        'conv': conv,
        'cpa': cpa,
        'conv_rate': conv_rate,
        'cpc': cpc
    })

google_locations.sort(key=lambda x: x['cost'], reverse=True)

# 2. Load Shopify Orders by City / Region
shopify_orders = []
with open('data/Pet Mode/orders_export.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        shopify_orders.append(row)

# Deduplicate orders
unique_orders = {}
for o in shopify_orders:
    unique_orders[o['Name']] = o

city_counts = Counter()
province_counts = Counter()
total_sales_by_city = defaultdict(float)

for o in unique_orders.values():
    city = (o['Shipping City'] or o['Billing City'] or 'Unknown').strip().title()
    prov = (o['Shipping Province'] or o['Billing Province'] or 'Unknown').strip().title()
    total = float(o['Total'] or 0)
    city_counts[city] += 1
    province_counts[prov] += 1
    total_sales_by_city[city] += total

print("=== GOOGLE ADS LOCATION PERFORMANCE ===")
print(f"{'Location':40} | {'Spend':>8} | {'Clicks':>6} | {'Conv':>5} | {'CPA':>8} | {'Conv Rate':>9}")
print("-" * 85)
for g in google_locations:
    print(f"{g['location'][:40]:40} | £{g['cost']:7.2f} | {g['clicks']:6.0f} | {g['conv']:5.1f} | £{g['cpa']:7.2f} | {g['conv_rate']*100:8.2f}%")

print("\n=== TOP 20 SHOPIFY ORDER CITIES ===")
print(f"{'City':30} | {'Orders':>6} | {'Revenue':>9}")
print("-" * 50)
for city, count in city_counts.most_common(20):
    print(f"{city:30} | {count:6d} | £{total_sales_by_city[city]:8.2f}")
