import pandas as pd
excel_path = r'data/IAOL/October/Conversion_ROI (1).xlsx'
wb = pd.ExcelFile(excel_path)
for sheet in wb.sheet_names:
    print(f'=== Sheet: {sheet} ===')
    df = pd.read_excel(excel_path, sheet_name=sheet)
    # print non-null summary
    print(df.iloc[:12, :10])
