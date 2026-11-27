import openpyxl
import pandas as pd
import numpy as np

def run_deep_audit():
    path = r"C:\Users\test\Downloads\Fabb6-Jan-1-2026-to-Nov-17-2026.xlsx"
    wb = openpyxl.load_workbook(path, data_only=True)
    raw = wb['Raw Data Report']
    
    data = []
    for r in range(4, raw.max_row+1):
        vals = [raw.cell(r, c).value for c in range(2, 14)]
        if any(vals):
            data.append(vals)

    cols = ['Campaign', 'Month', 'Reach', 'Impressions', 'Currency', 'Amount_Spent', 'Attribution', 'Purchases', 'Cost_per_Purchase', 'Conv_Value', 'Start', 'End']
    df = pd.DataFrame(data, columns=cols)
    
    df['Amount_Spent'] = pd.to_numeric(df['Amount_Spent'], errors='coerce').fillna(0)
    df['Purchases'] = pd.to_numeric(df['Purchases'], errors='coerce').fillna(0)
    df['Conv_Value'] = pd.to_numeric(df['Conv_Value'], errors='coerce').fillna(0)
    df['Reach'] = pd.to_numeric(df['Reach'], errors='coerce').fillna(0)
    df['Impressions'] = pd.to_numeric(df['Impressions'], errors='coerce').fillna(0)

    post_aug = df[df['Month'].astype(str).str.contains('2026-09|2026-10|2026-11', na=False) & (df['Campaign'].astype(str).str.strip() != '')].copy()

    print("================================================================================")
    print("DETAILED CAMPAIGN BREAKDOWN (SEPTEMBER 1 - NOVEMBER 17, 2026)")
    print("================================================================================")
    
    for c in post_aug['Campaign'].unique():
        c_df = post_aug[post_aug['Campaign'] == c]
        tot_spend = c_df['Amount_Spent'].sum()
        tot_pur = c_df['Purchases'].sum()
        tot_val = c_df['Conv_Value'].sum()
        tot_reach = c_df['Reach'].sum()
        tot_imp = c_df['Impressions'].sum()
        cpa = tot_spend / tot_pur if tot_pur > 0 else 0
        roas = tot_val / tot_spend if tot_spend > 0 else 0
        cpm = (tot_spend / tot_imp) * 1000 if tot_imp > 0 else 0
        freq = tot_imp / tot_reach if tot_reach > 0 else 0
        
        print(f"\nCAMPAIGN: {c}")
        print(f"  Overall: Spend: Rs {tot_spend:,.2f} | Purchases: {tot_pur:,.0f} | CPA: Rs {cpa:.2f} | ROAS: {roas:.2f}x | Rev: Rs {tot_val:,.2f}")
        print(f"  Delivery: Impressions: {tot_imp:,.0f} | Reach: {tot_reach:,.0f} | CPM: Rs {cpm:.2f} | Frequency: {freq:.2f}")
        print("  Monthly Breakdown:")
        for idx, row in c_df.iterrows():
            m_cpa = row['Amount_Spent'] / row['Purchases'] if row['Purchases'] > 0 else 0
            m_roas = row['Conv_Value'] / row['Amount_Spent'] if row['Amount_Spent'] > 0 else 0
            m_cpm = (row['Amount_Spent'] / row['Impressions']) * 1000 if row['Impressions'] > 0 else 0
            m_freq = row['Impressions'] / row['Reach'] if row['Reach'] > 0 else 0
            print(f"    - {row['Month']}: Spend: Rs {row['Amount_Spent']:,.2f} | Orders: {int(row['Purchases'])} | CPA: Rs {m_cpa:.2f} | ROAS: {m_roas:.2f}x | CPM: Rs {m_cpm:.2f} | Freq: {m_freq:.2f}")

    print("\n================================================================================")
    print("TOTAL COMPETITOR AGENCY RUN (SEP 1 - NOV 17, 2026 COMBINED)")
    print("================================================================================")
    comp_spend = post_aug['Amount_Spent'].sum()
    comp_pur = post_aug['Purchases'].sum()
    comp_val = post_aug['Conv_Value'].sum()
    comp_imp = post_aug['Impressions'].sum()
    comp_reach = post_aug['Reach'].sum()
    print(f"Total Ad Spend: Rs {comp_spend:,.2f}")
    print(f"Total Purchases: {comp_pur:,.0f}")
    print(f"Total Reported Revenue: Rs {comp_val:,.2f}")
    print(f"Blended Competitor CPA: Rs {comp_spend / comp_pur:.2f}")
    print(f"Blended Competitor ROAS: {comp_val / comp_spend:.2f}x")
    print(f"Blended AOV: Rs {comp_val / comp_pur:.2f}")
    print(f"Total Impressions: {comp_imp:,.0f} | Total Reach: {comp_reach:,.0f}")

    print("\n================================================================================")
    print("COMPARISON: COMPETITOR ACTUALS vs TECHNO EXPONENT FORECAST (SEP - NOV)")
    print("================================================================================")
    # Plan B was:
    # Sept: Spend 45L, Sales 1.717 Cr, CPA 308, ROAS 3.82x (Meta portion: Spend ~17.5L, Sales ~68.6L)
    # Oct: Spend 52L, Sales 2.258 Cr, CPA 287, ROAS 4.34x (Meta portion: Spend ~22L, Sales ~91.7L, CPA ~₹260-280)
    # Nov: Spend 60L, Sales 2.786 Cr, CPA 278, ROAS 4.64x (Meta portion: Spend ~26L, Sales ~111.6L, CPA ~₹250-270)
    
if __name__ == '__main__':
    run_deep_audit()
