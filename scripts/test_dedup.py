import os
import glob
import csv
from collections import defaultdict

base_dir = r'C:\Users\test\Videos\Office\data\fabb6\Shopify Order'
csv_files = glob.glob(os.path.join(base_dir, '**', '*.csv'), recursive=True)

# Order ID -> {created_at, subtotal, discount, total, cancelled_at, financial_status, lineitems}
orders = {}
duplicates = 0

for fpath in sorted(csv_files):
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        current_order = None
        for row in reader:
            name = row.get('Name')
            if not name:
                continue
            
            # Check if this row starts a new order or continues previous line item
            # In Shopify CSV, if row has 'Created at', it has the order header
            created_at = row.get('Created at')
            q = float(row['Lineitem quantity']) if row.get('Lineitem quantity') else 0
            p = float(row['Lineitem price']) if row.get('Lineitem price') else 0
            item_name = row.get('Lineitem name', '')

            if name not in orders:
                orders[name] = {
                    'created_at': created_at,
                    'subtotal': float(row['Subtotal']) if row.get('Subtotal') else 0.0,
                    'discount': float(row['Discount Amount']) if row.get('Discount Amount') else 0.0,
                    'total': float(row['Total']) if row.get('Total') else 0.0,
                    'shipping': float(row['Shipping']) if row.get('Shipping') else 0.0,
                    'financial_status': row.get('Financial Status', ''),
                    'cancelled_at': row.get('Cancelled at', ''),
                    'line_items': [(q, p, item_name)],
                    'sources': {os.path.basename(fpath)}
                }
            else:
                # If we've seen this order name before
                # Is it another line item in the same file or a duplicate across files?
                if os.path.basename(fpath) not in orders[name]['sources']:
                    duplicates += 1
                    orders[name]['sources'].add(os.path.basename(fpath))
                else:
                    # Same file, additional line item
                    orders[name]['line_items'].append((q, p, item_name))

print(f"Total unique orders: {len(orders)}")
print(f"Total cross-file order instances: {duplicates}")
