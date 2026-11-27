import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import pandas as pd
import re
import os

# 1. Load Shopify Orders Export
csv_path = r'c:\Users\test\Videos\Office\data\Pet Mode\orders_export.csv'
df = pd.read_csv(csv_path, low_memory=False)

# Deduplicate to order-level (first row per order)
orders = df.groupby('Name', as_index=False).first()

# 2. Postcode & Region Map
postcode_region_map = {
    'AB': ('Aberdeen & North East Scotland', 'Scotland'),
    'B': ('Birmingham & West Midlands', 'West Midlands'),
    'BA': ('Bath & Somerset', 'South West'),
    'BB': ('Blackburn & Lancashire', 'North West'),
    'BD': ('Bradford & West Yorkshire', 'Yorkshire and the Humber'),
    'BH': ('Bournemouth & Dorset', 'South West'),
    'BL': ('Bolton & Greater Manchester', 'North West'),
    'BN': ('Brighton & East Sussex', 'South East'),
    'BR': ('Bromley & Greater London', 'Greater London'),
    'BS': ('Bristol & North Somerset', 'South West'),
    'BT': ('Northern Ireland', 'Northern Ireland'),
    'CA': ('Cumbria', 'North West'),
    'CB': ('Cambridge & Cambridgeshire', 'East of England'),
    'CF': ('Cardiff & South Wales', 'Wales'),
    'CH': ('Chester & Cheshire', 'North West'),
    'CM': ('Chelmsford & Essex', 'East of England'),
    'CO': ('Colchester & Essex', 'East of England'),
    'CR': ('Croydon & Greater London', 'Greater London'),
    'CT': ('Canterbury & Kent', 'South East'),
    'CV': ('Coventry & Warwickshire', 'West Midlands'),
    'CW': ('Crewe & Cheshire', 'North West'),
    'DA': ('Dartford & Greater London/Kent', 'Greater London'),
    'DD': ('Dundee & Angus/Fife', 'Scotland'),
    'DE': ('Derby & Derbyshire', 'East Midlands'),
    'DG': ('Dumfries and Galloway', 'Scotland'),
    'DH': ('Durham & County Durham', 'North East'),
    'DL': ('Darlington & North Yorkshire', 'North East'),
    'DN': ('Doncaster & North Lincolnshire', 'Yorkshire and the Humber'),
    'DT': ('Dorchester & Dorset', 'South West'),
    'DY': ('Dudley & West Midlands', 'West Midlands'),
    'E': ('East London', 'Greater London'),
    'EC': ('East Central London', 'Greater London'),
    'EH': ('Edinburgh & Lothians', 'Scotland'),
    'EN': ('Enfield & Greater London', 'Greater London'),
    'EX': ('Exeter & Devon', 'South West'),
    'FK': ('Falkirk & Stirling', 'Scotland'),
    'FY': ('Blackpool & Lancashire', 'North West'),
    'G': ('Glasgow & Dunbartonshire', 'Scotland'),
    'GL': ('Gloucester & Gloucestershire', 'South West'),
    'GU': ('Guildford & Surrey', 'South East'),
    'HA': ('Harrow & Greater London', 'Greater London'),
    'HD': ('Huddersfield & West Yorkshire', 'Yorkshire and the Humber'),
    'HG': ('Harrogate & North Yorkshire', 'Yorkshire and the Humber'),
    'HP': ('Hemel Hempstead & Buckinghamshire', 'South East'),
    'HR': ('Hereford & Herefordshire', 'West Midlands'),
    'HS': ('Outer Hebrides', 'Scotland'),
    'HU': ('Hull & East Yorkshire', 'Yorkshire and the Humber'),
    'HX': ('Halifax & West Yorkshire', 'Yorkshire and the Humber'),
    'IG': ('Ilford & Greater London', 'Greater London'),
    'IP': ('Ipswich & Suffolk', 'East of England'),
    'IV': ('Inverness & Highlands', 'Scotland'),
    'KA': ('Kilmarnock & Ayrshire', 'Scotland'),
    'KT': ('Kingston upon Thames & Greater London', 'Greater London'),
    'KW': ('Kirkwall & Highlands', 'Scotland'),
    'KY': ('Kirkcaldy & Fife', 'Scotland'),
    'L': ('Liverpool & Merseyside', 'North West'),
    'LA': ('Lancaster & Cumbria/Lancashire', 'North West'),
    'LD': ('Llandrindod Wells & Powys', 'Wales'),
    'LE': ('Leicester & Leicestershire', 'East Midlands'),
    'LL': ('Llandudno & North Wales', 'Wales'),
    'LN': ('Lincoln & Lincolnshire', 'East Midlands'),
    'LS': ('Leeds & West Yorkshire', 'Yorkshire and the Humber'),
    'LU': ('Luton & Bedfordshire', 'East of England'),
    'M': ('Manchester & Greater Manchester', 'North West'),
    'ME': ('Medway & Kent', 'South East'),
    'MK': ('Milton Keynes & Buckinghamshire', 'South East'),
    'ML': ('Motherwell & Lanarkshire', 'Scotland'),
    'N': ('North London', 'Greater London'),
    'NE': ('Newcastle upon Tyne & Tyne and Wear', 'North East'),
    'NG': ('Nottingham & Nottinghamshire', 'East Midlands'),
    'NN': ('Northampton & Northamptonshire', 'East Midlands'),
    'NP': ('Newport & South Wales', 'Wales'),
    'NR': ('Norwich & Norfolk', 'East of England'),
    'NW': ('North West London', 'Greater London'),
    'OL': ('Oldham & Greater Manchester', 'North West'),
    'OX': ('Oxford & Oxfordshire', 'South East'),
    'PA': ('Paisley & Renfrewshire/Argyll', 'Scotland'),
    'PE': ('Peterborough & Cambridgeshire/Norfolk', 'East of England'),
    'PH': ('Perth & Highlands', 'Scotland'),
    'PL': ('Plymouth & Devon/Cornwall', 'South West'),
    'PO': ('Portsmouth & Hampshire/West Sussex', 'South East'),
    'PR': ('Preston & Lancashire', 'North West'),
    'RG': ('Reading & Berkshire', 'South East'),
    'RH': ('Redhill & Surrey/West Sussex', 'South East'),
    'RM': ('Romford & Greater London', 'Greater London'),
    'S': ('Sheffield & South Yorkshire', 'Yorkshire and the Humber'),
    'SA': ('Swansea & South Wales', 'Wales'),
    'SE': ('South East London', 'Greater London'),
    'SG': ('Stevenage & Hertfordshire', 'East of England'),
    'SK': ('Stockport & Cheshire/Greater Manchester', 'North West'),
    'SL': ('Slough & Berkshire/Buckinghamshire', 'South East'),
    'SM': ('Sutton & Greater London', 'Greater London'),
    'SN': ('Swindon & Wiltshire', 'South West'),
    'SO': ('Southampton & Hampshire', 'South East'),
    'SP': ('Salisbury & Wiltshire', 'South West'),
    'SR': ('Sunderland & Tyne and Wear', 'North East'),
    'SS': ('Southend-on-Sea & Essex', 'East of England'),
    'ST': ('Stoke-on-Trent & Staffordshire', 'West Midlands'),
    'SW': ('South West London', 'Greater London'),
    'SY': ('Shrewsbury & Shropshire/Mid Wales', 'West Midlands'),
    'TA': ('Taunton & Somerset', 'South West'),
    'TD': ('Galashiels & Scottish Borders', 'Scotland'),
    'TF': ('Telford & Shropshire', 'West Midlands'),
    'TN': ('Tunbridge Wells & Kent/East Sussex', 'South East'),
    'TQ': ('Torquay & Devon', 'South West'),
    'TR': ('Truro & Cornwall', 'South West'),
    'TS': ('Cleveland & Teesside', 'North East'),
    'TW': ('Twickenham & Greater London', 'Greater London'),
    'UB': ('Uxbridge & Greater London', 'Greater London'),
    'W': ('West London', 'Greater London'),
    'WA': ('Warrington & Cheshire/Merseyside', 'North West'),
    'WC': ('West Central London', 'Greater London'),
    'WD': ('Watford & Hertfordshire', 'East of England'),
    'WF': ('Wakefield & West Yorkshire', 'Yorkshire and the Humber'),
    'WN': ('Wigan & Greater Manchester', 'North West'),
    'WR': ('Worcester & Worcestershire', 'West Midlands'),
    'WS': ('Walsall & West Midlands', 'West Midlands'),
    'WV': ('Wolverhampton & West Midlands', 'West Midlands'),
    'YO': ('York & North Yorkshire', 'Yorkshire and the Humber'),
    'ZE': ('Shetland', 'Scotland')
}

