import openpyxl
import os
import glob

oct_folder = r'C:\Users\test\Videos\Office\data\IAOL\October'
files = glob.glob(os.path.join(oct_folder, '*.xlsx'))

for f in files:
    print(f"\n=======================================================")
    print(f"FILE: {os.path.basename(f)}")
    print(f"=======================================================")
    try:
        wb = openpyxl.load_workbook(f)
        print("Sheet names:", wb.sheetnames)
        for s in wb.sheetnames:
            ws = wb[s]
            print(f"  Tab '{s}': state={ws.sheet_state}, max_row={ws.max_row}, max_column={ws.max_column}")
    except Exception as e:
        print("Error reading with openpyxl:", e)
