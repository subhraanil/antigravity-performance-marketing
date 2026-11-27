import os
import openpyxl
import pandas as pd
import numpy as np

folder = r"C:\Users\test\Videos\Office\data\fabb6\November"

def audit_details():
    # 1. Google Ads Campaign Report
    camp_path = os.path.join(folder, "Campaign report (2).xlsx")
    wb_camp = openpyxl.load_workbook(camp_path, data_only=True)
    sheet_c = wb_camp.active
    headers = [sheet_c.cell(3, c).value for c in range(1, sheet_c.max_column+1)]
    
    rows = []
    for r in range(4, sheet_c.max_row+1):
        vals = [sheet_c.cell(r, c).value for c in range(1, sheet_c.max_column+1)]
        if any(vals):
            rows.append(vals)
    df_camp = pd.DataFrame(rows, columns=headers)
    
    # Ensure numeric columns
    for col in ['Cost', 'Conversions', 'Conv. value', 'Impr.', 'Interactions']:
        if col in df_camp.columns:
            df_camp[col] = pd.to_numeric(df_camp[col], errors='coerce').fillna(0)

    print("=" * 80)
    print("GOOGLE ADS CAMPAIGN BREAKDOWN BY MONTH (AUG, SEP, OCT, NOV 2026)")
    print("=" * 80)
    for m in ['August 2026', 'September 2026', 'October 2026', 'November 2026']:
        m_df = df_camp[df_camp['Month'] == m]
        tot_cost = m_df['Cost'].sum()
        tot_conv = m_df['Conversions'].sum()
        tot_val = m_df['Conv. value'].sum()
        cpa = tot_cost / tot_conv if tot_conv > 0 else 0
        roas = tot_val / tot_cost if tot_cost > 0 else 0
        print(f"\n--- {m} --- Total Cost: Rs {tot_cost:,.2f} | Conv: {tot_conv:,.1f} | Val: Rs {tot_val:,.2f} | CPA: Rs {cpa:.2f} | ROAS: {roas:.2f}x")
        
        active_camps = m_df[m_df['Cost'] > 0].sort_values(by='Cost', ascending=False)
        for idx, r in active_camps.iterrows():
            c_cpa = r['Cost'] / r['Conversions'] if r['Conversions'] > 0 else 0
            c_roas = r['Conv. value'] / r['Cost'] if r['Cost'] > 0 else 0
            print(f"  * {r['Campaign']} ({r['Campaign type']}) | Cost: Rs {r['Cost']:,.2f} | Conv: {r['Conversions']:,.1f} | CPA: Rs {c_cpa:.2f} | ROAS: {c_roas:.2f}x | Val: Rs {r['Conv. value']:,.2f}")

    # 2. Product Report
    prod_path = os.path.join(folder, "Product report (7).xlsx")
    if os.path.exists(prod_path):
        wb_prod = openpyxl.load_workbook(prod_path, data_only=True)
        sheet_p = wb_prod.active
        p_headers = [sheet_p.cell(3, c).value for c in range(1, sheet_p.max_column+1)]
        p_rows = []
        for r in range(4, sheet_p.max_row+1):
            vals = [sheet_p.cell(r, c).value for c in range(1, sheet_p.max_column+1)]
            if any(vals):
                p_rows.append(vals)
        df_prod = pd.DataFrame(p_rows, columns=p_headers)
        for col in ['Cost', 'Conversions', 'Conv. value', 'Clicks', 'Impr.']:
            if col in df_prod.columns:
                df_prod[col] = pd.to_numeric(df_prod[col], errors='coerce').fillna(0)
        
        print("\n" + "=" * 80)
        print("GOOGLE SHOPPING / PMAX PRODUCT PERFORMANCE HIGHLIGHTS")
        print("=" * 80)
        print(f"Total Products tracked: {len(df_prod)}")
        tot_prod_cost = df_prod['Cost'].sum()
        tot_prod_conv = df_prod['Conversions'].sum()
        tot_prod_val = df_prod['Conv. value'].sum()
        print(f"Total Product Spend: Rs {tot_prod_cost:,.2f} | Conversions: {tot_prod_conv:,.1f} | Value: Rs {tot_prod_val:,.2f}")
        
        # Zero conversion products with spend
        zero_conv = df_prod[(df_prod['Conversions'] == 0) & (df_prod['Cost'] > 500)].sort_values(by='Cost', ascending=False)
        print(f"\nZero-Conversion Products Burning Budget (>Rs 500 wasted): {len(zero_conv)} products")
        print(f"Total Money Wasted on Zero-Conversion Products: Rs {zero_conv['Cost'].sum():,.2f}")
        for idx, r in zero_conv.head(10).iterrows():
            print(f"  - {r.get('Item ID', r.get('Product title', 'Product'))}: Spend Rs {r['Cost']:,.2f} | Clicks: {r['Clicks']} | 0 Conversions")

        # Top 10 revenue generating products
        top_prod = df_prod.sort_values(by='Conv. value', ascending=False).head(10)
        print(f"\nTop 10 Revenue-Driving Products:")
        for idx, r in top_prod.iterrows():
            p_roas = r['Conv. value'] / r['Cost'] if r['Cost'] > 0 else 0
            p_cpa = r['Cost'] / r['Conversions'] if r['Conversions'] > 0 else 0
            print(f"  + {r.get('Product title', r.get('Item ID', 'Product'))} | Spend Rs {r['Cost']:,.2f} | Conv: {r['Conversions']:,.1f} | Val: Rs {r['Conv. value']:,.2f} | CPA: Rs {p_cpa:.2f} | ROAS: {p_roas:.2f}x")

    # 3. Landing page report
    lp_path = os.path.join(folder, "Landing page report.xlsx")
    if os.path.exists(lp_path):
        wb_lp = openpyxl.load_workbook(lp_path, data_only=True)
        sheet_lp = wb_lp.active
        lp_headers = [sheet_lp.cell(3, c).value for c in range(1, sheet_lp.max_column+1)]
        lp_rows = []
        for r in range(4, sheet_lp.max_row+1):
            vals = [sheet_lp.cell(r, c).value for c in range(1, sheet_lp.max_column+1)]
            if any(vals):
                lp_rows.append(vals)
        df_lp = pd.DataFrame(lp_rows, columns=lp_headers)
        for col in ['Cost', 'Conversions', 'Conv. value', 'Clicks', 'Impr.']:
            if col in df_lp.columns:
                df_lp[col] = pd.to_numeric(df_lp[col], errors='coerce').fillna(0)
        
        print("\n" + "=" * 80)
        print("LANDING PAGE PERFORMANCE HIGHLIGHTS")
        print("=" * 80)
        print(f"Total Landing Pages tracked: {len(df_lp)}")
        zero_conv_lp = df_lp[(df_lp['Conversions'] == 0) & (df_lp['Cost'] > 1000)].sort_values(by='Cost', ascending=False)
        print(f"Landing pages with zero conversions (>Rs 1,000 cost): {len(zero_conv_lp)}")
        print(f"Total Spend on Dead Landing Pages: Rs {zero_conv_lp['Cost'].sum():,.2f}")
        for idx, r in zero_conv_lp.head(10).iterrows():
            print(f"  - {r.get('Landing page', 'URL')}: Cost Rs {r['Cost']:,.2f} | Clicks: {r['Clicks']} | 0 Conversions")

if __name__ == '__main__':
    audit_details()
