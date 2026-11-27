import os
import glob
import csv
from collections import defaultdict
import datetime

base_dir = r'C:\Users\test\Videos\Office\data\fabb6\Shopify Order'
csv_files = glob.glob(os.path.join(base_dir, '**', '*.csv'), recursive=True)

print(f"Scanning {len(csv_files)} files...")

# Unique orders: order_name -> order_dict
orders = {}

for fpath in sorted(csv_files):
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('Name')
            if not name:
                continue
            
            created_at = row.get('Created at', '')
            q = float(row['Lineitem quantity']) if row.get('Lineitem quantity') else 0.0
            p = float(row['Lineitem price']) if row.get('Lineitem price') else 0.0
            line_val = q * p
            
            if name not in orders:
                subtotal = float(row['Subtotal']) if row.get('Subtotal') else 0.0
                discount = float(row['Discount Amount']) if row.get('Discount Amount') else 0.0
                total = float(row['Total']) if row.get('Total') else 0.0
                shipping = float(row['Shipping']) if row.get('Shipping') else 0.0
                taxes = float(row['Taxes']) if row.get('Taxes') else 0.0
                cancelled_at = row.get('Cancelled at', '').strip()
                financial_status = row.get('Financial Status', '').strip()
                
                orders[name] = {
                    'created_at': created_at,
                    'subtotal': subtotal,
                    'discount': discount,
                    'total': total,
                    'shipping': shipping,
                    'taxes': taxes,
                    'cancelled_at': cancelled_at,
                    'financial_status': financial_status,
                    'line_gross': line_val,
                    'line_count': 1
                }
            else:
                orders[name]['line_gross'] += line_val
                orders[name]['line_count'] += 1

print(f"Total unique orders parsed: {len(orders)}")

# Month-wise aggregation
# We will track:
# 1. All placed orders
# 2. Non-cancelled orders (cancelled_at == '')
months_all = defaultdict(lambda: {
    'orders': 0,
    'gross_line': 0.0,
    'subtotal': 0.0,
    'discount': 0.0,
    'total': 0.0,
    'taxes': 0.0,
    'shipping': 0.0,
    'cancelled_orders': 0,
    'cancelled_gross': 0.0
})

for name, o in orders.items():
    cat = o['created_at']
    if not cat:
        month_key = 'Unknown'
    else:
        month_key = cat[:7] # YYYY-MM
    
    m = months_all[month_key]
    m['orders'] += 1
    m['gross_line'] += o['line_gross']
    m['subtotal'] += o['subtotal']
    m['discount'] += o['discount']
    m['total'] += o['total']
    m['taxes'] += o['taxes']
    m['shipping'] += o['shipping']
    
    if o['cancelled_at']:
        m['cancelled_orders'] += 1
        m['cancelled_gross'] += o['line_gross']

print("\n" + "="*110)
print(f"{'Month':<10} | {'Total Orders':<12} | {'Gross Sales (Line)':<18} | {'Gross AOV':<12} | {'Non-Canc Orders':<15} | {'Non-Canc Gross':<16} | {'Non-Canc AOV':<12}")
print("="*110)

sorted_months = sorted(months_all.keys())
for mk in sorted_months:
    m = months_all[mk]
    tot_orders = m['orders']
    gross_val = m['gross_line']
    gross_aov = gross_val / tot_orders if tot_orders > 0 else 0.0
    
    non_canc_orders = tot_orders - m['cancelled_orders']
    non_canc_gross = gross_val - m['cancelled_gross']
    non_canc_aov = non_canc_gross / non_canc_orders if non_canc_orders > 0 else 0.0
    
    print(f"{mk:<10} | {tot_orders:<12,d} | ₹{gross_val:<16,.2f} | ₹{gross_aov:<10,.2f} | {non_canc_orders:<15,d} | ₹{non_canc_gross:<14,.2f} | ₹{non_canc_aov:<10,.2f}")

print("="*110)
