import openpyxl

file1 = r"C:\Users\test\Videos\Personal\data\Paid Media World\https___paidmediaworld.com_-Performance-on-Search-2026-10-13.xlsx"
file2 = r"C:\Users\test\Videos\Personal\data\Paid Media World\https___paidmediaworld.com_-Performance-on-Search-2026-10-13 (1).xlsx"

for path in [file1, file2]:
    print(f"\n=================== {path} ===================")
    try:
        wb = openpyxl.load_workbook(path, data_only=True)
        print("Sheet names:", wb.sheetnames)
        for sname in wb.sheetnames:
            sheet = wb[sname]
            print(f"--- Sheet: {sname} (Rows: {sheet.max_row}, Cols: {sheet.max_column}) ---")
            for r in list(sheet.iter_rows(values_only=True))[:5]:
                print("  ", r)
    except Exception as e:
        print("Error reading excel:", e)