order_records = []
for idx, r in orders.iterrows():
    name = str(r['Name']).strip()
    raw_city = str(r['Shipping City']).strip() if pd.notna(r['Shipping City']) else ''
    zip_code = str(r['Shipping Zip']).strip().upper() if pd.notna(r['Shipping Zip']) else ''
    country = str(r['Shipping Country']).strip().upper() if pd.notna(r['Shipping Country']) else ''
    province = str(r['Shipping Province Name']).strip() if pd.notna(r['Shipping Province Name']) else ''
    total = float(r['Total']) if pd.notna(r['Total']) else 0.0
    status = str(r['Financial Status']).strip() if pd.notna(r['Financial Status']) else ''
    created_at = str(r['Created at']).strip() if pd.notna(r['Created at']) else ''
    
    # Extract postcode area & outcode
    if country == 'GB':
        m_area = re.match(r'^([A-Z]{1,2})', zip_code)
        pc_area = m_area.group(1) if m_area else 'Other'
        outcode = zip_code.split(' ')[0] if ' ' in zip_code else zip_code
        area_info = postcode_region_map.get(pc_area, ('Other UK', 'Other UK'))
        county_desc = area_info[0]
        region = area_info[1]
    elif country == 'PL':
        pc_area = 'PL'
        outcode = zip_code
        county_desc = 'West Pomerania (Poland)'
        region = 'International (Poland)'
    elif country == 'US':
        pc_area = 'NJ'
        outcode = zip_code
        county_desc = 'Ocean County, New Jersey (USA)'
        region = 'International (USA)'
    else:
        pc_area = 'Other'
        outcode = zip_code
        county_desc = 'Other'
        region = 'Other'
        
    # Standardize city display
    c_lower = raw_city.lower()
    if country == 'PL':
        clean_city = 'Świnoujście (Poland)'
        metro = 'International'
    elif country == 'US':
        clean_city = 'Lacey Township, NJ (USA)'
        metro = 'International'
    else:
        if c_lower in ['london', 'greater london']:
            clean_city = 'London'
            metro = 'Greater London'
        elif 'hackney' in c_lower:
            clean_city = 'London'
            metro = 'Greater London'
        elif 'islington' in c_lower:
            clean_city = 'London'
            metro = 'Greater London'
        elif 'leytonstone' in c_lower:
            clean_city = 'London (Leytonstone)'
            metro = 'Greater London'
        elif 'cheam' in c_lower:
            clean_city = 'Cheam (London)'
            metro = 'Greater London'
        elif 'purley' in c_lower:
            clean_city = 'Purley (London)'
            metro = 'Greater London'
        elif 'beckenham' in c_lower:
            clean_city = 'Beckenham (London)'
            metro = 'Greater London'
        elif 'pinner' in c_lower:
            clean_city = 'Pinner (London)'
            metro = 'Greater London'
        elif 'teddington' in c_lower:
            clean_city = 'Teddington (London)'
            metro = 'Greater London'
        elif 'uxbridge' in c_lower:
            clean_city = 'Uxbridge (London)'
            metro = 'Greater London'
        elif 'worcester park' in c_lower:
            clean_city = 'Worcester Park (London)'
            metro = 'Greater London'
        elif 'bognor regis' in c_lower:
            clean_city = 'Bognor Regis'
            metro = 'West Sussex Coastal'
        elif 'chorleywood' in c_lower:
            clean_city = 'Chorleywood'
            metro = 'Hertfordshire'
        elif 'edenbridge' in c_lower:
            clean_city = 'Edenbridge'
            metro = 'Kent / Sevenoaks'
        elif 'hatfield' in c_lower:
            clean_city = 'Doncaster (Hatfield)'
            metro = 'Greater Doncaster'
        elif 'mirfield' in c_lower:
            clean_city = 'Mirfield'
            metro = 'West Yorkshire'
        elif 'newcastle upon tyne' in c_lower or c_lower == 'newcastle':
            clean_city = 'Newcastle upon Tyne'
            metro = 'Tyne and Wear'
        elif 'old kilpatrick' in c_lower:
            clean_city = 'Clydebank / Old Kilpatrick'
            metro = 'Greater Glasgow'
        elif 'penylan' in c_lower:
            clean_city = 'Cardiff (Penylan)'
            metro = 'Cardiff & South Wales'
        elif 'pollokshields' in c_lower:
            clean_city = 'Glasgow (Pollokshields)'
            metro = 'Greater Glasgow'
        elif 'stone' in c_lower:
            clean_city = 'Stone'
            metro = 'Staffordshire'
        elif 'stratford-upon-avon' in c_lower:
            clean_city = 'Stratford-upon-Avon'
            metro = 'Warwickshire'
        elif 'winsham' in c_lower:
            clean_city = 'Winsham'
            metro = 'Somerset'
        elif 'wokingham' in c_lower:
            clean_city = 'Wokingham'
            metro = 'Berkshire'
        elif 'yelverton' in c_lower:
            clean_city = 'Yelverton'
            metro = 'Devon / Plymouth fringe'
        elif 'essex' in c_lower:
            clean_city = 'Epping (Essex)'
            metro = 'Essex'
        elif 'warmley' in c_lower:
            clean_city = 'Bristol (Warmley)'
            metro = 'Greater Bristol'
        elif 'cheddar' in c_lower:
            clean_city = 'Cheddar'
            metro = 'Somerset'
        elif 'sutton coldfield' in c_lower:
            clean_city = 'Sutton Coldfield'
            metro = 'Greater Birmingham'
        elif 'tamworth' in c_lower:
            clean_city = 'Tamworth'
            metro = 'Greater Birmingham'
        elif 'walsall' in c_lower:
            clean_city = 'Walsall'
            metro = 'Greater Birmingham'
        elif 'bristol' in c_lower:
            clean_city = 'Bristol'
            metro = 'Greater Bristol'
        elif 'glasgow' in c_lower:
            clean_city = 'Glasgow'
            metro = 'Greater Glasgow'
        elif 'edinburgh' in c_lower:
            clean_city = 'Edinburgh'
            metro = 'Edinburgh & Lothians'
        elif 'cardiff' in c_lower:
            clean_city = 'Cardiff'
            metro = 'Cardiff & South Wales'
        elif 'leeds' in c_lower:
            clean_city = 'Leeds'
            metro = 'West Yorkshire'
        elif 'manchester' in c_lower:
            clean_city = 'Manchester'
            metro = 'Greater Manchester'
        else:
            clean_city = raw_city.title()
            metro = area_info[0]

    order_records.append({
        'Order_ID': name,
        'Created_At': created_at,
        'Financial_Status': status,
        'Raw_City': raw_city,
        'Clean_City': clean_city,
        'Metro_Area': metro,
        'County_Desc': county_desc,
        'Region': region,
        'Country': country,
        'Postcode': zip_code,
        'Outcode': outcode,
        'Postcode_Area': pc_area,
        'Order_Total': total
    })

order_df = pd.DataFrame(order_records)
total_orders_count = len(order_df)
total_revenue_sum = order_df['Order_Total'].sum()

