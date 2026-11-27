"""
Update both Excel files to exclude 3,202 manually-added Supervisor Panel leads.
Works by:
1. Re-running the full lead classification against the uploaded CRM file
2. Writing corrected values into both existing Excel workbooks in-place
"""
import pandas as pd
import numpy as np
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
import shutil, os

XLSX_SRC  = r"C:\Users\test\.gemini\antigravity\brain\cc612d54-d8d2-4a43-a285-4bda2d3e91ba\.user_uploaded\media_1795518002487_5ba75fc4.xlsx"
CRM_XLSX  = r"C:\Users\test\Videos\Office\reports\Share_Samadhan_Annual_Leads_Analysis_Nov2025_Nov2026.xlsx"
PERF_XLSX = r"C:\Users\test\Videos\Office\reports\Share_Samadhan_Positive_Performance_Metrics.xlsx"
CS_CRM    = r"C:\Users\test\Videos\Office\case-studies\Share Samadhan\Share_Samadhan_Annual_Leads_Analysis_Nov2025_Nov2026.xlsx"
CS_PERF   = r"C:\Users\test\Videos\Office\case-studies\Share Samadhan\Share_Samadhan_Positive_Performance_Metrics.xlsx"

MONTH_ORDER  = ['2025-11','2025-12','2026-01','2026-02','2026-03','2026-04',
                '2026-05','2026-06','2026-07','2026-08','2026-09','2026-10','2026-11']
MONTH_LABELS = ['November 2025','December 2025','January 2026','February 2026',
                'March 2026','April 2026','May 2026','June 2026','July 2026',
                'August 2026','September 2026','October 2026','November 2026']

# ─── 1. Load & clean raw CRM data ─────────────────────────────────────────────
print("Loading CRM data...")
df = pd.read_excel(XLSX_SRC, sheet_name=0)
df['Query Date & Time'] = pd.to_datetime(df['Query Date & Time'], errors='coerce')
df = df[(df['Query Date & Time'] >= '2025-11-01') & (df['Query Date & Time'] <= '2026-11-23')]
df['YearMonth'] = df['Query Date & Time'].dt.to_period('M').astype(str)

# Exclude Supervisor Panel manually-added leads
df_digital = df[df['Source'].str.strip() != 'Supervisor Panel'].copy()
df_assoc   = df[df['Source'].str.strip() == 'Supervisor Panel'].copy()
print(f"Total in window: {len(df)} | Digital: {len(df_digital)} | Assoc excluded: {len(df_assoc)}")

# ─── 2. Source → channel mapping (same logic as original analysis) ─────────────
def map_channel(row):
    src = str(row.get('Source', '')).strip()
    camp = str(row.get('Campaign Source', '')).strip()
    ref  = str(row.get('Reference', '')).strip().lower()
    if 'whatsapp' in src.lower() or 'anantya' in src.lower():
        return 'WhatsApp Leads'
    if src == 'Landing Page':
        if camp == 'Facebook' or 'facebook' in ref or 'meta' in ref or 'fb' in ref:
            return 'Facebook / Meta Ads'
        elif camp == 'GoogleAds' or 'google' in ref:
            return 'Google Ads / Search'
        else:
            return 'Direct / Organic Landing Page'
    if src == 'Contact Us':
        return 'Website Contact Us Page'
    if src == 'Blog Page':
        return 'Website Blog Page'
    if src in ('www.lostshare.com', 'www.iepfclaim.com'):
        return 'Microsites (LostShare / IEPFClaim)'
    if src == 'NRI Landing Page':
        return 'NRI Landing Page'
    if src == 'Website - Services':
        return 'Website Service Pages'
    if src == 'WSC User':
        return 'Direct / Others'
    return 'Direct / Organic Landing Page'

df_digital['Channel'] = df_digital.apply(map_channel, axis=1)

# ─── 3. Nature of Investment → service category mapping ───────────────────────
def map_service(val):
    v = str(val).lower().strip()
    if 'iepf' in v or 'free search' in v:                     return 'IEPF Claim & Free Search'
    if 'transmission' in v:                                    return 'Transmission of Shares'
    if 'pf' in v or 'provident' in v:                         return 'Provident Fund (PF) Claims'
    if 'demat' in v or 'physical' in v:                        return 'Physical Shares to Demat'
    if 'duplicate' in v:                                       return 'Duplicate Issue of Shares'
    if 'mutual' in v or 'scwf' in v:                          return 'Mutual Funds (SCWF)'
    if 'insurance' in v:                                       return 'Unclaimed Insurance'
    if 'bank' in v or 'deaf' in v:                            return 'Inoperative Bank Deposits (DEAF)'
    if 'debtor' in v or 'litigation' in v:                    return 'Debtor Recovery & Litigation'
    if 'nri' in v:                                             return 'NRI Samadhan'
    if 'lost share' in v or 'whatsapp' in v or 'web' in v:   return 'Lost Shares Recovery (WhatsApp / Web)'
    if 'recovery' in v or 'shares recovery' in v:             return 'Shares Recovery (General)'
    if 'portfolio' in v or 'shares' in v:                     return 'Shares (General Portfolio)'
    if 'contact us' in v or 'general' in v or 'enquir' in v: return 'Contact Us Inquiries (General)'
    if v in ('none', 'nan', ''):                              return 'Others / General Inquiries'
    return 'Others / General Inquiries'

