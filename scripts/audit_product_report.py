import openpyxl, os
import pandas as pd

folder = r"C:\Users\test\Videos\Office\data\fabb6\November"
wb = openpyxl.load_workbook(os.path.join(folder, "Product report (7).xlsx"), data_only=True)
sheet = wb.active
headers = [sheet.cell(3, c).value for c in range(1, sheet.max_column+1)]

rows = []
for r in range(4, sheet.max_row+1):
    vals = [sheet.cell(r, c).value for c in range(1, sheet.max_column+1)]
    if any(vals):
        rows.append(vals)

df = pd.DataFrame(rows, columns=headers)
print("Product report columns:", df.columns.tolist())

for col in ['Cost', 'Conversions', 'Product clicks', 'Impr.']:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# Check issues
print("\nProduct Issues count:")
print(df['Issues'].value_counts().head(10))

print("\nProduct Status count:")
print(df['Status'].value_counts())

# Zero conversions with spend
zero_conv = df[(df['Conversions'] == 0) & (df['Cost'] > 200)].sort_values(by='Cost', ascending=False)
print(f"\nZero conversion products (>Rs 200 cost): {len(zero_conv)}")
print(f"Total spent on zero conversion products: Rs {zero_conv['Cost'].sum():,.2f}")
for idx, r in zero_conv.head(15).iterrows():
    print(f"  - Item: {r['Item ID']} | Title: {str(r['Title'])[:40]} | Cost: Rs {r['Cost']:,.2f} | Clicks: {r['Product clicks']} | Issues: {r['Issues']}")

# Top converting products
top_conv = df[df['Conversions'] > 0].sort_values(by='Conversions', ascending=False)
print(f"\nTop 15 Converting Products:")
for idx, r in top_conv.head(15).iterrows():
    cpa = r['Cost'] / r['Conversions'] if r['Conversions'] > 0 else 0
    print(f"  + Item: {r['Item ID']} | Title: {str(r['Title'])[:40]} | Spend: Rs {r['Cost']:,.2f} | Conv: {r['Conversions']} | CPA: Rs {cpa:.2f}")
