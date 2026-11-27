import csv
import re
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

input_file = "data/Pet Mode/orders_export.csv"
output_csv = "data/Pet Mode/Google Ads/Pet_Mode_Customer_Match_Google_Ads.csv"
mirror_csv = "reports/Pet_Mode_Customer_Match_Google_Ads.csv"
output_xlsx = "data/Pet Mode/Google Ads/Pet_Mode_Customer_Match_Google_Ads.xlsx"
mirror_xlsx = "reports/Pet_Mode_Customer_Match_Google_Ads.xlsx"

customers = {}
raw_orders = []

with open(input_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        raw_orders.append(row)

for row in raw_orders:
    email = (row["Email"] or "").strip().lower()
    if not email or "@" not in email:
        continue
    
    # Phone formatting (E.164 standard)
    raw_phone = row["Phone"] or row["Shipping Phone"] or row["Billing Phone"] or ""
    clean_digits = re.sub(r"[^0-9]", "", raw_phone)
    formatted_phone = ""
    if clean_digits:
        if clean_digits.startswith("44") and len(clean_digits) >= 11:
            formatted_phone = "+" + clean_digits
        elif clean_digits.startswith("0") and len(clean_digits) == 11:
            formatted_phone = "+44" + clean_digits[1:]
        elif len(clean_digits) == 10 and clean_digits.startswith("7"):
            formatted_phone = "+44" + clean_digits
        elif len(clean_digits) == 10 and clean_digits.startswith("1"): # UK landline
            formatted_phone = "+44" + clean_digits
        else:
            formatted_phone = "+" + clean_digits if not raw_phone.startswith("+") else raw_phone
            
    # Name extraction
    name = (row["Shipping Name"] or row["Billing Name"] or "").strip()
    first_name = ""
    last_name = ""
    if name:
        parts = name.split()
        first_name = parts[0].capitalize()
        if len(parts) > 1:
            last_name = " ".join(parts[1:]).capitalize()
            
    # Country & Zip
    country = (row["Shipping Country"] or row["Billing Country"] or "GB").strip().upper()
    if len(country) > 2:
        if "UNITED KINGDOM" in country: country = "GB"
        elif "UNITED STATES" in country: country = "US"
        else: country = country[:2]
        
    zip_code = (row["Shipping Zip"] or row["Billing Zip"] or "").strip().upper()
    
    if email not in customers:
        customers[email] = {
            "Email": email,
            "Phone": formatted_phone,
            "First Name": first_name,
            "Last Name": last_name,
            "Country": country,
            "Zip": zip_code,
            "Total Spend": 0.0,
            "Order Count": 0
        }
    else:
        if not customers[email]["Phone"] and formatted_phone:
            customers[email]["Phone"] = formatted_phone
        if not customers[email]["Zip"] and zip_code:
            customers[email]["Zip"] = zip_code
            
    customers[email]["Order Count"] += 1
    try:
        customers[email]["Total Spend"] += float(row["Total"] or 0)
    except:
        pass

# 1. Write official Google Ads CSV (Strict Google Format)
google_headers = ["Email", "Phone", "First Name", "Last Name", "Country", "Zip"]
with open(output_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(google_headers)
    for c in customers.values():
        writer.writerow([
            c["Email"],
            c["Phone"],
            c["First Name"],
            c["Last Name"],
            c["Country"],
            c["Zip"]
        ])

import shutil
shutil.copyfile(output_csv, mirror_csv)
print(f"Saved Google Ads Customer Match CSV: {output_csv} ({len(customers)} records)")
print(f"Mirrored to: {mirror_csv}")

# 2. Write Excel workbook for user review (including Spend and Order count)
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Customer Match Data"
ws.views.sheetView[0].showGridLines = True

hdr_font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
hdr_fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
zebra_fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
white_fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
thin_side = Side(border_style="thin", color="CBD5E1")
cell_border = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)

excel_headers = ["Email", "Phone (E.164)", "First Name", "Last Name", "Country", "Postcode (Zip)", "Orders", "Total Spend (£)"]
for col_idx, h in enumerate(excel_headers, start=1):
    cell = ws.cell(row=1, column=col_idx, value=h)
    cell.font = hdr_font
    cell.fill = hdr_fill
    cell.alignment = Alignment(horizontal="center", vertical="center")
    cell.border = cell_border
ws.row_dimensions[1].height = 25

sorted_customers = sorted(customers.values(), key=lambda x: x["Total Spend"], reverse=True)
for row_idx, c in enumerate(sorted_customers, start=2):
    fill_to_use = zebra_fill if (row_idx % 2 == 1) else white_fill
    row_vals = [
        c["Email"],
        c["Phone"],
        c["First Name"],
        c["Last Name"],
        c["Country"],
        c["Zip"],
        c["Order Count"],
        c["Total Spend"]
    ]
    for col_idx, val in enumerate(row_vals, start=1):
        cell = ws.cell(row=row_idx, column=col_idx, value=val)
        cell.fill = fill_to_use
        cell.border = cell_border
        cell.font = Font(name="Calibri", size=9.5)
        if col_idx in [1, 3, 4]:
            cell.alignment = Alignment(horizontal="left", vertical="center")
        elif col_idx in [2, 5, 6, 7]:
            cell.alignment = Alignment(horizontal="center", vertical="center")
        elif col_idx == 8:
            cell.alignment = Alignment(horizontal="right", vertical="center")
            cell.number_format = "[$£-809]#,##0.00"
    ws.row_dimensions[row_idx].height = 20

col_widths = {1: 32, 2: 18, 3: 16, 4: 18, 5: 12, 6: 16, 7: 12, 8: 16}
for col, w in col_widths.items():
    ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = w

wb.save(output_xlsx)
shutil.copyfile(output_xlsx, mirror_xlsx)
print(f"Saved Customer Match Excel: {output_xlsx}")
