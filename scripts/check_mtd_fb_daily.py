import pandas as pd

excel_path = r'data/IAOL/October/MTD_Campaign.xlsx'
xl = pd.ExcelFile(excel_path)
print("Looking for French Bangalore sheets or rows in MTD_Campaign:")
for s in ['OCT26_CAMPAIGN', 'OCT26_SUMMARY']:
    if s in xl.sheet_names:
        df = pd.read_excel(excel_path, sheet_name=s)
        print(f"\n--- Sheet: {s} ---")
        # find French Bangalore
        for idx, row in df.iterrows():
            txt = str(row.values)
            if 'french' in txt.lower() and 'bangalore' in txt.lower():
                print(f"Row {idx}: {row.iloc[:8].to_dict()}")
