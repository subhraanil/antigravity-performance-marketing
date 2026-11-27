import os
import openpyxl
import pandas as pd
import numpy as np

folder = r"C:\Users\test\Videos\Office\data\fabb6\November"
file_path = os.path.join(folder, "Historic Data and Forecast - 18 Nov 2026.xlsx")

def run_forecast_comparison():
    wb = openpyxl.load_workbook(file_path, data_only=True)
    
    # 1. Extract Actuals from 'Historic Data' sheet
    sheet_hist = wb['Historic Data']
    actuals = {
        'Sep 2026': {
            'Shopify_Orders': float(sheet_hist.cell(12, 2).value or 0),
            'Gross_Sales': float(sheet_hist.cell(12, 3).value or 0),
            'Net_Revenue': float(sheet_hist.cell(12, 5).value or 0),
            'Total_Paid_Spend': float(sheet_hist.cell(12, 6).value or 0),
            'Paid_Purchases': float(sheet_hist.cell(12, 14).value or 0),
            'Blended_CPA': float(sheet_hist.cell(12, 17).value or 0),
            'Blended_ROAS': float(sheet_hist.cell(12, 18).value or 0),
            'Google_Spend': float(sheet_hist.cell(28, 4).value or 0),
            'Google_Orders': float(sheet_hist.cell(28, 2).value or 0),
            'Google_CPA': float(sheet_hist.cell(28, 5).value or 0),
            'Meta_Spend': float(sheet_hist.cell(43, 4).value or 0),
            'Meta_Orders': float(sheet_hist.cell(43, 2).value or 0),
            'Meta_CPA': float(sheet_hist.cell(43, 5).value or 0),
            'Returning_Rate': float(sheet_hist.cell(12, 7).value or 0)
        },
        'Oct 2026': {
            'Shopify_Orders': float(sheet_hist.cell(13, 2).value or 0),
            'Gross_Sales': float(sheet_hist.cell(13, 3).value or 0),
            'Net_Revenue': float(sheet_hist.cell(13, 5).value or 0),
            'Total_Paid_Spend': float(sheet_hist.cell(13, 6).value or 0),
            'Paid_Purchases': float(sheet_hist.cell(13, 14).value or 0),
            'Blended_CPA': float(sheet_hist.cell(13, 17).value or 0),
            'Blended_ROAS': float(sheet_hist.cell(13, 18).value or 0),
            'Google_Spend': float(sheet_hist.cell(29, 4).value or 0),
            'Google_Orders': float(sheet_hist.cell(29, 2).value or 0),
            'Google_CPA': float(sheet_hist.cell(29, 5).value or 0),
            'Meta_Spend': float(sheet_hist.cell(44, 4).value or 0),
            'Meta_Orders': float(sheet_hist.cell(44, 2).value or 0),
            'Meta_CPA': float(sheet_hist.cell(44, 5).value or 0),
            'Returning_Rate': float(sheet_hist.cell(13, 7).value or 0)
        },
        'Nov 2026 (18 Days)': {
            'Shopify_Orders': float(sheet_hist.cell(14, 2).value or 0),
            'Gross_Sales': float(sheet_hist.cell(14, 3).value or 0),
            'Net_Revenue': float(sheet_hist.cell(14, 5).value or 0),
            'Total_Paid_Spend': float(sheet_hist.cell(14, 6).value or 0),
            'Paid_Purchases': float(sheet_hist.cell(14, 14).value or 0),
            'Blended_CPA': float(sheet_hist.cell(14, 17).value or 0),
            'Blended_ROAS': float(sheet_hist.cell(14, 18).value or 0),
            'Google_Spend': float(sheet_hist.cell(30, 4).value or 0),
            'Google_Orders': float(sheet_hist.cell(30, 2).value or 0),
            'Google_CPA': float(sheet_hist.cell(30, 5).value or 0),
            'Meta_Spend': float(sheet_hist.cell(45, 4).value or 0),
            'Meta_Orders': float(sheet_hist.cell(45, 2).value or 0),
            'Meta_CPA': float(sheet_hist.cell(45, 5).value or 0),
            'Returning_Rate': float(sheet_hist.cell(14, 7).value or 0)
        }
    }
    
    # 18-day pacing for November (multiply by 30/18 = 1.6667)
    actuals['Nov 2026 (Paced Full Month)'] = {
        'Shopify_Orders': actuals['Nov 2026 (18 Days)']['Shopify_Orders'] * (30/18),
        'Gross_Sales': actuals['Nov 2026 (18 Days)']['Gross_Sales'] * (30/18),
        'Net_Revenue': actuals['Nov 2026 (18 Days)']['Net_Revenue'] * (30/18),
        'Total_Paid_Spend': actuals['Nov 2026 (18 Days)']['Total_Paid_Spend'] * (30/18),
        'Paid_Purchases': actuals['Nov 2026 (18 Days)']['Paid_Purchases'] * (30/18),
        'Blended_CPA': actuals['Nov 2026 (18 Days)']['Blended_CPA'],
        'Blended_ROAS': actuals['Nov 2026 (18 Days)']['Blended_ROAS'],
        'Google_Spend': actuals['Nov 2026 (18 Days)']['Google_Spend'] * (30/18),
        'Google_Orders': actuals['Nov 2026 (18 Days)']['Google_Orders'] * (30/18),
        'Google_CPA': actuals['Nov 2026 (18 Days)']['Google_CPA'],
        'Meta_Spend': actuals['Nov 2026 (18 Days)']['Meta_Spend'] * (30/18),
        'Meta_Orders': actuals['Nov 2026 (18 Days)']['Meta_Orders'] * (30/18),
        'Meta_CPA': actuals['Nov 2026 (18 Days)']['Meta_CPA'],
        'Returning_Rate': actuals['Nov 2026 (18 Days)']['Returning_Rate']
    }

    # 2. Extract Forecasts for each Plan
    # Row 3 = Sep 2026, Row 4 = Oct 2026, Row 5 = Nov 2026
    # Shopify: Col 2 Total Orders, Col 3 Gross Sales, Col 4 Ads Spend, Col 5 Paid Orders, Col 6 Others, Col 7 AOV, Col 8 ROAS, Col 9 Blended CPA (or Daily)
    plans = {}
    plan_names = ['Plan - A (normal Growth)', 'Plan - C (30Lbudget)', 'Plan - C.1 (30Lbudget)', 'Plan - B (1500day order)']
    
    for p in plan_names:
        sheet = wb[p]
        p_dict = {}
        for r_idx, m_name in [(3, 'Sep 2026'), (4, 'Oct 2026'), (5, 'Nov 2026')]:
            # Shopify block
            tot_orders = float(sheet.cell(r_idx, 2).value or 0)
            gross_sales = float(sheet.cell(r_idx, 3).value or 0)
            ad_spend = float(sheet.cell(r_idx, 4).value or 0)
            paid_orders = float(sheet.cell(r_idx, 5).value or 0)
            others_orders = float(sheet.cell(r_idx, 6).value or 0)
            aov = float(sheet.cell(r_idx, 7).value or 0)
            roas = float(sheet.cell(r_idx, 8).value or 0)
            cpa = float(sheet.cell(r_idx, 9).value or 0)
            if 'Plan - B' in p:
                # In Plan B: Col 9 is Daily Avg Orders, Col 10 is Blended CPA
                cpa = float(sheet.cell(r_idx, 10).value or 0)
            
            # Google block (Rows 21, 22, 23)
            g_r = r_idx + 18
            g_orders = float(sheet.cell(g_r, 2).value or 0)
            g_rev = float(sheet.cell(g_r, 3).value or 0)
            g_budget = float(sheet.cell(g_r, 4).value or 0)
            g_cpa = float(sheet.cell(g_r, 5).value or 0)
            g_roas = float(sheet.cell(g_r, 7).value or 0)

            # Meta block (Rows 30, 31, 32)
            m_r = r_idx + 27
            m_orders = float(sheet.cell(m_r, 2).value or 0)
            m_rev = float(sheet.cell(m_r, 3).value or 0)
            m_budget = float(sheet.cell(m_r, 4).value or 0)
            m_cpa = float(sheet.cell(m_r, 5).value or 0)
            m_roas = float(sheet.cell(m_r, 7).value or 0)

            p_dict[m_name] = {
                'Total_Orders': tot_orders,
                'Gross_Sales': gross_sales,
                'Total_Spend': ad_spend,
                'Paid_Orders': paid_orders,
                'Blended_CPA': cpa,
                'ROAS': roas,
                'Google_Budget': g_budget,
                'Google_Orders': g_orders,
                'Google_CPA': g_cpa,
                'Google_ROAS': g_roas,
                'Meta_Budget': m_budget,
                'Meta_Orders': m_orders,
                'Meta_CPA': m_cpa,
                'Meta_ROAS': m_roas
            }
        plans[p] = p_dict

    print("=" * 80)
    print("DETAILED COMPARISON: ACTUALS VS THE 4 FORECAST PLANS")
    print("=" * 80)

    # Let us print side-by-side comparison for September, October, November
    for m in ['Sep 2026', 'Oct 2026', 'Nov 2026']:
        act_key = m if m != 'Nov 2026' else 'Nov 2026 (Paced Full Month)'
        act = actuals[act_key]
        print(f"\n==================== {m.upper()} COMPARISON ====================")
        if m == 'Nov 2026':
            print("*(Note: November Actual is paced to 30 days based on first 18 days actuals)*")
        print(f"{'Metric':<25} | {'Actual':<14} | {'Plan A':<14} | {'Plan C (30L)':<14} | {'Plan C.1':<14} | {'Plan B (1500)':<14}")
        print("-" * 105)
        
        metrics = [
            ('Shopify Total Orders', act['Shopify_Orders'], [plans[p][m]['Total_Orders'] for p in plan_names], "{:,.0f}"),
            ('Gross Sales (₹)', act['Gross_Sales'], [plans[p][m]['Gross_Sales'] for p in plan_names], "₹{:,.0f}"),
            ('Total Paid Spend (₹)', act['Total_Paid_Spend'], [plans[p][m]['Total_Spend'] for p in plan_names], "₹{:,.0f}"),
            ('Paid Purchases', act['Paid_Purchases'], [plans[p][m]['Paid_Orders'] for p in plan_names], "{:,.0f}"),
            ('Blended Paid CPA (₹)', act['Blended_CPA'], [plans[p][m]['Blended_CPA'] for p in plan_names], "₹{:.2f}"),
            ('ROAS', act['Blended_ROAS'], [plans[p][m]['ROAS'] for p in plan_names], "{:.2f}x"),
            ('Google Spend (₹)', act['Google_Spend'], [plans[p][m]['Google_Budget'] for p in plan_names], "₹{:,.0f}"),
            ('Google Orders', act['Google_Orders'], [plans[p][m]['Google_Orders'] for p in plan_names], "{:,.0f}"),
            ('Google CPA (₹)', act['Google_CPA'], [plans[p][m]['Google_CPA'] for p in plan_names], "₹{:.2f}"),
            ('Meta Spend (₹)', act['Meta_Spend'], [plans[p][m]['Meta_Budget'] for p in plan_names], "₹{:,.0f}"),
            ('Meta Orders', act['Meta_Orders'], [plans[p][m]['Meta_Orders'] for p in plan_names], "{:,.0f}"),
            ('Meta CPA (₹)', act['Meta_CPA'], [plans[p][m]['Meta_CPA'] for p in plan_names], "₹{:.2f}")
        ]
        
        for name, act_v, f_vals, fmt in metrics:
            f_strs = [fmt.format(fv) for fv in f_vals]
            print(f"{name:<25} | {fmt.format(act_v):<14} | {f_strs[0]:<14} | {f_strs[1]:<14} | {f_strs[2]:<14} | {f_strs[3]:<14}")

    # Accuracy Calculation
    print("\n" + "=" * 80)
    print("ACCURACY ANALYSIS (% VARIANCE = (ACTUAL - FORECAST) / FORECAST)")
    print("=" * 80)
    for p in plan_names:
        print(f"\n--- {p} ---")
        for m in ['Sep 2026', 'Oct 2026', 'Nov 2026']:
            act_key = m if m != 'Nov 2026' else 'Nov 2026 (Paced Full Month)'
            act = actuals[act_key]
            f = plans[p][m]
            
            spend_var = (act['Total_Paid_Spend'] - f['Total_Spend']) / f['Total_Spend'] * 100
            order_var = (act['Shopify_Orders'] - f['Total_Orders']) / f['Total_Orders'] * 100
            paid_order_var = (act['Paid_Purchases'] - f['Paid_Orders']) / f['Paid_Orders'] * 100
            cpa_var = (act['Blended_CPA'] - f['Blended_CPA']) / f['Blended_CPA'] * 100
            roas_var = (act['Blended_ROAS'] - f['ROAS']) / f['ROAS'] * 100
            
            print(f"[{m}] Spend Variance: {spend_var:+.1f}% | Total Orders Variance: {order_var:+.1f}% | Paid Orders: {paid_order_var:+.1f}% | CPA Variance: {cpa_var:+.1f}% | ROAS Variance: {roas_var:+.1f}%")

if __name__ == '__main__':
    run_forecast_comparison()