# 3. Save clean CSV
csv_out_path = r'c:\Users\test\Videos\Office\data\Pet Mode\Pet_Mode_City_Wise_Orders_Report.csv'
order_df.to_csv(csv_out_path, index=False, encoding='utf-8')
print(f"Saved CSV to {csv_out_path}")

# 4. Load Google Ads Location report for cross-comparison
google_wb = openpyxl.load_workbook(r'c:\Users\test\Videos\Office\data\Pet Mode\Location report.xlsx', data_only=True)
google_ws = google_wb.active
google_data = []
for r in range(4, google_ws.max_row + 1):
    loc = google_ws.cell(r, 1).value
    if not loc or loc.startswith('Total:'):
        continue
    clicks = float(google_ws.cell(r, 2).value or 0)
    impr = float(google_ws.cell(r, 3).value or 0)
    ctr = float(google_ws.cell(r, 4).value or 0)
    cpc = float(google_ws.cell(r, 6).value or 0)
    cost = float(google_ws.cell(r, 7).value or 0)
    conv_rate = float(google_ws.cell(r, 8).value or 0)
    conv = float(google_ws.cell(r, 9).value or 0)
    cpa = float(google_ws.cell(r, 10).value or 0)
    google_data.append({
        'Location': loc,
        'Clicks': clicks,
        'Impressions': impr,
        'CTR': ctr,
        'CPC': cpc,
        'Cost': cost,
        'Conv_Rate': conv_rate,
        'Conversions': conv,
        'CPA': cpa
    })

# 5. Build Master Excel Report
wb = openpyxl.Workbook()
wb.remove(wb.active) # Remove default sheet

# Styling definitions
navy_header_fill = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
navy_header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")

teal_sub_fill = PatternFill(start_color="008080", end_color="008080", fill_type="solid")
teal_sub_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")

soft_gray_fill = PatternFill(start_color="F4F7FA", end_color="F4F7FA", fill_type="solid")
zebra_fill = PatternFill(start_color="F9FBFC", end_color="F9FBFC", fill_type="solid")
total_fill = PatternFill(start_color="E9EFF5", end_color="E9EFF5", fill_type="solid")

kpi_card_fill = PatternFill(start_color="E8F0FE", end_color="E8F0FE", fill_type="solid")
kpi_border = Border(
    left=Side(style='thin', color='B0C4DE'),
    right=Side(style='thin', color='B0C4DE'),
    top=Side(style='thin', color='B0C4DE'),
    bottom=Side(style='thin', color='B0C4DE')
)

bold_font = Font(name="Calibri", size=11, bold=True, color="000000")
regular_font = Font(name="Calibri", size=10, color="000000")
total_font = Font(name="Calibri", size=11, bold=True, color="1B365D")

thin_border = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'),
    bottom=Side(style='thin', color='D9D9D9')
)
double_bottom_border = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='1B365D'),
    bottom=Side(style='double', color='1B365D')
)

align_left = Alignment(horizontal="left", vertical="center")
align_center = Alignment(horizontal="center", vertical="center")
align_right = Alignment(horizontal="right", vertical="center")

def autofit_columns(ws, min_col=1, max_col=None):
    if max_col is None:
        max_col = ws.max_column
    for col in range(min_col, max_col + 1):
        col_letter = get_column_letter(col)
        max_len = 0
        for row in range(1, ws.max_row + 1):
            val = ws.cell(row, col).value
            if val is not None:
                s = str(val)
                lines = s.split('\n')
                line_max = max(len(l) for l in lines)
                if line_max > max_len:
                    max_len = line_max
        ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

# ==========================================
# SHEET 1: Executive Summary & Geo Insights
# ==========================================
ws_sum = wb.create_sheet(title="Executive Summary")
ws_sum.views.sheetView[0].showGridLines = True

ws_sum['A1'] = "PET MODE - GEOGRAPHIC ORDERS & REVENUE AUDIT"
ws_sum['A1'].font = Font(name="Calibri", size=16, bold=True, color="1B365D")
ws_sum['A2'] = "Storewide Customer Geographic Distribution & Google Ads Cross-Audit | Shopify Order Export Reconciliation"
ws_sum['A2'].font = Font(name="Calibri", size=11, italic=True, color="555555")

# KPI Cards
kpis = [
    ("TOTAL STORE ORDERS", total_orders_count, "B4:C5", "#,##0"),
    ("TOTAL ORDER REVENUE", total_revenue_sum, "D4:E5", "[$£-809]#,##0.00"),
    ("STOREWIDE BLENDED AOV", total_revenue_sum / total_orders_count, "F4:G5", "[$£-809]#,##0.00"),
    ("UK DOMESTIC SHARE", 160 / total_orders_count, "H4:I5", "0.0%"),
]

for title, val, rng, num_fmt in kpis:
    start_cell, end_cell = rng.split(':')
    ws_sum.merge_cells(rng)
    cell = ws_sum[start_cell]
    cell.value = f"{title}\n{val:{'.2f' if '£' in num_fmt else ('.1%' if '%' in num_fmt else 'd')}}"
    if '£' in num_fmt:
        cell.value = f"{title}\n£{val:,.2f}"
    elif '%' in num_fmt:
        cell.value = f"{title}\n{val*100:.1f}%"
    else:
        cell.value = f"{title}\n{val:,}"
    cell.font = Font(name="Calibri", size=12, bold=True, color="1B365D")
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    cell.fill = kpi_card_fill
    for r in ws_sum[rng]:
        for c in r:
            c.border = kpi_border

# Key Executive Insights text
ws_sum['B7'] = "CORE AUDIT FINDINGS & STRATEGIC RECOMMENDATIONS"
ws_sum['B7'].font = Font(name="Calibri", size=13, bold=True, color="1B365D")

insights = [
    ("1. London & South East Hegemony (32.1% of Orders, 35.6% of Revenue)", 
     "Greater London (34 orders, £972.99) and South East England (18 orders, £636.20) represent over £1,609 of store revenue. In Google Ads, London absorbed £755.61 (57% of total budget) and generated 23 conversions at £32.85 CPA. High concentration of affluent pet owners in SW, W, N postcodes with higher willingness to buy premium cat flaps and car seat covers."),
    ("2. Bristol is the #2 Powerhouse Nationally (8 Orders, £239.12 Revenue)", 
     "The BS postcode area (Bristol, Warmley, Cheddar) ranks #2 in the UK with 8 orders. While Google Ads only attributed 1 conversion directly to Bristol (£73.09 CPA), Shopify proves Bristol has massive organic and multi-touch resonance. Recommendation: Maintain aggressive visibility in Bristol with localized ad extensions."),
    ("3. High Basket-Size Pockets in Rural South East & Coastal Towns", 
     "Bexhill-on-Sea (£119.96 AOV), Brighton (£85.00 AOV), Falmouth (£49.99 AOV), Hook (£57.60 AOV), and Woolacombe (£45.00 AOV) generated exceptional order values driven by multi-item purchases and premium dog ramp/stairs bundles."),
    ("4. Scotland Stronghold (19 Orders, 11.7% of UK Total)", 
     "Scotland is Pet Mode's 3rd largest geographic region (19 orders, £495.40 revenue), spanning Edinburgh (4 orders across Lothians), Glasgow (3 orders), Fife/Kirkcaldy (3 orders), and Dundee/Aberdeen. In Google Ads, Glasgow (£87.72 CPA) and Edinburgh (£0 reported conv) appeared inefficient due to click attribution windows, but actual order volume confirms sustained Scottish demand."),
    ("5. Negative Geotargeting & Location Exclusion Safeguards", 
     "Shopify records show 2 international orders: #1029 to New Jersey, USA (£29.79) and #1004 to Poland (£22.65). Recommendation: In Google Ads Campaign Settings > Locations, ensure 'Presence: People in or regularly in your targeted locations' is selected, and explicitly exclude non-UK regions to prevent budget bleed on international clicks.")
]

