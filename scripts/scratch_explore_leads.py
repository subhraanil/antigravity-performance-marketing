import openpyxl
wb = openpyxl.load_workbook(r'C:\Users\test\.gemini\antigravity\brain\cc612d54-d8d2-4a43-a285-4bda2d3e91ba\.user_uploaded\media_1795518002487_5ba75fc4.xlsx', read_only=True)
ws = wb.active
rows = list(ws.rows)
headers = [str(c.value) for c in rows[0]]

src_idx = headers.index('Source')
date_idx = headers.index('Query Date & Time')

from collections import Counter

# 'Supervisor Panel' is the source for leads manually entered by associates/supervisors
# Let's also check a few more details:
print('=== Rows where Source = Supervisor Panel: Referred Associate distribution ===')
sp_ref = Counter()
for row in rows[1:]:
    src = str(row[src_idx].value).strip()
    ra = str(row[headers.index('Referred Associate')].value).strip()
    if src == 'Supervisor Panel':
        sp_ref[ra] += 1
for k, v in sp_ref.most_common(10):
    print(f'  "{k}": {v}')

print()
print('=== Rows where Source = Supervisor Panel: Assigned To (Sales Team) ===')
sp_sales = Counter()
for row in rows[1:]:
    src = str(row[src_idx].value).strip()
    st = str(row[headers.index('Assigned To (Sales Team)')].value).strip()
    if src == 'Supervisor Panel':
        sp_sales[st] += 1
for k, v in sp_sales.most_common(10):
    print(f'  "{k}": {v}')

print()
print('=== Month-wise Supervisor Panel lead count ===')
sp_month = Counter()
total_month = Counter()
for row in rows[1:]:
    src = str(row[src_idx].value).strip()
    raw_date = str(row[date_idx].value).strip()
    try:
        # format: 2025-01-11 00:00:00 or 2026-11-01 00:00:00
        yr = raw_date[:4]
        mo = raw_date[5:7]
        label = f"{yr}-{mo}"
    except:
        label = "Unknown"
    total_month[label] += 1
    if src == 'Supervisor Panel':
        sp_month[label] += 1

print(f"{'Month':<12} {'Supervisor Panel':>18} {'Total Leads':>12} {'% of Total':>12}")
for k in sorted(total_month.keys()):
    sp = sp_month.get(k, 0)
    tot = total_month[k]
    pct = round(sp / tot * 100, 1) if tot else 0
    print(f"{k:<12} {sp:>18} {tot:>12} {pct:>11}%")

print(f"\n{'TOTAL':<12} {sum(sp_month.values()):>18} {sum(total_month.values()):>12}")

wb.close()