df_digital['ServiceCategory'] = df_digital['Nature of Investment'].apply(map_service)

# Strict NRI flag matching domain logic
def is_nri(row):
    if str(row.get('Source', '')).strip() == 'NRI Landing Page':
        return True
    for col in ['Campaign Name', 'Campaign Source', 'Reference']:
        if 'nri' in str(row.get(col, '')).lower():
            return True
    raw_cc = str(row.get('Country Code', '')).strip().replace('+', '')
    if pd.notna(row.get('Country Code')) and raw_cc not in ['', 'nan', 'none', 'None']:
        if raw_cc == '91' or (raw_cc.startswith('91') and len(raw_cc) > 9) or (len(raw_cc) >= 10 and not raw_cc.startswith(('1', '44', '971', '65', '61'))):
            return False
        else:
            return True
    city = str(row.get('City', '')).strip().lower()
    intl_cities = ['dubai', 'london', 'singapore', 'new york', 'california', 'texas', 'sydney', 'toronto', 'melbourne', 'sharjah', 'abu dhabi', 'doha', 'riyadh', 'kuwait', 'muscat', 'chicago', 'houston', 'fremont', 'new jersey']
    for ic in intl_cities:
        if ic in city:
            return True
    return False

df_digital['IsNRI'] = df_digital.apply(is_nri, axis=1)

# ─── 4. Build corrected monthly summary ──────────────────────────────────────
monthly_rows = []
for m_code, m_label in zip(MONTH_ORDER, MONTH_LABELS):
    mdf = df_digital[df_digital['YearMonth'] == m_code]
    total = len(mdf)
    nri   = int(mdf['IsNRI'].sum())
    top_svc = mdf['ServiceCategory'].value_counts().head(3)
    top_svc_str = ', '.join([f"{k} ({v})" for k,v in top_svc.items()])
    top_ch  = mdf['Channel'].value_counts().head(2)
    top_ch_str = ', '.join([f"{k} ({v})" for k,v in top_ch.items()])
    monthly_rows.append([m_label, total, top_svc_str, nri, top_ch_str])

# ─── 5. Build corrected month × service matrix ───────────────────────────────
all_services = sorted(df_digital['ServiceCategory'].unique())
svc_matrix_rows = []
for m_code in MONTH_ORDER:
    mdf = df_digital[df_digital['YearMonth'] == m_code]
    row = {'YearMonth': m_code}
    for svc in all_services:
        row[svc] = int((mdf['ServiceCategory'] == svc).sum())
    row['Total'] = len(mdf)
    svc_matrix_rows.append(row)
svc_df = pd.DataFrame(svc_matrix_rows)
# Total row
totals = {'YearMonth': 'Total'}
for svc in all_services:
    totals[svc] = int(svc_df[svc].sum())
totals['Total'] = int(svc_df['Total'].sum())
svc_df = pd.concat([svc_df, pd.DataFrame([totals])], ignore_index=True)

# ─── 6. Build corrected month × source/channel matrix ───────────────────────
all_channels = sorted(df_digital['Channel'].unique())
ch_matrix_rows = []
for m_code in MONTH_ORDER:
    mdf = df_digital[df_digital['YearMonth'] == m_code]
    row = {'YearMonth': m_code}
    for ch in all_channels:
        row[ch] = int((mdf['Channel'] == ch).sum())
    row['Total'] = len(mdf)
    ch_matrix_rows.append(row)
ch_df = pd.DataFrame(ch_matrix_rows)
ch_totals = {'YearMonth': 'Total'}
for ch in all_channels:
    ch_totals[ch] = int(ch_df[ch].sum())
ch_totals['Total'] = int(ch_df['Total'].sum())
ch_df = pd.concat([ch_df, pd.DataFrame([ch_totals])], ignore_index=True)

# ─── 7. Service category totals ──────────────────────────────────────────────
svc_totals = []
for svc in all_services:
    sdf = df_digital[df_digital['ServiceCategory'] == svc]
    svc_totals.append([svc, len(sdf), int(sdf['IsNRI'].sum())])
svc_totals.sort(key=lambda x: -x[1])