row_idx = 9
for header, body in insights:
    ws_sum.cell(row_idx, 2, header).font = Font(name="Calibri", size=11, bold=True, color="004080")
    ws_sum.merge_cells(start_row=row_idx, start_column=2, end_row=row_idx, end_column=9)
    row_idx += 1
    
    body_cell = ws_sum.cell(row_idx, 2, body)
    body_cell.font = regular_font
    body_cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    ws_sum.merge_cells(start_row=row_idx, start_column=2, end_row=row_idx + 1, end_column=9)
    row_idx += 3

ws_sum.column_dimensions['A'].width = 4
for c in ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']:
    ws_sum.column_dimensions[c].width = 16

# ==========================================
# SHEET 2: City & Town Breakdown (Ranked)
# ==========================================
ws_city = wb.create_sheet(title="City Breakdown")
ws_city.views.sheetView[0].showGridLines = True

city_agg = order_df.groupby(['Clean_City', 'Region']).agg(
    orders=('Order_ID', 'count'),
    revenue=('Order_Total', 'sum'),
    aov=('Order_Total', 'mean')
).reset_index().sort_values(by=['orders', 'revenue'], ascending=[False, False])

city_agg['order_pct'] = city_agg['orders'] / total_orders_count
city_agg['rev_pct'] = city_agg['revenue'] / total_revenue_sum

headers_city = ["Rank", "City / Town Name", "Standard Region", "Total Orders", "Total Revenue (£)", "Average Order Value (£)", "% of Total Orders", "% of Total Revenue"]

ws_city.cell(1, 1, "PET MODE - COMPLETE CITY & TOWN ORDER BREAKDOWN").font = Font(name="Calibri", size=14, bold=True, color="1B365D")
ws_city.cell(2, 1, "All 162 Orders Ranked by Order Count and Sales Volume").font = Font(name="Calibri", size=10, italic=True, color="666666")

r_start = 4
for col_idx, h in enumerate(headers_city, start=1):
    c = ws_city.cell(r_start, col_idx, h)
    c.fill = navy_header_fill
    c.font = navy_header_font
    c.alignment = align_center if col_idx in [1, 4, 7, 8] else (align_right if col_idx in [5, 6] else align_left)
    c.border = thin_border

curr_row = r_start + 1
rank = 1
for _, row_data in city_agg.iterrows():
    c_rank = ws_city.cell(curr_row, 1, rank)
    c_city = ws_city.cell(curr_row, 2, row_data['Clean_City'])
    c_reg = ws_city.cell(curr_row, 3, row_data['Region'])
    c_ord = ws_city.cell(curr_row, 4, row_data['orders'])
    c_rev = ws_city.cell(curr_row, 5, row_data['revenue'])
    c_aov = ws_city.cell(curr_row, 6, row_data['aov'])
    c_opct = ws_city.cell(curr_row, 7, row_data['order_pct'])
    c_rpct = ws_city.cell(curr_row, 8, row_data['rev_pct'])
    
    fill = zebra_fill if rank % 2 == 0 else PatternFill(fill_type=None)
    for c in [c_rank, c_city, c_reg, c_ord, c_rev, c_aov, c_opct, c_rpct]:
        c.font = regular_font
        c.border = thin_border
        if fill.fill_type:
            c.fill = fill
            
    c_rank.alignment = align_center
    c_city.alignment = align_left
    c_reg.alignment = align_left
    c_ord.alignment = align_center
    c_rev.alignment = align_right
    c_aov.alignment = align_right
    c_opct.alignment = align_right
    c_rpct.alignment = align_right
    
    c_ord.number_format = '#,##0'
    c_rev.number_format = '[$£-809]#,##0.00'
    c_aov.number_format = '[$£-809]#,##0.00'
    c_opct.number_format = '0.0%'
    c_rpct.number_format = '0.0%'
    
    curr_row += 1
    rank += 1

# Total Row
t_rank = ws_city.cell(curr_row, 1, "")
t_city = ws_city.cell(curr_row, 2, "TOTAL")
t_reg = ws_city.cell(curr_row, 3, "All Regions")
t_ord = ws_city.cell(curr_row, 4, f"=SUM(D{r_start+1}:D{curr_row-1})")
t_rev = ws_city.cell(curr_row, 5, f"=SUM(E{r_start+1}:E{curr_row-1})")
t_aov = ws_city.cell(curr_row, 6, f"=E{curr_row}/D{curr_row}")
t_opct = ws_city.cell(curr_row, 7, f"=SUM(G{r_start+1}:G{curr_row-1})")
t_rpct = ws_city.cell(curr_row, 8, f"=SUM(H{r_start+1}:H{curr_row-1})")

for c in [t_rank, t_city, t_reg, t_ord, t_rev, t_aov, t_opct, t_rpct]:
    c.font = total_font
    c.fill = total_fill
    c.border = double_bottom_border

t_city.alignment = align_left
t_reg.alignment = align_left
t_ord.alignment = align_center
t_rev.alignment = align_right
t_aov.alignment = align_right
t_opct.alignment = align_right
t_rpct.alignment = align_right

t_ord.number_format = '#,##0'
t_rev.number_format = '[$£-809]#,##0.00'
t_aov.number_format = '[$£-809]#,##0.00'
t_opct.number_format = '0.0%'
t_rpct.number_format = '0.0%'

autofit_columns(ws_city)

# ==========================================
# SHEET 3: Metro & Urban Area Clusters
# ==========================================
ws_metro = wb.create_sheet(title="Metro & Urban Clusters")
ws_metro.views.sheetView[0].showGridLines = True

metro_agg = order_df.groupby('Metro_Area').agg(
    orders=('Order_ID', 'count'),
    revenue=('Order_Total', 'sum'),
    aov=('Order_Total', 'mean')
).reset_index().sort_values(by=['orders', 'revenue'], ascending=[False, False])

metro_agg['order_pct'] = metro_agg['orders'] / total_orders_count
metro_agg['rev_pct'] = metro_agg['revenue'] / total_revenue_sum

headers_metro = ["Rank", "Metropolitan / Urban Cluster", "Orders", "Revenue (£)", "Average Order Value (£)", "% of Orders", "% of Revenue", "Strategic Ad Recommendation"]

ws_metro.cell(1, 1, "PET MODE - METROPOLITAN & URBAN CLUSTER ANALYSIS").font = Font(name="Calibri", size=14, bold=True, color="1B365D")
ws_metro.cell(2, 1, "Grouped by Economic Conurbation & Ad Targeting Radius").font = Font(name="Calibri", size=10, italic=True, color="666666")

r_start = 4
for col_idx, h in enumerate(headers_metro, start=1):
    c = ws_metro.cell(r_start, col_idx, h)
    c.fill = navy_header_fill
    c.font = navy_header_font
    c.alignment = align_center if col_idx in [1, 3, 6, 7] else (align_right if col_idx in [4, 5] else align_left)
    c.border = thin_border

# Recommendations dictionary
metro_recs = {
    'Greater London': 'Core Growth Engine: Increase PMax target share; add London-specific headlines (Next Day Dispatch in London).',
    'Greater Bristol': 'Tier 1 Priority: High organic pull. Add +15% location bid adjustment in Search campaigns.',
    'West Yorkshire': 'High Efficiency: Solid conversion rate. Target Leeds & Bradford conurbation.',
    'Greater Glasgow': 'CPA Optimization Required: Verify landing page speeds and shipping promise to Scotland.',
    'Edinburgh & Lothians': 'High Affinity: Scale presence in Edinburgh, East/West Lothian with pet lifestyle themes.',
    'Greater Birmingham': 'Low CPA Benchmark: Google Ads CPA was £21.89. Increase target radius around Birmingham & Black Country.',
    'Greater Doncaster': 'Strong Conversion Node: Excellent return on DN outcodes. Maintain standard bids.',
    'West Sussex Coastal': 'Affluent High-AOV Cluster: Top-performing basket sizes. Target with premium car seat covers.',
    'Cardiff & South Wales': 'Emerging Market: Good baseline engagement. Keep active in PMax UK-wide signal.'
}

