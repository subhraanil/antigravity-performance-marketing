import pandas as pd
import os

oct_folder = r'C:\Users\test\Videos\Office\data\IAOL\October'
f_mtd = os.path.join(oct_folder, 'MTD_Campaign.xlsx')
f_roi = os.path.join(oct_folder, 'Conversion_ROI (1).xlsx')

print("=" * 80)
print("DUMPING OCT26_SUMMARY from MTD_Campaign.xlsx")
print("=" * 80)
df_oct_summary = pd.read_excel(f_mtd, sheet_name='OCT26_SUMMARY')
# Clean and print all rows
print(df_oct_summary.dropna(subset=['Till 31st Oct']).to_string(index=False))

print("\n" + "=" * 80)
print("DUMPING CONVERSION & ROI from Conversion_ROI (1).xlsx")
print("=" * 80)
df_conv = pd.read_excel(f_roi, sheet_name='CONVERSION')
print("\nCONVERSION TAB (First 15 rows):")
print(df_conv.iloc[:15, :12].to_string())

df_roi = pd.read_excel(f_roi, sheet_name='ROI')
print("\nROI TAB (First 15 rows):")
print(df_roi.iloc[:15, :12].to_string())

df_s3 = pd.read_excel(f_roi, sheet_name='Sheet3')
print("\nSheet3 TAB (Full):")
print(df_s3.to_string())
