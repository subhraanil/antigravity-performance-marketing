import csv

fpath = r'C:\Users\test\Videos\Office\data\fabb6\Shopify Order\orders_export_1\orders_export_1.csv'
orders = {}
with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row['Name']
        if name not in orders:
            orders[name] = {
                'subtotal': row['Subtotal'],
                'total': row['Total'],
                'discount': row['Discount Amount'],
                'taxes': row['Taxes'],
                'shipping': row['Shipping'],
                'financial_status': row['Financial Status'],
                'cancelled_at': row['Cancelled at'],
                'created_at': row['Created at'],
                'line_items': []
            }
        q = float(row['Lineitem quantity']) if row.get('Lineitem quantity') else 0
        p = float(row['Lineitem price']) if row.get('Lineitem price') else 0
        orders[name]['line_items'].append((q, p))

for name in list(orders.keys())[:15]:
    o = orders[name]
    gross_line = sum(q * p for q, p in o['line_items'])
    sub = float(o['subtotal']) if o['subtotal'] else 0
    disc = float(o['discount']) if o['discount'] else 0
    tot = float(o['total']) if o['total'] else 0
    ship = float(o['shipping']) if o['shipping'] else 0
    tax = float(o['taxes']) if o['taxes'] else 0
    print(f"Order {name}: GrossLine={gross_line:.2f}, Sub={sub:.2f}, Disc={disc:.2f}, Sub+Disc={sub+disc:.2f}, Ship={ship:.2f}, Tax={tax:.2f}, Tot={tot:.2f}, Cancelled={bool(o['cancelled_at'])}")
