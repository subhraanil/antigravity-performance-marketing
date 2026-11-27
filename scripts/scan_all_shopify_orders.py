import os
import glob
import csv
from collections import defaultdict
import datetime

base_dir = r'C:\Users\test\Videos\Office\data\fabb6\Shopify Order'
csv_files = glob.glob(os.path.join(base_dir, '**', '*.csv'), recursive=True)

print(f"Total CSV files found: {len(csv_files)}")

file_summary = []
for fpath in sorted(csv_files):
    fname = os.path.basename(fpath)
    parent = os.path.basename(os.path.dirname(fpath))
    min_date = None
    max_date = None
    order_names = set()
    row_count = 0
    
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row_count += 1
            name = row.get('Name')
            if name:
                order_names.add(name)
            created_at = row.get('Created at')
            if created_at:
                dt_str = created_at[:10]
                if min_date is None or dt_str < min_date:
                    min_date = dt_str
                if max_date is None or dt_str > max_date:
                    max_date = dt_str
                    
    print(f"{parent}/{fname}: Rows={row_count}, Orders={len(order_names)}, Range={min_date} to {max_date}")