# ─── 8. Lead source totals ───────────────────────────────────────────────────
ch_totals_list = []
for ch in all_channels:
    cdf = df_digital[df_digital['Channel'] == ch]
    ch_totals_list.append([ch, len(cdf), int(cdf['IsNRI'].sum())])
ch_totals_list.sort(key=lambda x: -x[1])

# ─── 9. Write updated CRM Excel ──────────────────────────────────────────────
print("Updating Share_Samadhan_Annual_Leads_Analysis_Nov2025_Nov2026.xlsx ...")
wb = openpyxl.load_workbook(CRM_XLSX)

# --- Monthly_Summary sheet ---
ws = wb['Monthly_Summary']
# Clear and rewrite from row 2
for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
    for cell in row:
        cell.value = None
for i, row_data in enumerate(monthly_rows):
    ws.cell(i+2, 1).value = row_data[0]
    ws.cell(i+2, 2).value = row_data[1]
    ws.cell(i+2, 3).value = row_data[2]
    ws.cell(i+2, 4).value = row_data[3]
    ws.cell(i+2, 5).value = row_data[4]

# --- Month_x_Service_Matrix sheet ---
ws2 = wb['Month_x_Service_Matrix']
# Clear existing content completely
for row in ws2.iter_rows(min_row=1, max_row=ws2.max_row, max_col=ws2.max_column):
    for cell in row:
        cell.value = None

all_svc_cols = [c for c in svc_df.columns if c not in ('YearMonth', 'Total')]
ws2.cell(1, 1).value = 'YearMonth'
for ci, col in enumerate(all_svc_cols):
    ws2.cell(1, ci+2).value = col
ws2.cell(1, len(all_svc_cols)+2).value = 'Total'

for ri in range(len(svc_df)):
    ws2.cell(ri+2, 1).value = str(svc_df['YearMonth'].iloc[ri])
    for ci, col in enumerate(all_svc_cols):
        ws2.cell(ri+2, ci+2).value = int(svc_df[col].iloc[ri])
    ws2.cell(ri+2, len(all_svc_cols)+2).value = int(svc_df['Total'].iloc[ri])

# --- Month_x_Source_Matrix sheet ---
ws3 = wb['Month_x_Source_Matrix']
for row in ws3.iter_rows(min_row=1, max_row=ws3.max_row, max_col=ws3.max_column):
    for cell in row:
        cell.value = None

all_ch_cols = [c for c in ch_df.columns if c not in ('YearMonth', 'Total')]
ws3.cell(1, 1).value = 'YearMonth'
for ci, col in enumerate(all_ch_cols):
    ws3.cell(1, ci+2).value = col
ws3.cell(1, len(all_ch_cols)+2).value = 'Total'

for ri in range(len(ch_df)):
    ws3.cell(ri+2, 1).value = str(ch_df['YearMonth'].iloc[ri])
    for ci, col in enumerate(all_ch_cols):
        ws3.cell(ri+2, ci+2).value = int(ch_df[col].iloc[ri])
    ws3.cell(ri+2, len(all_ch_cols)+2).value = int(ch_df['Total'].iloc[ri])

# --- Service_Category_Totals sheet ---
ws4 = wb['Service_Category_Totals']
for row in ws4.iter_rows(min_row=2, max_row=ws4.max_row):
    for cell in row:
        cell.value = None
for ri, (cat, tot, nri) in enumerate(svc_totals):
    ws4.cell(ri+2, 1).value = cat
    ws4.cell(ri+2, 2).value = tot
    ws4.cell(ri+2, 3).value = nri

# --- Lead_Source_Totals sheet ---
ws5 = wb['Lead_Source_Totals']
for row in ws5.iter_rows(min_row=2, max_row=ws5.max_row):
    for cell in row:
        cell.value = None
for ri, (ch, tot, nri) in enumerate(ch_totals_list):
    ws5.cell(ri+2, 1).value = ch
    ws5.cell(ri+2, 2).value = tot
    ws5.cell(ri+2, 3).value = nri

wb.save(CRM_XLSX)
shutil.copy2(CRM_XLSX, CS_CRM)
print(f"  Saved: {CRM_XLSX}")

# ─── 10. Update Positive Performance Metrics (Paid_Media_Growth only needs GA4 organic leads updated) ──
# The GA4_Organic_Growth sheet organic leads came from a different source (GA4 not CRM)
# so the organic leads numbers there stay the same.
# The Paid_Media_Growth total paid leads numbers also don't change (they came from ad platform data)
# However the CRM-derived totals in reports need the corrected note added.
# We just add a new sheet 'CRM_Corrected_Monthly' to the Positive Metrics file.
print("Updating Share_Samadhan_Positive_Performance_Metrics.xlsx ...")
wb2 = openpyxl.load_workbook(PERF_XLSX)

