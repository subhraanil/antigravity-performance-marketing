import os
import pandas as pd
import numpy as np
import openpyxl

folder = r"C:\Users\test\Videos\Office\data\fabb6\November"
csv_path = os.path.join(folder, "FABB6-Campaigns-1-Aug-2026-18-Nov-2026.csv")

def run_meta_deep_dive():
    df = pd.read_csv(csv_path)
    print("Meta CSV Rows:", len(df))
    print("Meta CSV Columns:", df.columns.tolist())

    num_cols = [
        'Amount spent (INR)', 'Results', 'Impressions', 'Reach', 'Frequency', 
        'Link clicks', 'Clicks (all)', 'Landing page views', 'CPM (cost per 1,000 impressions) (INR)',
        'CPC (cost per link click) (INR)', 'CTR (link click-through rate)'
    ]
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

    # Let's inspect by period (Aug vs Sep vs Oct vs Nov)
    print("\n" + "="*80)
    print("META ADS MONTH-BY-MONTH SUMMARY (AUG 1 - NOV 18, 2026)")
    print("="*80)
    
    # Filter periods
    periods = df[['Reporting starts', 'Reporting ends']].drop_duplicates().sort_values(by='Reporting starts')
    for idx, p in periods.iterrows():
        p_df = df[(df['Reporting starts'] == p['Reporting starts']) & (df['Reporting ends'] == p['Reporting ends'])]
        tot_spend = p_df['Amount spent (INR)'].sum()
        tot_res = p_df['Results'].sum()
        tot_imp = p_df['Impressions'].sum()
        tot_reach = p_df['Reach'].sum()
        tot_clicks = p_df['Link clicks'].sum()
        tot_lpv = p_df['Landing page views'].sum()
        
        cpa = tot_spend / tot_res if tot_res > 0 else 0
        cpm = (tot_spend / tot_imp) * 1000 if tot_imp > 0 else 0
        cpc = tot_spend / tot_clicks if tot_clicks > 0 else 0
        ctr = (tot_clicks / tot_imp) * 100 if tot_imp > 0 else 0
        freq = tot_imp / tot_reach if tot_reach > 0 else 0
        lpv_loss = ((tot_clicks - tot_lpv) / tot_clicks) * 100 if tot_clicks > 0 else 0
        
        print(f"\nPeriod: {p['Reporting starts']} to {p['Reporting ends']}")
        print(f"  Spend: Rs {tot_spend:,.2f} | Results: {tot_res:,.0f} | CPA: Rs {cpa:.2f}")
        print(f"  Delivery: Impressions: {tot_imp:,.0f} | Reach: {tot_reach:,.0f} | Freq: {freq:.2f} | CPM: Rs {cpm:.2f}")
        print(f"  Engagement: Link Clicks: {tot_clicks:,.0f} | CPC: Rs {cpc:.2f} | CTR: {ctr:.2f}% | LPV: {tot_lpv:,.0f} | LPV Drop-off: {lpv_loss:.1f}%")

    # Granular breakdown for Sep, Oct, Nov campaigns
    print("\n" + "="*80)
    print("CAMPAIGN-BY-CAMPAIGN BREAKDOWN DURING COMPETITOR TENURE (SEP - NOV 2026)")
    print("="*80)
    post_aug = df[df['Reporting starts'].astype(str) >= '2026-09-01'].copy()
    
    camp_summary = post_aug.groupby('Campaign name').agg({
        'Amount spent (INR)': 'sum',
        'Results': 'sum',
        'Impressions': 'sum',
        'Reach': 'sum',
        'Link clicks': 'sum',
        'Landing page views': 'sum'
    }).reset_index()

    camp_summary['CPA'] = camp_summary['Amount spent (INR)'] / camp_summary['Results'].replace(0, np.nan)
    camp_summary['CPM'] = (camp_summary['Amount spent (INR)'] / camp_summary['Impressions'].replace(0, np.nan)) * 1000
    camp_summary['CPC'] = camp_summary['Amount spent (INR)'] / camp_summary['Link clicks'].replace(0, np.nan)
    camp_summary['CTR'] = (camp_summary['Link clicks'] / camp_summary['Impressions'].replace(0, np.nan)) * 100
    camp_summary['Frequency'] = camp_summary['Impressions'] / camp_summary['Reach'].replace(0, np.nan)
    camp_summary['LPV_Dropoff'] = ((camp_summary['Link clicks'] - camp_summary['Landing page views']) / camp_summary['Link clicks'].replace(0, np.nan)) * 100

    camp_summary = camp_summary[camp_summary['Amount spent (INR)'] > 0].sort_values(by='Amount spent (INR)', ascending=False)
    
    for idx, r in camp_summary.iterrows():
        cpa_str = f"Rs {r['CPA']:.2f}" if not pd.isna(r['CPA']) else "0 Conversions (Waste)"
        print(f"\n[Campaign: {r['Campaign name']}]")
        print(f"   Spend: Rs {r['Amount spent (INR)']:,.2f} ({r['Amount spent (INR)']/post_aug['Amount spent (INR)'].sum()*100:.1f}% of total spend)")
        print(f"   Results: {r['Results']:,.0f} | CPA: {cpa_str}")
        print(f"   Delivery: CPM: Rs {r['CPM']:.2f} | Reach: {r['Reach']:,.0f} | Impressions: {r['Impressions']:,.0f} | Frequency: {r['Frequency']:.2f}")
        print(f"   Traffic: Link Clicks: {r['Link clicks']:,.0f} | CPC: Rs {r['CPC']:.2f} | CTR: {r['CTR']:.2f}% | LPV: {r['Landing page views']:,.0f} | Drop-off: {r['LPV_Dropoff']:.1f}%")

if __name__ == '__main__':
    run_meta_deep_dive()