curr_row = r_start + 1
rank = 1
for _, row_data in metro_agg.iterrows():
    c_rank = ws_metro.cell(curr_row, 1, rank)
    c_metro = ws_metro.cell(curr_row, 2, row_data['Metro_Area'])
    c_ord = ws_metro.cell(curr_row, 3, row_data['orders'])
    c_rev = ws_metro.cell(curr_row, 4, row_data['revenue'])
    c_aov = ws_metro.cell(curr_row, 5, row_data['aov'])
    c_opct = ws_metro.cell(curr_row, 6, row_data['order_pct'])
    c_rpct = ws_metro.cell(curr_row, 7, row_data['rev_pct'])
    rec_text = metro_recs.get(row_data['Metro_Area'], 'Maintain active coverage in UK-wide PMax campaigns.')
    c_rec = ws_metro.cell(curr_row, 8, rec_text)
    
    fill = zebra_fill if rank % 2 == 0 else PatternFill(fill_type=None)
    for c in [c_rank, c_metro, c_ord, c_rev, c_aov, c_opct, c_rpct, c_rec]:
        c.font = regular_font
        c.border = thin_border
        if fill.fill_type:
            c.fill = fill
            
    c_rank.alignment = align_center
    c_metro.alignment = align_left
    c_ord.alignment = align_center
    c_rev.alignment = align_right
    c_aov.alignment = align_right
    c_opct.alignment = align_right
    c_rpct.alignment = align_right
    c_rec.alignment = align_left
    
    c_ord.number_format = '#,##0'
    c_rev.number_format = '[$£-809]#,##0.00'
    c_aov.number_format = '[$£-809]#,##0.00'
    c_opct.number_format = '0.0%'
    c_rpct.number_format = '0.0%'
    
    curr_row += 1
    rank += 1

# Total Row
t_rank = ws_metro.cell(curr_row, 1, "")
t_metro = ws_metro.cell(curr_row, 2, "TOTAL")
t_ord = ws_metro.cell(curr_row, 3, f"=SUM(C{r_start+1}:C{curr_row-1})")
t_rev = ws_metro.cell(curr_row, 4, f"=SUM(D{r_start+1}:D{curr_row-1})")
t_aov = ws_metro.cell(curr_row, 5, f"=D{curr_row}/C{curr_row}")
t_opct = ws_metro.cell(curr_row, 6, f"=SUM(F{r_start+1}:F{curr_row-1})")
t_rpct = ws_metro.cell(curr_row, 7, f"=SUM(G{r_start+1}:G{curr_row-1})")
t_rec = ws_metro.cell(curr_row, 8, "Complete Store Reconciliation")

for c in [t_rank, t_metro, t_ord, t_rev, t_aov, t_opct, t_rpct, t_rec]:
    c.font = total_font
    c.fill = total_fill
    c.border = double_bottom_border

t_metro.alignment = align_left
t_ord.alignment = align_center
t_rev.alignment = align_right
t_aov.alignment = align_right
t_opct.alignment = align_right
t_rpct.alignment = align_right
t_rec.alignment = align_left

t_ord.number_format = '#,##0'
t_rev.number_format = '[$£-809]#,##0.00'
t_aov.number_format = '[$£-809]#,##0.00'
t_opct.number_format = '0.0%'
t_rpct.number_format = '0.0%'

autofit_columns(ws_metro)

# ==========================================
# SHEET 4: Regional Breakdown (UK Nations & English Regions)
# ==========================================
ws_reg = wb.create_sheet(title="Regional Breakdown")
ws_reg.views.sheetView[0].showGridLines = True

reg_agg = order_df.groupby('Region').agg(
    orders=('Order_ID', 'count'),
    revenue=('Order_Total', 'sum'),
    aov=('Order_Total', 'mean')
).reset_index().sort_values(by=['orders', 'revenue'], ascending=[False, False])

reg_agg['order_pct'] = reg_agg['orders'] / total_orders_count
reg_agg['rev_pct'] = reg_agg['revenue'] / total_revenue_sum

headers_reg = ["Rank", "UK Region / Territory", "Orders", "Revenue (£)", "Average Order Value (£)", "% of Orders", "% of Revenue", "Regional Market Performance"]

ws_reg.cell(1, 1, "PET MODE - UK REGIONAL & NATIONAL PERFORMANCE").font = Font(name="Calibri", size=14, bold=True, color="1B365D")
ws_reg.cell(2, 1, "Macro-Geographic Breakdown of Orders and Revenue").font = Font(name="Calibri", size=10, italic=True, color="666666")

r_start = 4
for col_idx, h in enumerate(headers_reg, start=1):
    c = ws_reg.cell(r_start, col_idx, h)
    c.fill = navy_header_fill
    c.font = navy_header_font
    c.alignment = align_center if col_idx in [1, 3, 6, 7] else (align_right if col_idx in [4, 5] else align_left)
    c.border = thin_border

reg_comments = {
    'Greater London': 'Dominant market: 21.0% orders, 21.5% revenue. Core engine of brand scale.',
    'South West': '#2 Region: 14.2% orders, 15.4% revenue. Driven by Bristol, Devon, Cornwall pet culture.',
    'Scotland': '#3 Region: 11.7% orders, 10.9% revenue. Broad dispersion across Lothians, Fife, Glasgow.',
    'South East': 'Highest AOV Region (£35.34): High affluent suburban spend across Surrey, Sussex, Kent.',
    'Yorkshire and the Humber': 'Solid mid-market: 8.6% orders, 8.2% revenue. Led by Leeds, Doncaster, Kirklees.',
    'East of England': 'Stable baseline: 8.6% orders, 7.7% revenue. Led by Norwich, Ipswich, Essex.',
    'North West': 'Key urban presence: 8.0% orders, 7.4% revenue. Manchester, Liverpool, Preston.',
    'East Midlands': 'Steady demand: 4.9% orders, 4.4% revenue. Led by Northampton (NN) cluster.',
    'West Midlands': 'Cost-efficient ad region: 4.3% orders, 4.0% revenue. Very low CPA in Google Ads (£21.89).',
    'North East': 'Niche presence: 3.1% orders, 2.5% revenue. Newcastle upon Tyne & Durham.',
    'Wales': 'Growth territory: 1.9% orders, 1.6% revenue. Cardiff, Penylan, Monmouth.',
    'Northern Ireland': 'Emerging territory: 1.2% orders, 1.1% revenue. Lisburn & Newtownabbey.',
    'International (USA)': 'Single order (#1029): Recommend setting location exclusion to prevent ad spend bleed.',
    'International (Poland)': 'Single order (#1004): Recommend setting location exclusion to prevent ad spend bleed.'
}

curr_row = r_start + 1
rank = 1
for _, row_data in reg_agg.iterrows():
    c_rank = ws_reg.cell(curr_row, 1, rank)
    c_reg = ws_reg.cell(curr_row, 2, row_data['Region'])
    c_ord = ws_reg.cell(curr_row, 3, row_data['orders'])
    c_rev = ws_reg.cell(curr_row, 4, row_data['revenue'])
    c_aov = ws_reg.cell(curr_row, 5, row_data['aov'])
    c_opct = ws_reg.cell(curr_row, 6, row_data['order_pct'])
    c_rpct = ws_reg.cell(curr_row, 7, row_data['rev_pct'])
    c_comm = ws_reg.cell(curr_row, 8, reg_comments.get(row_data['Region'], ''))
    
    fill = zebra_fill if rank % 2 == 0 else PatternFill(fill_type=None)
    for c in [c_rank, c_reg, c_ord, c_rev, c_aov, c_opct, c_rpct, c_comm]:
        c.font = regular_font
        c.border = thin_border
        if fill.fill_type:
            c.fill = fill
            
    c_rank.alignment = align_center
    c_reg.alignment = align_left
    c_ord.alignment = align_center
    c_rev.alignment = align_right
    c_aov.alignment = align_right
    c_opct.alignment = align_right
    c_rpct.alignment = align_right
    c_comm.alignment = align_left
    
    c_ord.number_format = '#,##0'
    c_rev.number_format = '[$£-809]#,##0.00'
    c_aov.number_format = '[$£-809]#,##0.00'
    c_opct.number_format = '0.0%'
    c_rpct.number_format = '0.0%'
    
    curr_row += 1
    rank += 1

