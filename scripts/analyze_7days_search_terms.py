import openpyxl
import pandas as pd

file_path = r'c:\Users\test\Videos\Office\data\Pet Mode\Search terms report - pet mode 7 days.xlsx'
wb = openpyxl.load_workbook(file_path, data_only=True)
ws = wb.active

data = []
summary_rows = []
for r in range(4, ws.max_row + 1):
    st = ws.cell(r, 1).value
    if not st:
        continue
    if str(st).startswith('Total:'):
        summary_rows.append([ws.cell(r, c).value for c in range(1, 13)])
        continue
        
    match_type = ws.cell(r, 2).value
    added = ws.cell(r, 3).value
    clicks = float(ws.cell(r, 4).value or 0)
    impr = float(ws.cell(r, 5).value or 0)
    ctr = float(ws.cell(r, 6).value or 0)
    cpc = float(ws.cell(r, 8).value or 0)
    cost = float(ws.cell(r, 9).value or 0)
    conv_rate = float(ws.cell(r, 10).value or 0)
    conv = float(ws.cell(r, 11).value or 0)
    cpa = float(ws.cell(r, 12).value or 0)
    data.append({
        'term': str(st).strip(),
        'match_type': match_type,
        'added': added,
        'clicks': clicks,
        'impr': impr,
        'ctr': ctr,
        'cpc': cpc,
        'cost': cost,
        'conv_rate': conv_rate,
        'conv': conv,
        'cpa': cpa
    })

df = pd.DataFrame(data)
print(f"Total search term rows: {len(df)}")
print(f"Reported Summary Rows: {summary_rows}")
print(f"Search Terms Sum Clicks: {df['clicks'].sum()}")
print(f"Search Terms Sum Impressions: {df['impr'].sum()}")
print(f"Search Terms Sum Cost: £{df['cost'].sum():.2f}")
print(f"Search Terms Sum Conversions: {df['conv'].sum()}")

# Clicked terms
clicked = df[df['clicks'] > 0].sort_values(by='cost', ascending=False)
print(f"\nSearch terms that got CLICKS (>0): {len(clicked)}")
print(clicked[['term', 'clicks', 'impr', 'cpc', 'cost', 'conv']].to_string())

# Zero-click terms summary
zero_clicks = df[df['clicks'] == 0].sort_values(by='impr', ascending=False)
print(f"\nZero click terms: {len(zero_clicks)}, Total Impressions: {zero_clicks['impr'].sum()}")
print("Top 20 Zero-click terms by impressions:")
print(zero_clicks[['term', 'impr']].head(20).to_string())
