import os
import glob
import csv
from collections import defaultdict

base_dir = r'C:\Users\test\Videos\Office\data\fabb6\Shopify Order'
csv_files = glob.glob(os.path.join(base_dir, '**', '*.csv'), recursive=True)

orders = {}

for fpath in sorted(csv_files):
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('Name')
            if not name:
                continue
            cat = row.get('Created at', '')
            q = float(row['Lineitem quantity']) if row.get('Lineitem quantity') else 0.0
            p = float(row['Lineitem price']) if row.get('Lineitem price') else 0.0
            line_val = q * p
            
            if name not in orders:
                orders[name] = {
                    'created_at': cat,
                    'line_gross': line_val,
                    'subtotal': float(row['Subtotal']) if row.get('Subtotal') else 0.0,
                    'discount': float(row['Discount Amount']) if row.get('Discount Amount') else 0.0,
                    'total': float(row['Total']) if row.get('Total') else 0.0,
                    'taxes': float(row['Taxes']) if row.get('Taxes') else 0.0,
                    'shipping': float(row['Shipping']) if row.get('Shipping') else 0.0,
                    'cancelled': bool(row.get('Cancelled at', '').strip()),
                    'financial_status': row.get('Financial Status', '').strip()
                }
            else:
                orders[name]['line_gross'] += line_val

# Group by month
months = defaultdict(lambda: {
    'all_orders': 0,
    'all_gross': 0.0,
    'all_subtotal': 0.0,
    'all_discount': 0.0,
    'all_total': 0.0,
    'non_canc_orders': 0,
    'non_canc_gross': 0.0,
    'non_canc_subtotal': 0.0,
    'cancelled_orders': 0
})

for name, o in orders.items():
    cat = o['created_at']
    mkey = cat[:7] if cat else 'Unknown'
    m = months[mkey]
    
    m['all_orders'] += 1
    m['all_gross'] += o['line_gross']
    m['all_subtotal'] += o['subtotal']
    m['all_discount'] += o['discount']
    m['all_total'] += o['total']
    
    if not o['cancelled']:
        m['non_canc_orders'] += 1
        m['non_canc_gross'] += o['line_gross']
        m['non_canc_subtotal'] += o['subtotal']
    else:
        m['cancelled_orders'] += 1

print("\n--- DETAILED MONTHLY ANALYSIS ---")
for mk in sorted(months.keys()):
    if mk < '2025-12' and mk != 'Unknown':
        continue
    m = months[mk]
    all_ord = m['all_orders']
    all_g = m['all_gross']
    all_aov = all_g / all_ord if all_ord else 0
    
    nc_ord = m['non_canc_orders']
    nc_g = m['non_canc_gross']
    nc_aov = nc_g / nc_ord if nc_ord else 0
    
    canc_rate = (m['cancelled_orders'] / all_ord * 100) if all_ord else 0
    
    print(f"Month {mk}:")
    print(f"  [All Orders]      Count: {all_ord:>6,d} | Gross Sales: ₹{all_g:>12,.2f} ({all_g/1e5:>6.2f}L) | AOV: ₹{all_aov:>8.2f}")
    print(f"  [Non-Cancelled]   Count: {nc_ord:>6,d} | Gross Sales: ₹{nc_g:>12,.2f} ({nc_g/1e5:>6.2f}L) | AOV: ₹{nc_aov:>8.2f}")
    print(f"  [Discounts/Canc]  Disc: ₹{m['all_discount']:>10,.2f} | Canc Orders: {m['cancelled_orders']:>5,d} ({canc_rate:.1f}%)")
