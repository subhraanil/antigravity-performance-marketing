import openpyxl, os
import pandas as pd

folder = r"C:\Users\test\Videos\Office\data\fabb6\November"
wb = openpyxl.load_workbook(os.path.join(folder, "Channel distribution report.xlsx"), data_only=True)
sheet = wb.active
headers = [sheet.cell(3, c).value for c in range(1, sheet.max_column+1)]

rows = []
for r in range(4, sheet.max_row+1):
    vals = [sheet.cell(r, c).value for c in range(1, sheet.max_column+1)]
    if any(vals):
        rows.append(vals)

df = pd.DataFrame(rows, columns=headers)
for c in ['Cost', 'Conversions', 'Conv. value', 'Clicks', 'Impr.']:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

ch_summary = df.groupby('Channels').agg({
    'Cost': 'sum',
    'Conversions': 'sum',
    'Conv. value': 'sum',
    'Clicks': 'sum',
    'Impr.': 'sum'
}).reset_index()

ch_summary['CPA'] = ch_summary['Cost'] / ch_summary['Conversions'].replace(0, None)
ch_summary['ROAS'] = ch_summary['Conv. value'] / ch_summary['Cost'].replace(0, None)
ch_summary = ch_summary.sort_values(by='Cost', ascending=False)

print("=== GOOGLE CHANNEL DISTRIBUTION BREAKDOWN ===")
for idx, r in ch_summary.iterrows():
    cpa_str = f"Rs {r['CPA']:.2f}" if pd.notnull(r['CPA']) else "N/A"
    roas_str = f"{r['ROAS']:.2f}x" if pd.notnull(r['ROAS']) else "N/A"
    print(f"{r['Channels']}: Cost Rs {r['Cost']:,.2f} | Conv: {r['Conversions']:,.1f} | Value: Rs {r['Conv. value']:,.2f} | CPA: {cpa_str} | ROAS: {roas_str}")
