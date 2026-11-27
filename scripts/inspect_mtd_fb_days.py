import pandas as pd

excel_path = r'data/IAOL/October/MTD_Campaign.xlsx'
df = pd.read_excel(excel_path, sheet_name='OCT26_CAMPAIGN')

print("Columns in OCT26_CAMPAIGN:", df.columns.tolist()[:10])
print("\nRow 0 (dates?):", df.iloc[0].values[:10])
# Let's inspect rows 40-45
for r_idx in range(39, 45):
    row = df.iloc[r_idx]
    label = row.iloc[0]
    metric = row.iloc[1]
    # print dates and values for late October (columns from 20 onwards)
    print(f"\nRow {r_idx}: {label} | {metric}")
    for col_idx in range(len(df.columns)):
        val = row.iloc[col_idx]
        col_name = df.iloc[0, col_idx]
        if pd.notnull(val) and col_idx > 1:
            print(f"  Col {col_idx} ({col_name}): {val}")