# Remove old CRM_Corrected_Monthly if exists
if 'CRM_Corrected_Monthly' in wb2.sheetnames:
    del wb2['CRM_Corrected_Monthly']

ws_new = wb2.create_sheet('CRM_Corrected_Monthly')

# Header row
HDR_FILL = PatternFill('solid', fgColor='0A2540')
HDR_FONT = Font(bold=True, color='FFFFFF', size=10)
headers = [
    'Month', 'Original CRM Total', 'Associate-Added (Excluded)', 
    'Verified Digital Leads', '% Associate-Added',
    'Google Ads Leads', 'Meta Ads Leads', 'WhatsApp Leads',
    'Other Digital Leads', 'NRI Leads'
]
for ci, h in enumerate(headers):
    cell = ws_new.cell(1, ci+1)
    cell.value = h
    cell.font = HDR_FONT
    cell.fill = HDR_FILL
    cell.alignment = Alignment(horizontal='center', wrap_text=True)

# Monthly corrected data
corrected_rows = []
for m_code, m_label in zip(MONTH_ORDER, MONTH_LABELS):
    mdf_all    = df[df['YearMonth'] == m_code]
    mdf_dig    = df_digital[df_digital['YearMonth'] == m_code]
    mdf_assoc  = df_assoc[df_assoc['YearMonth'] == m_code]
    total_orig = len(mdf_all)
    assoc_excl = len(mdf_assoc)
    digital    = len(mdf_dig)
    pct        = round(assoc_excl / total_orig * 100, 1) if total_orig else 0
    ggl_leads  = int((mdf_dig['Channel'] == 'Google Ads / Search').sum())
    meta_leads = int((mdf_dig['Channel'] == 'Facebook / Meta Ads').sum())
    wa_leads   = int((mdf_dig['Channel'] == 'WhatsApp Leads').sum())
    other      = digital - ggl_leads - meta_leads - wa_leads
    nri        = int(mdf_dig['IsNRI'].sum())
    corrected_rows.append([m_label, total_orig, assoc_excl, digital, f"{pct}%", ggl_leads, meta_leads, wa_leads, other, nri])

EVEN_FILL = PatternFill('solid', fgColor='F8F9FA')
TOTAL_FILL = PatternFill('solid', fgColor='EBF3FA')
TOTAL_FONT = Font(bold=True, size=10)

for ri, row in enumerate(corrected_rows):
    fill = EVEN_FILL if ri % 2 == 1 else None
    for ci, val in enumerate(row):
        cell = ws_new.cell(ri+2, ci+1)
        cell.value = val
        cell.font = Font(size=9)
        cell.alignment = Alignment(horizontal='right' if ci > 0 else 'left')
        if fill:
            cell.fill = fill

# Total row
all_dig = df_digital
total_row = [
    'TOTAL (Nov 2025 – Nov 2026)',
    len(df),
    len(df_assoc),
    len(all_dig),
    f"{round(len(df_assoc)/len(df)*100,1)}%",
    int((all_dig['Channel'] == 'Google Ads / Search').sum()),
    int((all_dig['Channel'] == 'Facebook / Meta Ads').sum()),
    int((all_dig['Channel'] == 'WhatsApp Leads').sum()),
    len(all_dig) - int((all_dig['Channel'] == 'Google Ads / Search').sum()) - int((all_dig['Channel'] == 'Facebook / Meta Ads').sum()) - int((all_dig['Channel'] == 'WhatsApp Leads').sum()),
    int(all_dig['IsNRI'].sum())
]
for ci, val in enumerate(total_row):
    cell = ws_new.cell(len(corrected_rows)+2, ci+1)
    cell.value = val
    cell.font = TOTAL_FONT
    cell.fill = TOTAL_FILL
    cell.alignment = Alignment(horizontal='right' if ci > 0 else 'left')

# Column widths
col_widths = [22, 20, 24, 22, 20, 18, 16, 16, 18, 12]
for ci, w in enumerate(col_widths):
    ws_new.column_dimensions[openpyxl.utils.get_column_letter(ci+1)].width = w

wb2.save(PERF_XLSX)
shutil.copy2(PERF_XLSX, CS_PERF)
print(f"  Saved: {PERF_XLSX}")

# ─── Final Summary ────────────────────────────────────────────────────────────
print("\n=== CORRECTED TOTALS ===")
print(f"Original CRM total (reporting window): {len(df)}")
print(f"Associate-added leads (Supervisor Panel) REMOVED: {len(df_assoc)}")
print(f"Verified digital inbound leads: {len(df_digital)}")
print(f"\nCorrected Monthly Breakdown:")
for row in corrected_rows:
    print(f"  {row[0]:<22} Total:{row[3]:>5}  (Excluded: {row[2]:>3}  = {row[4]})")
print(f"\n  {'TOTAL':<22} {sum(r[3] for r in corrected_rows):>5}")
