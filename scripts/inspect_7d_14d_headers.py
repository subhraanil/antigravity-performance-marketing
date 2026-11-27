import pandas as pd

f7 = r'c:\Users\test\Videos\Office\data\IAOL\Search terms report - last 7 days.xlsx'
f14 = r'c:\Users\test\Videos\Office\data\IAOL\Search terms report - last 14 days.xlsx'

print("=== LAST 7 DAYS REPORT ===")
df7_raw = pd.read_excel(f7, header=None)
print("Row 0:", df7_raw.iloc[0, 0])
print("Row 1 (Date range):", df7_raw.iloc[1, 0])
print("Row 2 (Columns):", df7_raw.iloc[2, :].dropna().tolist())

print("\n=== LAST 14 DAYS REPORT ===")
df14_raw = pd.read_excel(f14, header=None)
print("Row 0:", df14_raw.iloc[0, 0])
print("Row 1 (Date range):", df14_raw.iloc[1, 0])
print("Row 2 (Columns):", df14_raw.iloc[2, :].dropna().tolist())
