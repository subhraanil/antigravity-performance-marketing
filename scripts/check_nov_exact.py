import os
import glob
import csv

base_dir = r'C:\Users\test\Videos\Office\data\fabb6\Shopify Order'
csv_files = glob.glob(os.path.join(base_dir, '**', '*.csv'), recursive=True)

nov_orders = {}

for fpath in sorted(csv_files):
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('Name')
            cat = row.get('Created at', '')
            if not name or not cat:
                continue
            
            dt = cat[:10]
            if dt.startswith('2026-11'):
                q = float(row['Lineitem quantity']) if row.get('Lineitem quantity') else 0.0
                p = float(row['Lineitem price']) if row.get('Lineitem price') else 0.0
                if name not in nov_orders:
                    nov_orders[name] = {
                        'date': dt,
                        'created_at': cat,
                        'gross': q * p,
                        'cancelled': bool(row.get('Cancelled at', '').strip())
                    }
                else:
                    nov_orders[name]['gross'] += q * p

orders_to_18 = [o for o in nov_orders.values() if o['date'] <= '2026-11-18']
orders_all_nov = list(nov_orders.values())

gross_to_18 = sum(o['gross'] for o in orders_to_18)
gross_all_nov = sum(o['gross'] for o in orders_all_nov)

print(f"Nov 1-18 Unique Orders: {len(orders_to_18)}")
print(f"Nov 1-18 Gross Sales: ₹{gross_to_18:,.2f} (₹{gross_to_18/1e5:.2f}L)")
print(f"Nov 1-18 AOV: ₹{gross_to_18/len(orders_to_18):,.2f}")
print("---")
print(f"Nov 1-24 Full MTD Orders: {len(orders_all_nov)}")
print(f"Nov 1-24 Full MTD Gross Sales: ₹{gross_all_nov:,.2f} (₹{gross_all_nov/1e5:.2f}L)")
print(f"Nov 1-24 Full MTD AOV: ₹{gross_all_nov/len(orders_all_nov):,.2f}")
