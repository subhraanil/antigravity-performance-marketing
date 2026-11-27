import csv
import glob
import os

sample_csv = r'C:\Users\test\Videos\Office\data\fabb6\Shopify Order\orders_export_1\orders_export_1.csv'

with open(sample_csv, 'r', encoding='utf-8', errors='ignore') as f:
    reader = csv.DictReader(f)
    orders = {}
    for row in reader:
        name = row['Name']
        if name not in orders:
            orders[name] = []
        orders[name].append(row)
        if len(orders) >= 10:
            break

for name, rows in orders.items():
    r0 = rows[0]
    sub = float(r0.get('Subtotal') or 0)
    disc = float(r0.get('Discount Amount') or 0)
    tot = float(r0.get('Total') or 0)
    tax = float(r0.get('Taxes') or 0)
    ship = float(r0.get('Shipping') or 0)
    financial = r0.get('Financial Status')
    cancelled = r0.get('Cancelled at')
    created = r0.get('Created at')
    
    line_sum = 0
    for r in rows:
        q = float(r.get('Lineitem quantity') or 0)
        p = float(r.get('Lineitem price') or 0)
        line_sum += q * p

    print(f"Order: {name} | Created: {created} | Status: {financial} | Cancelled: {cancelled}")
    print(f"  Subtotal: {sub} | Disc: {disc} | Ship: {ship} | Tax: {tax} | Total: {tot}")
    print(f"  Sum of Lineitems (Qty*Price): {line_sum}")
    print(f"  Subtotal + Discount: {sub + disc}")
    print(f"  Total - Tax - Ship + Disc: {tot - tax - ship + disc}")
    print("-" * 50)
