import os
import glob
import csv
from collections import defaultdict

base_dir = r'C:\Users\test\Videos\Office\data\fabb6\Shopify Order'
csv_files = glob.glob(os.path.join(base_dir, '**', '*.csv'), recursive=True)

nov_18_orders = 0
nov_18_gross = 0.0
nov_all_orders = 0
nov_all_gross = 0.0

diff_count = 0

for fpath in sorted(csv_files):
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('Name')
            cat = row.get('Created at', '')
            if not cat:
                continue
            
            # First row of order has created_at
            dt = cat[:10]
            if dt.startswith('2026-11'):
                nov_all_orders += 1
                if dt <= '2026-11-18':
                    nov_18_orders += 1

print(f"Nov 1-18 Orders count in Shopify raw: {nov_18_orders}")
print(f"Nov 1-24 Orders count in Shopify raw: {nov_all_orders}")
