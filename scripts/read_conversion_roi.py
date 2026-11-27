import pandas as pd

f_roi = r'C:\Users\test\Videos\Office\data\IAOL\October\Conversion_ROI (1).xlsx'

print("=== CONVERSION TAB ===")
df_conv = pd.read_excel(f_roi, sheet_name='CONVERSION')
print("Shape:", df_conv.shape)
print("Columns:", df_conv.columns.tolist()[:25])
print(df_conv.head(5))

print("\n=== ROI TAB ===")
df_roi = pd.read_excel(f_roi, sheet_name='ROI')
print("Shape:", df_roi.shape)
print("Columns:", df_roi.columns.tolist()[:25])
print(df_roi.head(10))

print("\n=== Sheet3 TAB ===")
df_s3 = pd.read_excel(f_roi, sheet_name='Sheet3')
print("Shape:", df_s3.shape)
print("Columns:", df_s3.columns.tolist())
print(df_s3.head(10))
