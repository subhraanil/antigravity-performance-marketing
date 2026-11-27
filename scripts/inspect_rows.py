import csv
fpath = r'C:\Users\test\Videos\Office\data\fabb6\Shopify Order\orders_export_1\orders_export_1.csv'
with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        if i < 15:
            print(f"Row {i}: Name={row.get('Name')}, Created={bool(row.get('Created at'))}, LineQty={row.get('Lineitem quantity')}, LineName={row.get('Lineitem name', '')[:30]}")