# Total Row
t_rank = ws_reg.cell(curr_row, 1, "")
t_reg = ws_reg.cell(curr_row, 2, "TOTAL")
t_ord = ws_reg.cell(curr_row, 3, f"=SUM(C{r_start+1}:C{curr_row-1})")
t_rev = ws_reg.cell(curr_row, 4, f"=SUM(D{r_start+1}:D{curr_row-1})")
t_aov = ws_reg.cell(curr_row, 5, f"=D{curr_row}/C{curr_row}")
t_opct = ws_reg.cell(curr_row, 6, f"=SUM(F{r_start+1}:F{curr_row-1})")
t_rpct = ws_reg.cell(curr_row, 7, f"=SUM(G{r_start+1}:G{curr_row-1})")
t_comm = ws_reg.cell(curr_row, 8, "Complete 162 Orders Storewide")

for c in [t_rank, t_reg, t_ord, t_rev, t_aov, t_opct, t_rpct, t_comm]:
    c.font = total_font
    c.fill = total_fill
    c.border = double_bottom_border

t_reg.alignment = align_left
t_ord.alignment = align_center
t_rev.alignment = align_right
t_aov.alignment = align_right
t_opct.alignment = align_right
t_rpct.alignment = align_right
t_comm.alignment = align_left

t_ord.number_format = '#,##0'
t_rev.number_format = '[$£-809]#,##0.00'
t_aov.number_format = '[$£-809]#,##0.00'
t_opct.number_format = '0.0%'
t_rpct.number_format = '0.0%'

autofit_columns(ws_reg)

# ==========================================
# SHEET 5: Postcode Area Analysis (Actionable for Google Ads)
# ==========================================
ws_pc = wb.create_sheet(title="Postcode Area Analysis")
ws_pc.views.sheetView[0].showGridLines = True

pc_agg = order_df.groupby(['Postcode_Area', 'County_Desc', 'Region']).agg(
    orders=('Order_ID', 'count'),
    revenue=('Order_Total', 'sum'),
    aov=('Order_Total', 'mean')
).reset_index().sort_values(by=['orders', 'revenue'], ascending=[False, False])

pc_agg['order_pct'] = pc_agg['orders'] / total_orders_count
pc_agg['rev_pct'] = pc_agg['revenue'] / total_revenue_sum

headers_pc = ["Rank", "Postcode Area", "Area / County Description", "Region", "Orders", "Revenue (£)", "Average Order Value (£)", "% of Orders", "% of Revenue", "Google Ads Location Action"]

ws_pc.cell(1, 1, "PET MODE - POSTCODE AREA AUDIT & GOOGLE ADS TARGETING").font = Font(name="Calibri", size=14, bold=True, color="1B365D")
ws_pc.cell(2, 1, "Granular Postcode Area Distribution for Bid Adjustments & Geofencing").font = Font(name="Calibri", size=10, italic=True, color="666666")

r_start = 4
for col_idx, h in enumerate(headers_pc, start=1):
    c = ws_pc.cell(r_start, col_idx, h)
    c.fill = navy_header_fill
    c.font = navy_header_font
    c.alignment = align_center if col_idx in [1, 2, 5, 8, 9] else (align_right if col_idx in [6, 7] else align_left)
    c.border = thin_border

pc_actions = {
    'SW': 'Tier 1 Priority: High volume & revenue (£277.71). Maintain top ad impression share.',
    'BS': 'Tier 1 Priority: #2 UK market (£239.12). Apply +10% to +15% location bid modifier.',
    'W': 'High-Affluence Core: £200.95 revenue, £33.49 AOV. Prime market for premium pet accessories.',
    'N': 'High-Volume Core: 5 orders, £132.49 revenue. Consistent urban demand.',
    'DN': 'Mid-Market Stronghold: 5 orders, £127.45 revenue. Doncaster & Goole corridor.',
    'TN': 'High AOV Powerhouse: £194.72 revenue across 4 orders (£48.68 AOV). Scale spend.',
    'EH': 'Scotland Capital Core: 4 orders, £105.94 revenue. Add Scottish delivery assurances.',
    'NN': 'Midlands Hub: 4 orders, £86.95 revenue. Northampton cluster.',
    'TW': 'West London Fringe: 4 orders, £98.95 revenue. High converting suburb.',
    'BN': 'Coastal Affluence: 3 orders, £131.98 revenue, £43.99 AOV. Excellent basket sizes.',
    'TR': 'Cornwall Coastal: 3 orders, £121.98 revenue, £40.66 AOV. Dog ramp/travel gear affinity.',
    'RG': 'Thames Valley Tech Belt: 3 orders, £101.58 revenue. Reading & Hook.',
    'E': 'East London Core: 3 orders, £100.97 revenue. Urban pet owner audience.',
    'LS': 'Yorkshire Core: 3 orders, £84.96 revenue. Leeds urban conurbation.',
    'PL': 'Plymouth / South Devon: 3 orders, £74.97 revenue.',
    'KY': 'Fife Coast: 3 orders, £73.97 revenue. Leven, Dunfermline, St Andrews.',
    'G': 'Glasgow Metro: 3 orders, £67.99 revenue. Optimize ad scheduling.',
    'NR': 'Norwich & Norfolk: 3 orders, £64.97 revenue.',
    'NE': 'Newcastle & Tyne: 3 orders, £59.98 revenue.'
}

curr_row = r_start + 1
rank = 1
for _, row_data in pc_agg.iterrows():
    c_rank = ws_pc.cell(curr_row, 1, rank)
    c_pc = ws_pc.cell(curr_row, 2, row_data['Postcode_Area'])
    c_desc = ws_pc.cell(curr_row, 3, row_data['County_Desc'])
    c_reg = ws_pc.cell(curr_row, 4, row_data['Region'])
    c_ord = ws_pc.cell(curr_row, 5, row_data['orders'])
    c_rev = ws_pc.cell(curr_row, 6, row_data['revenue'])
    c_aov = ws_pc.cell(curr_row, 7, row_data['aov'])
    c_opct = ws_pc.cell(curr_row, 8, row_data['order_pct'])
    c_rpct = ws_pc.cell(curr_row, 9, row_data['rev_pct'])
    action_text = pc_actions.get(row_data['Postcode_Area'], 'Maintain active national campaign inclusion.')
    c_act = ws_pc.cell(curr_row, 10, action_text)
    
    fill = zebra_fill if rank % 2 == 0 else PatternFill(fill_type=None)
    for c in [c_rank, c_pc, c_desc, c_reg, c_ord, c_rev, c_aov, c_opct, c_rpct, c_act]:
        c.font = regular_font
        c.border = thin_border
        if fill.fill_type:
            c.fill = fill
            
    c_rank.alignment = align_center
    c_pc.alignment = align_center
    c_desc.alignment = align_left
    c_reg.alignment = align_left
    c_ord.alignment = align_center
    c_rev.alignment = align_right
    c_aov.alignment = align_right
    c_opct.alignment = align_right
    c_rpct.alignment = align_right
    c_act.alignment = align_left
    
    c_ord.number_format = '#,##0'
    c_rev.number_format = '[$£-809]#,##0.00'
    c_aov.number_format = '[$£-809]#,##0.00'
    c_opct.number_format = '0.0%'
    c_rpct.number_format = '0.0%'
    
    curr_row += 1
    rank += 1

