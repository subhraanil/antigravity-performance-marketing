import os
import glob
import csv
from collections import defaultdict
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

base_dir = r'C:\Users\test\Videos\Office\data\fabb6\Shopify Order'
csv_files = glob.glob(os.path.join(base_dir, '**', '*.csv'), recursive=True)

orders = {}

for fpath in sorted(csv_files):
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('Name')
            if not name:
                continue
            cat = row.get('Created at', '')
            q = float(row['Lineitem quantity']) if row.get('Lineitem quantity') else 0.0
            p = float(row['Lineitem price']) if row.get('Lineitem price') else 0.0
            line_val = q * p
            
            if name not in orders:
                orders[name] = {
                    'created_at': cat,
                    'line_gross': line_val,
                    'subtotal': float(row['Subtotal']) if row.get('Subtotal') else 0.0,
                    'discount': float(row['Discount Amount']) if row.get('Discount Amount') else 0.0,
                    'total': float(row['Total']) if row.get('Total') else 0.0,
                    'taxes': float(row['Taxes']) if row.get('Taxes') else 0.0,
                    'shipping': float(row['Shipping']) if row.get('Shipping') else 0.0,
                    'cancelled': bool(row.get('Cancelled at', '').strip()),
                    'financial_status': row.get('Financial Status', '').strip()
                }
            else:
                orders[name]['line_gross'] += line_val

# Group by month
months = defaultdict(lambda: {
    'all_orders': 0,
    'all_gross': 0.0,
    'all_subtotal': 0.0,
    'all_discount': 0.0,
    'all_total': 0.0,
    'non_canc_orders': 0,
    'non_canc_gross': 0.0,
    'non_canc_subtotal': 0.0,
    'cancelled_orders': 0
})

for name, o in orders.items():
    cat = o['created_at']
    mkey = cat[:7] if cat else 'Unknown'
    m = months[mkey]
    
    m['all_orders'] += 1
    m['all_gross'] += o['line_gross']
    m['all_subtotal'] += o['subtotal']
    m['all_discount'] += o['discount']
    m['all_total'] += o['total']
    
    if not o['cancelled']:
        m['non_canc_orders'] += 1
        m['non_canc_gross'] += o['line_gross']
        m['non_canc_subtotal'] += o['subtotal']
    else:
        m['cancelled_orders'] += 1

# Create workbook
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Monthly Shopify Gross Sales"

# Styles
navy_fill = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
bold_font = Font(name="Calibri", size=10, bold=True)
regular_font = Font(name="Calibri", size=10)
thin_side = Side(border_style="thin", color="D9D9D9")
thin_border = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)

headers = [
    "Month",
    "No of Orders (Total Placed)",
    "Gross Sales Value (₹)",
    "Gross Sales (₹ Lakhs)",
    "AOV on Gross Sales (₹)",
    "Non-Cancelled Orders",
    "Non-Cancelled Gross Sales (₹)",
    "Non-Cancelled AOV (₹)",
    "Discounts Total (₹)",
    "Cancelled Orders Count",
    "Cancellation Rate (%)"
]

ws.append(headers)
for col_num in range(1, len(headers) + 1):
    cell = ws.cell(row=1, column=col_num)
    cell.fill = navy_fill
    cell.font = header_font
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

row_idx = 2
for mk in sorted(months.keys()):
    if mk == 'Unknown':
        continue
    m = months[mk]
    all_ord = m['all_orders']
    all_g = m['all_gross']
    all_aov = all_g / all_ord if all_ord else 0.0
    
    nc_ord = m['non_canc_orders']
    nc_g = m['non_canc_gross']
    nc_aov = nc_g / nc_ord if nc_ord else 0.0
    
    canc_rate = (m['cancelled_orders'] / all_ord * 100) if all_ord else 0.0
    
    row_data = [
        mk,
        all_ord,
        round(all_g, 2),
        round(all_g / 100000.0, 2),
        round(all_aov, 2),
        nc_ord,
        round(nc_g, 2),
        round(nc_aov, 2),
        round(m['all_discount'], 2),
        m['cancelled_orders'],
        round(canc_rate, 2)
    ]
    ws.append(row_data)
    
    # Format cells
    for col_num in range(1, len(row_data) + 1):
        c = ws.cell(row=row_idx, column=col_num)
        c.font = regular_font
        c.border = thin_border
        if col_num in [2, 6, 10]:
            c.number_format = "#,##0"
            c.alignment = Alignment(horizontal="right")
        elif col_num in [3, 5, 7, 8, 9]:
            c.number_format = "₹#,##0.00"
            c.alignment = Alignment(horizontal="right")
        elif col_num == 4:
            c.number_format = "₹#,##0.00\"L\""
            c.alignment = Alignment(horizontal="right")
        elif col_num == 11:
            c.number_format = "0.00\"%\""
            c.alignment = Alignment(horizontal="right")
        else:
            c.alignment = Alignment(horizontal="center")
    row_idx += 1

# Auto-adjust column widths
for col in ws.columns:
    max_len = max(len(str(cell.value or '')) for cell in col)
    col_letter = get_column_letter(col[0].column)
    ws.column_dimensions[col_letter].width = max(max_len + 4, 14)

excel_path = r'C:\Users\test\Videos\Office\data\fabb6\FABB6_Shopify_Monthly_Gross_Sales_Master.xlsx'
wb.save(excel_path)
print(f"Master Excel saved to: {excel_path}")

# Also save CSV
csv_path = r'C:\Users\test\Videos\Office\data\fabb6\FABB6_Shopify_Monthly_Gross_Sales_Master.csv'
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    for r in range(2, row_idx):
        writer.writerow([ws.cell(row=r, column=c).value for c in range(1, len(headers) + 1)])
print(f"Master CSV saved to: {csv_path}")
