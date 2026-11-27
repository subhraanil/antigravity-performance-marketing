import openpyxl, os

path = r"C:\Users\test\Videos\Office\data\fabb6\November\Search terms report (9).xlsx"
wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
sheet = wb.active

junk_keywords = ['gym', 'badminton', 'cricket', 'fitness', 'exercise', 'push up', 'equipment', 'shoes', 'cycle', 'bike', 'board', 'table', 'chair', 'car', 'phone', 'mobile']

total_spend = 0.0
total_clicks = 0
junk_spend = 0.0
junk_clicks = 0
junk_samples = []

row_idx = 0
for row in sheet.iter_rows(min_row=4, values_only=True):
    row_idx += 1
    term = str(row[0]).lower() if row[0] else ''
    clicks = float(row[5]) if row[5] else 0.0
    cost = float(row[10]) if row[10] else 0.0
    conv = float(row[13]) if row[13] else 0.0
    
    total_spend += cost
    total_clicks += clicks
    
    if any(k in term for k in junk_keywords):
        junk_spend += cost
        junk_clicks += clicks
        if cost > 50 or clicks > 10:
            junk_samples.append((term, clicks, cost, conv))
    
    if row_idx >= 50000: # process first 50k rows
        break

print(f"Scanned {row_idx} search term rows:")
print(f"Total Cost scanned: Rs {total_spend:,.2f} | Total Clicks: {total_clicks:,.0f}")
print(f"Direct Junk Spend Identified: Rs {junk_spend:,.2f} | Junk Clicks: {junk_clicks:,.0f}")
print("\nSample High-Cost Junk Search Terms:")
for s in sorted(junk_samples, key=lambda x: x[2], reverse=True)[:25]:
    print(f"  - '{s[0]}': Clicks: {s[1]}, Cost: Rs {s[2]:,.2f}, Conv: {s[3]}")
