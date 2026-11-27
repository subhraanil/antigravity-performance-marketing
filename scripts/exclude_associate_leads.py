import pandas as pd
import numpy as np
import os

XLSX_PATH = r"C:\Users\test\.gemini\antigravity\brain\cc612d54-d8d2-4a43-a285-4bda2d3e91ba\.user_uploaded\media_1795518002487_5ba75fc4.xlsx"
OUT_EXCEL = r"C:\Users\test\Videos\Office\reports\Share_Samadhan_Associate_Lead_Exclusion_Analysis.xlsx"
OUT_CASE  = r"C:\Users\test\Videos\Office\case-studies\Share Samadhan\Share_Samadhan_Associate_Lead_Exclusion_Analysis.xlsx"
OUT_CSV   = r"C:\Users\test\Videos\Office\reports\Share_Samadhan_Associate_Leads_Monthly.csv"

os.makedirs(r"C:\Users\test\Videos\Office\reports", exist_ok=True)
os.makedirs(r"C:\Users\test\Videos\Office\case-studies\Share Samadhan", exist_ok=True)

print("Loading data...")
df = pd.read_excel(XLSX_PATH, sheet_name=0)
print(f"Loaded {len(df)} rows, {len(df.columns)} cols")
print("Columns:", list(df.columns))

# Parse date
df['Query Date & Time'] = pd.to_datetime(df['Query Date & Time'], errors='coerce')

# Filter to Nov 2025 - Nov 2026 only (the reporting period)
df = df[
    (df['Query Date & Time'] >= '2025-11-01') &
    (df['Query Date & Time'] <= '2026-11-23')
]
print(f"Rows in Nov 2025 – Nov 2026 reporting window: {len(df)}")

df['Month'] = df['Query Date & Time'].dt.to_period('M').astype(str)

# --- Identify manually-added associate leads ---
# Source = "Supervisor Panel" means the lead was entered manually by an associate/supervisor
# NOT through digital channels (Landing Page, Anantya.ai WhatsApp, Contact Us, Website, Blog, etc.)
df['Is_Associate_Manual'] = df['Source'].str.strip() == 'Supervisor Panel'

print("\n=== Source Distribution in Reporting Period ===")
print(df['Source'].value_counts().to_string())

# --- Monthly breakdown ---
month_order = [
    '2025-11','2025-12',
    '2026-01','2026-02','2026-03','2026-04','2026-05','2026-06',
    '2026-07','2026-08','2026-09','2026-10','2026-11'
]
month_labels = [
    'November 2025','December 2025',
    'January 2026','February 2026','March 2026','April 2026',
    'May 2026','June 2026','July 2026','August 2026',
    'September 2026','October 2026','November 2026'
]

monthly = []
for m_code, m_label in zip(month_order, month_labels):
    mdf = df[df['Month'] == m_code]
    total = len(mdf)
    assoc_leads = int(mdf['Is_Associate_Manual'].sum())
    digital_leads = total - assoc_leads
    pct = round(assoc_leads / total * 100, 1) if total > 0 else 0
    monthly.append({
        'Month': m_label,
        'Total CRM Leads (Original)': total,
        'Associate-Added (Manual) Leads': assoc_leads,
        'Verified Digital Leads (Excl. Manual)': digital_leads,
        '% Associate-Added': f"{pct}%"
    })

summary_df = pd.DataFrame(monthly)

# Total row
summary_df.loc[len(summary_df)] = {
    'Month': 'TOTAL (Nov 2025 – Nov 2026)',
    'Total CRM Leads (Original)': summary_df['Total CRM Leads (Original)'].sum(),
    'Associate-Added (Manual) Leads': summary_df['Associate-Added (Manual) Leads'].sum(),
    'Verified Digital Leads (Excl. Manual)': summary_df['Verified Digital Leads (Excl. Manual)'].sum(),
    '% Associate-Added': f"{round(summary_df['Associate-Added (Manual) Leads'].sum() / summary_df['Total CRM Leads (Original)'].sum() * 100, 1)}%"
}

print("\n=== Monthly Associate Lead Exclusion Summary ===")
print(summary_df.to_string(index=False))

# --- Associate-added rows detail ---
assoc_df = df[df['Is_Associate_Manual']].copy()
assoc_df_out = assoc_df[[
    'Sl.No.', 'Client Name', 'Query Date & Time', 'Source', 
    'Referred Associate', 'Parent Associate', 'Assigned To (Sales Team)',
    'Nature of Investment', 'City', 'Reference', 'Stage Name', 'Month'
]].copy()

# --- Referred associate breakdown within Supervisor Panel leads ---
assoc_detail = assoc_df.groupby('Referred Associate').size().reset_index(name='Leads')
assoc_detail = assoc_detail.sort_values('Leads', ascending=False)

# --- Source breakdown in digital-only leads ---
digital_df = df[~df['Is_Associate_Manual']].copy()
digital_sources = digital_df.groupby('Source').size().reset_index(name='Leads')
digital_sources = digital_sources.sort_values('Leads', ascending=False)

# --- Write to Excel with multiple sheets ---
with pd.ExcelWriter(OUT_EXCEL, engine='openpyxl') as writer:
    summary_df.to_excel(writer, sheet_name='Monthly Exclusion Summary', index=False)
    assoc_df_out.to_excel(writer, sheet_name='Associate-Added Leads (Raw)', index=False)
    assoc_detail.to_excel(writer, sheet_name='Associate Breakdown', index=False)
    digital_sources.to_excel(writer, sheet_name='Verified Digital Sources', index=False)

import shutil
shutil.copy2(OUT_EXCEL, OUT_CASE)

# Save CSV too
summary_df.to_csv(OUT_CSV, index=False, encoding='utf-8-sig')

print(f"\nSaved to:\n  {OUT_EXCEL}\n  {OUT_CASE}\n  {OUT_CSV}")
print("\n=== SUMMARY ===")
total_all = len(df)
total_assoc = int(df['Is_Associate_Manual'].sum())
total_digital = total_all - total_assoc
print(f"Total CRM Leads (original, Nov 2025 – Nov 2026): {total_all}")
print(f"Associate-added (Supervisor Panel) leads EXCLUDED: {total_assoc}")
print(f"Verified Digital / Inbound Leads (net): {total_digital}")
