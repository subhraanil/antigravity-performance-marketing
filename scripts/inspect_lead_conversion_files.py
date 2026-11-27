import openpyxl
import pandas as pd
import os

oct_folder = r'C:\Users\test\Videos\Office\data\IAOL\October'
f_roi = os.path.join(oct_folder, 'Conversion_ROI (1).xlsx')
f_mtd = os.path.join(oct_folder, 'MTD_Campaign.xlsx')

print("=== 1. Conversion_ROI (1).xlsx ===")
wb_roi = openpyxl.load_workbook(f_roi, read_only=True)
print("Sheet names:", wb_roi.sheetnames)
for s in wb_roi.sheetnames:
    df_s = pd.read_excel(f_roi, sheet_name=s)
    print(f"\nSheet '{s}': Shape {df_s.shape}")
    print("Columns:", df_s.columns.tolist()[:15])
    print(df_s.head(3))

print("\n=== 2. MTD_Campaign.xlsx ===")
wb_mtd = openpyxl.load_workbook(f_mtd, read_only=True)
print("Sheet names:", wb_mtd.sheetnames)
for s in wb_mtd.sheetnames:
    df_s = pd.read_excel(f_mtd, sheet_name=s)
    print(f"\nSheet '{s}': Shape {df_s.shape}")
    print("Columns:", df_s.columns.tolist()[:15])
    print(df_s.head(3))