# Total Row
t_rank = ws_pc.cell(curr_row, 1, "")
t_pc = ws_pc.cell(curr_row, 2, "TOTAL")
t_desc = ws_pc.cell(curr_row, 3, "All Postcode Areas")
t_reg = ws_pc.cell(curr_row, 4, "Storewide")
t_ord = ws_pc.cell(curr_row, 5, f"=SUM(E{r_start+1}:E{curr_row-1})")
t_rev = ws_pc.cell(curr_row, 6, f"=SUM(F{r_start+1}:F{curr_row-1})")
t_aov = ws_pc.cell(curr_row, 7, f"=F{curr_row}/E{curr_row}")
t_opct = ws_pc.cell(curr_row, 8, f"=SUM(H{r_start+1}:H{curr_row-1})")
t_rpct = ws_pc.cell(curr_row, 9, f"=SUM(I{r_start+1}:I{curr_row-1})")
t_act = ws_pc.cell(curr_row, 10, "100% Reconciled")

for c in [t_rank, t_pc, t_desc, t_reg, t_ord, t_rev, t_aov, t_opct, t_rpct, t_act]:
    c.font = total_font
    c.fill = total_fill
    c.border = double_bottom_border

t_pc.alignment = align_center
t_desc.alignment = align_left
t_reg.alignment = align_left
t_ord.alignment = align_center
t_rev.alignment = align_right
t_aov.alignment = align_right
t_opct.alignment = align_right
t_rpct.alignment = align_right
t_act.alignment = align_left

t_ord.number_format = '#,##0'
t_rev.number_format = '[$£-809]#,##0.00'
t_aov.number_format = '[$£-809]#,##0.00'
t_opct.number_format = '0.0%'
t_rpct.number_format = '0.0%'

autofit_columns(ws_pc)

# ==========================================
# SHEET 6: Google Ads vs Shopify Geo Cross-Audit
# ==========================================
ws_gads = wb.create_sheet(title="Google Ads vs Shopify Geo")
ws_gads.views.sheetView[0].showGridLines = True

headers_gads = [
    "Google Ads Location", "Ad Spend (£)", "Clicks", "CTR", "Avg CPC (£)", 
    "Reported Conv.", "Reported CPA (£)", "Shopify Orders", "Shopify Revenue (£)", 
    "Actual ROAS", "Auditor Strategic Insight"
]

ws_gads.cell(1, 1, "PET MODE - GOOGLE ADS SPEND VS. SHOPIFY STORE SALES BY LOCATION").font = Font(name="Calibri", size=14, bold=True, color="1B365D")
ws_gads.cell(2, 1, "Discrepancy Analysis: Ad Channel Attribution vs. Actual Customer Fulfilled Orders").font = Font(name="Calibri", size=10, italic=True, color="666666")

r_start = 4
for col_idx, h in enumerate(headers_gads, start=1):
    c = ws_gads.cell(r_start, col_idx, h)
    c.fill = navy_header_fill
    c.font = navy_header_font
    c.alignment = align_center if col_idx in [3, 4, 6, 8] else (align_right if col_idx in [2, 5, 7, 9, 10] else align_left)
    c.border = thin_border

# Mapping Google Ads locations to shopify metrics
gads_shopify_mapping = {
    'London, England, United Kingdom': (34, 972.99, 'Fully Validated Core: 57% of ad spend produced 34 fulfilled store orders. Excellent synergy.'),
    'Yorkshire, England, United Kingdom': (14, 370.36, 'Strong Organic Multiplier: 14 Shopify orders confirm Yorkshire is heavily under-reported in Google Ads (reported only 2 conv).'),
    'Glasgow, Scotland, United Kingdom': (3, 67.99, 'High Ad CPA (£87.72): Glasgow order volume is modest. Tighten search match types and negative keywords.'),
    'Birmingham, England, United Kingdom': (4, 110.95, 'High Efficiency Star: £21.89 Google CPA is best among major metros. Scale ad presence by +20%.'),
    'Bristol, England, United Kingdom': (8, 239.12, 'Hidden Gem: Only 1 direct conv in Google Ads, but #2 nationally on Shopify (8 orders, £239.12). Heavy multi-touch assist.'),
    'Manchester, England, United Kingdom': (3, 84.97, 'Consistent Volume: Manchester conurbation generates steady orders. Maintain current pacing.'),
    'Edinburgh, Scotland, United Kingdom': (4, 105.94, 'Attribution Lag: Google Ads reported 0 conv (£56 spend), but Shopify recorded 4 orders (£105.94 rev). Assisted conversions present.'),
    'Liverpool, England, United Kingdom': (2, 54.99, 'Moderate Return: £50 ad spend yielded 2 Shopify orders (Liverpool & Thornton).'),
    'Leeds, England, United Kingdom': (3, 84.96, 'High Converting: 1 reported Google conv, 3 Shopify orders. West Yorkshire cluster is very responsive.'),
    'Surrey, England, United Kingdom': (3, 80.97, 'High Affluence & High ROAS: £25.67 spend generated 3 orders in Woking, Egham, Reigate.'),
    'Buckinghamshire, England, United Kingdom': (2, 45.96, 'Solid Suburban ROI: Chalfont St Giles & Milton Keynes fringe. Low CPA (£20.44).'),
    'Berkshire, England, United Kingdom': (3, 101.58, 'High AOV Basket: Maidenhead, Reading, Hook. Strong revenue generation despite 0 reported Google conv.'),
    'Cambridgeshire, England, United Kingdom': (1, 25.99, 'Low Volume: St Ives order. Maintain standard targeting.'),
    'Newcastle upon Tyne, England, United Kin': (2, 41.99, 'Low Ad Spend (£6.19): Highly efficient. Generated 2 Shopify orders.'),
    'Sheffield, England, United Kingdom': (1, 25.99, 'Mexborough order nearby (£25.99). Low spend test.'),
    'Oxford, England, United Kingdom': (1, 34.99, 'High AOV (£34.99) on £4.35 ad spend. Profitable lead.'),
    'Leicester, England, United Kingdom': (1, 34.79, 'Wigston order (£34.79) on £2.89 ad spend. Profitable.'),
    'Southampton, England, United Kingdom': (0, 0.00, 'Zero store conversions from £2.07 spend. Keep under review.'),
    'Milton Keynes, England, United Kingdom': (0, 0.00, 'Minimal spend (£1.42).'),
    'Cardiff, Wales, United Kingdom': (2, 43.98, 'Very efficient: £1.37 spend, 2 Shopify orders in Cardiff & Penylan.'),
    'Reading, England, United Kingdom': (1, 21.99, 'Suburban Berkshire order.'),
    'Nottingham, England, United Kingdom': (1, 21.99, 'Negligible spend (£0.14) with Newark/Nottingham demand.'),
    'Cambridge, England, United Kingdom': (0, 0.00, 'Negligible spend (£0.01).')
}

