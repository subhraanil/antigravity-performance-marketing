import csv

p1 = r'website audit\internal_html.csv'
p2 = r'website audit\issues_overview_report.csv'

print('=== INTERNAL_HTML.CSV ===')
with open(p1, 'r', encoding='utf-8', errors='ignore') as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        if i == 0:
            print('Columns count:', len(row))
            print('Header preview:', row[:15])
        else:
            url = row[0] if len(row) > 0 else ''
            ct = row[1] if len(row) > 1 else ''
            sc = row[2] if len(row) > 2 else ''
            idx = row[4] if len(row) > 4 else ''
            title = row[6] if len(row) > 6 else ''
            h1 = row[14] if len(row) > 14 else ''
            meta = row[9] if len(row) > 9 else ''
            print(f"Row {i:2d}: [{sc}] ({idx}) {url}")
            print(f"        Title: {title[:40]} | H1: {h1[:40]} | Meta: {meta[:40]}")

print('\n=== ISSUES_OVERVIEW_REPORT.CSV ===')
with open(p2, 'r', encoding='utf-8', errors='ignore') as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        if row:
            print(f"Issue {i:2d}: {row[:4]}")
