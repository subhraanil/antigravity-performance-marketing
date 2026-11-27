import pandas as pd
import os

oct_folder = r'C:\Users\test\Videos\Office\data\IAOL\October'
f_roi = os.path.join(oct_folder, 'Conversion_ROI (1).xlsx')
f_mtd = os.path.join(oct_folder, 'MTD_Campaign.xlsx')

print("=" * 80)
print("1. Conversion_ROI (1).xlsx")
print("=" * 80)
for s in ['CONVERSION', 'ROI', 'Sheet3']:
    try:
        df = pd.read_excel(f_roi, sheet_name=s)
        print(f"\n--- SHEET: {s} --- (Shape: {df.shape})")
        print("Columns:", df.columns.tolist()[:15])
        print(df.head(5))
    except Exception as e:
        print(f"Error reading {s}:", e)

print("\n" + "=" * 80)
print("2. MTD_Campaign.xlsx (October & September 2026)")
print("=" * 80)
for s in ['OCT26_SUMMARY', 'OCT26_CAMPAIGN', 'SEP26_SUMMARY', 'SEP26_CAMPAIGN']:
    try:
        df = pd.read_excel(f_mtd, sheet_name=s)
        print(f"\n--- SHEET: {s} --- (Shape: {df.shape})")
        print("Columns:", df.columns.tolist()[:15])
        print(df.head(5))
    except Exception as e:
        print(f"Error reading {s}:", e)