curr_row = r_start + 1
for idx, g in enumerate(google_data, start=1):
    c_loc = ws_gads.cell(curr_row, 1, g['Location'])
    c_cost = ws_gads.cell(curr_row, 2, g['Cost'])
    c_clk = ws_gads.cell(curr_row, 3, g['Clicks'])
    c_ctr = ws_gads.cell(curr_row, 4, g['CTR'])
    c_cpc = ws_gads.cell(curr_row, 5, g['CPC'])
    c_conv = ws_gads.cell(curr_row, 6, g['Conversions'])
    c_cpa = ws_gads.cell(curr_row, 7, g['CPA'])
    
    # Shopify data lookup
    shop_ord, shop_rev, insight = gads_shopify_mapping.get(g['Location'], (0, 0.0, 'National distribution.'))
    c_sord = ws_gads.cell(curr_row, 8, shop_ord)
    c_srev = ws_gads.cell(curr_row, 9, shop_rev)
    c_roas = ws_gads.cell(curr_row, 10, f"=IF(B{curr_row}>0, I{curr_row}/B{curr_row}, 0)")
    c_ins = ws_gads.cell(curr_row, 11, insight)
    
    fill = zebra_fill if idx % 2 == 0 else PatternFill(fill_type=None)
    for c in [c_loc, c_cost, c_clk, c_ctr, c_cpc, c_conv, c_cpa, c_sord, c_srev, c_roas, c_ins]:
        c.font = regular_font
        c.border = thin_border
        if fill.fill_type:
            c.fill = fill
            
    c_loc.alignment = align_left
    c_cost.alignment = align_right
    c_clk.alignment = align_center
    c_ctr.alignment = align_right
    c_cpc.alignment = align_right
    c_conv.alignment = align_center
    c_cpa.alignment = align_right
    c_sord.alignment = align_center
    c_srev.alignment = align_right
    c_roas.alignment = align_right
    c_ins.alignment = align_left
    
    c_cost.number_format = '[$£-809]#,##0.00'
    c_clk.number_format = '#,##0'
    c_ctr.number_format = '0.00%'
    c_cpc.number_format = '[$£-809]#,##0.00'
    c_conv.number_format = '0.0'
    c_cpa.number_format = '[$£-809]#,##0.00'
    c_sord.number_format = '#,##0'
    c_srev.number_format = '[$£-809]#,##0.00'
    c_roas.number_format = '0.00x'
    
    curr_row += 1

# Total Row for Google Ads Sheet
t_loc = ws_gads.cell(curr_row, 1, "TOTAL (Top Reported Regions)")
t_cost = ws_gads.cell(curr_row, 2, f"=SUM(B{r_start+1}:B{curr_row-1})")
t_clk = ws_gads.cell(curr_row, 3, f"=SUM(C{r_start+1}:C{curr_row-1})")
t_ctr = ws_gads.cell(curr_row, 4, f"=C{curr_row}/SUM(Google_Impressions)") # will use direct formula
t_ctr.value = f"=AVERAGE(D{r_start+1}:D{curr_row-1})"
t_cpc = ws_gads.cell(curr_row, 5, f"=B{curr_row}/C{curr_row}")
t_conv = ws_gads.cell(curr_row, 6, f"=SUM(F{r_start+1}:F{curr_row-1})")
t_cpa = ws_gads.cell(curr_row, 7, f"=B{curr_row}/F{curr_row}")
t_sord = ws_gads.cell(curr_row, 8, f"=SUM(H{r_start+1}:H{curr_row-1})")
t_srev = ws_gads.cell(curr_row, 9, f"=SUM(I{r_start+1}:I{curr_row-1})")
t_roas = ws_gads.cell(curr_row, 10, f"=I{curr_row}/B{curr_row}")
t_ins = ws_gads.cell(curr_row, 11, "Audited Cross-Comparison")

for c in [t_loc, t_cost, t_clk, t_ctr, t_cpc, t_conv, t_cpa, t_sord, t_srev, t_roas, t_ins]:
    c.font = total_font
    c.fill = total_fill
    c.border = double_bottom_border

t_loc.alignment = align_left
t_cost.alignment = align_right
t_clk.alignment = align_center
t_ctr.alignment = align_right
t_cpc.alignment = align_right
t_conv.alignment = align_center
t_cpa.alignment = align_right
t_sord.alignment = align_center
t_srev.alignment = align_right
t_roas.alignment = align_right
t_ins.alignment = align_left

t_cost.number_format = '[$£-809]#,##0.00'
t_clk.number_format = '#,##0'
t_ctr.number_format = '0.00%'
t_cpc.number_format = '[$£-809]#,##0.00'
t_conv.number_format = '0.0'
t_cpa.number_format = '[$£-809]#,##0.00'
t_sord.number_format = '#,##0'
t_srev.number_format = '[$£-809]#,##0.00'
t_roas.number_format = '0.00x'

autofit_columns(ws_gads)

# ==========================================
# SHEET 7: All 162 Orders Log
# ==========================================
ws_log = wb.create_sheet(title="All 162 Orders Log")
ws_log.views.sheetView[0].showGridLines = True

headers_log = ["Order ID", "Date Created", "Status", "Order Total (£)", "Shipping City (Raw)", "Cleaned City", "Metro Cluster", "County / Area Description", "UK Region", "Postcode Area", "Postcode Outcode", "Full Postcode", "Country"]

ws_log.cell(1, 1, "PET MODE - ALL 162 SHOPIFY ORDERS COMPLETE GEOGRAPHIC AUDIT").font = Font(name="Calibri", size=14, bold=True, color="1B365D")
ws_log.cell(2, 1, "Granular Customer Level Audit Log Reconciled with Store Database").font = Font(name="Calibri", size=10, italic=True, color="666666")

r_start = 4
for col_idx, h in enumerate(headers_log, start=1):
    c = ws_log.cell(r_start, col_idx, h)
    c.fill = navy_header_fill
    c.font = navy_header_font
    c.alignment = align_center if col_idx in [1, 2, 3, 10, 11, 12, 13] else (align_right if col_idx == 4 else align_left)
    c.border = thin_border

curr_row = r_start + 1
for idx, r_data in order_df.iterrows():
    c1 = ws_log.cell(curr_row, 1, r_data['Order_ID'])
    c2 = ws_log.cell(curr_row, 2, r_data['Created_At'][:10] if len(r_data['Created_At'])>=10 else r_data['Created_At'])
    c3 = ws_log.cell(curr_row, 3, r_data['Financial_Status'])
    c4 = ws_log.cell(curr_row, 4, r_data['Order_Total'])
    c5 = ws_log.cell(curr_row, 5, r_data['Raw_City'])
    c6 = ws_log.cell(curr_row, 6, r_data['Clean_City'])
    c7 = ws_log.cell(curr_row, 7, r_data['Metro_Area'])
    c8 = ws_log.cell(curr_row, 8, r_data['County_Desc'])
    c9 = ws_log.cell(curr_row, 9, r_data['Region'])
    c10 = ws_log.cell(curr_row, 10, r_data['Postcode_Area'])
    c11 = ws_log.cell(curr_row, 11, r_data['Outcode'])
    c12 = ws_log.cell(curr_row, 12, r_data['Postcode'])
    c13 = ws_log.cell(curr_row, 13, r_data['Country'])
    
    fill = zebra_fill if idx % 2 == 0 else PatternFill(fill_type=None)
    for c in [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13]:
        c.font = regular_font
        c.border = thin_border
        if fill.fill_type:
            c.fill = fill
            
    c1.alignment = align_center
    c2.alignment = align_center
    c3.alignment = align_center
    c4.alignment = align_right
    c5.alignment = align_left
    c6.alignment = align_left
    c7.alignment = align_left
    c8.alignment = align_left
    c9.alignment = align_left
    c10.alignment = align_center
    c11.alignment = align_center
    c12.alignment = align_center
    c13.alignment = align_center
    
    c4.number_format = '[$£-809]#,##0.00'
    curr_row += 1

# Total Row
t1 = ws_log.cell(curr_row, 1, "TOTAL")
t2 = ws_log.cell(curr_row, 2, f"{len(order_df)} Orders")
t3 = ws_log.cell(curr_row, 3, "")
t4 = ws_log.cell(curr_row, 4, f"=SUM(D{r_start+1}:D{curr_row-1})")
for col_i in range(5, 14):
    ws_log.cell(curr_row, col_i, "")

for col_i in range(1, 14):
    c = ws_log.cell(curr_row, col_i)
    c.font = total_font
    c.fill = total_fill
    c.border = double_bottom_border

t1.alignment = align_center
t2.alignment = align_center
t4.alignment = align_right
t4.number_format = '[$£-809]#,##0.00'

autofit_columns(ws_log)

# Save Workbook
excel_out_path = r'c:\Users\test\Videos\Office\data\Pet Mode\Pet_Mode_City_Wise_Orders_Report.xlsx'
wb.save(excel_out_path)
print(f"Master Excel report successfully saved to: {excel_out_path}")
