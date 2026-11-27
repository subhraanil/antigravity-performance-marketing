import openpyxl
import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook(r'c:\Users\test\Videos\Office\data\Pet Mode\Negative keyword details report.xlsx', data_only=True)
ws = wb.active
rows = []
for r in range(4, ws.max_row + 1):
    kw = ws.cell(r, 1).value
    mt = ws.cell(r, 2).value
    if kw:
        rows.append({'keyword': str(kw).strip().lower(), 'match_type': mt})

df = pd.DataFrame(rows)
print(f"Total negatives in list: {len(df)}")
print("Match types:")
print(df['match_type'].value_counts())

print("\nSample of negatives:")
print(df.head(40).to_string())

# Check for specific items
keywords_set = set(df['keyword'])
checks = ['gps', 'tracker', 'sim card', 'subscription', 'airtag', 'air tag', 'apple', 'shoes', 'boots', 'funnyfuzzy', 'by teddy', 'speedy tail', 'pets at home', 'pep mills', 'free', 'diy', 'cheap', 'fountain', 'teeth', 'dental']
print("\n=== COVERAGE CHECK ===")
for c in checks:
    matched = [k for k in keywords_set if c in k]
    print(f"Check '{c}': {matched}")
