# Generate comprehensive comparison table for the 3 plans

plans = [
    {
        "name": "Plan 1: Base / Recommended",
        "spend_m": [30.0, 35.0, 40.0],
        "google_spend": [19.0, 22.0, 25.0],
        "meta_spend": [11.0, 13.0, 15.0],
        "paid_orders": [5454.55, 6666.67, 8000.00],
        "paid_rev": [71.40, 93.33, 120.00],
        "organic_orders": [1650, 1650, 1650],
        "other_orders": [1700, 1870, 2057],
        "store_orders": [8804.55, 10186.67, 11707.00],
        "store_rev": [115.25, 142.61, 175.61],
        "aov": [1309, 1400, 1500],
        "paid_cpa": [550, 525, 500],
        "blended_cpa": [340.73, 343.59, 341.68],
        "paid_roas": [2.38, 2.67, 3.00],
        "store_roas": [3.84, 4.07, 4.39]
    },
    {
        "name": "Plan 2: Moderate",
        "spend_m": [35.0, 41.0, 46.0],
        "google_spend": [22.0, 26.0, 29.0],
        "meta_spend": [13.0, 15.0, 17.0],
        "paid_orders": [6363.64, 7809.52, 9200.00],
        "paid_rev": [83.30, 109.33, 138.00],
        "organic_orders": [1650, 1650, 1650],
        "other_orders": [1700, 1870, 2057],
        "store_orders": [9713.64, 11329.52, 12907.00],
        "store_rev": [127.15, 158.61, 193.61],
        "aov": [1309, 1400, 1500],
        "paid_cpa": [550, 525, 500],
        "blended_cpa": [360.32, 361.89, 356.40],
        "paid_roas": [2.38, 2.67, 3.00],
        "store_roas": [3.63, 3.87, 4.21]
    },
    {
        "name": "Plan 3: Aggressive",
        "spend_m": [40.0, 47.0, 54.0],
        "google_spend": [25.0, 30.0, 34.0],
        "meta_spend": [15.0, 17.0, 20.0],
        "paid_orders": [7272.73, 8952.38, 10800.00],
        "paid_rev": [95.20, 125.33, 162.00],
        "organic_orders": [1650, 1650, 1650],
        "other_orders": [1700, 1870, 2057],
        "store_orders": [10622.73, 12472.38, 14507.00],
        "store_rev": [139.05, 174.61, 217.61],
        "aov": [1309, 1400, 1500],
        "paid_cpa": [550, 525, 500],
        "blended_cpa": [376.55, 376.83, 372.23],
        "paid_roas": [2.38, 2.67, 3.00],
        "store_roas": [3.48, 3.72, 4.03]
    }
]

print("=== 3-MONTH AGGREGATE SUMMARY BY PLAN ===")
for p in plans:
    tot_spend = sum(p['spend_m'])
    tot_g_spend = sum(p['google_spend'])
    tot_m_spend = sum(p['meta_spend'])
    tot_paid_ord = sum(p['paid_orders'])
    tot_paid_rev = sum(p['paid_rev'])
    tot_store_ord = sum(p['store_orders'])
    tot_store_rev = sum(p['store_rev'])
    blended_cpa = (tot_spend * 1e5) / tot_store_ord
    blended_roas = tot_store_rev / tot_spend
    paid_cpa = (tot_spend * 1e5) / tot_paid_ord
    paid_roas = tot_paid_rev / tot_spend
    
    print(f"\n{p['name']}:")
    print(f"  Total Spend: ₹{tot_spend:.2f}L (Google: ₹{tot_g_spend:.2f}L [{tot_g_spend/tot_spend*100:.1f}%], Meta: ₹{tot_m_spend:.2f}L [{tot_m_spend/tot_spend*100:.1f}%])")
    print(f"  Paid Orders: {tot_paid_ord:,.0f} | Paid Revenue: ₹{tot_paid_rev:.2f}L (₹{tot_paid_rev/100:.2f} Cr) | Paid CPA: ₹{paid_cpa:.2f} | Paid ROAS: {paid_roas:.2f}x")
    print(f"  Non-Paid Orders (Org + Retention): {sum(p['organic_orders']) + sum(p['other_orders']):,d} orders ({sum(p['organic_orders']):,d} Org + {sum(p['other_orders']):,d} Others)")
    print(f"  Total Store Orders: {tot_store_ord:,.0f} | Gross Sales Revenue: ₹{tot_store_rev:.2f}L (₹{tot_store_rev/100:.2f} Cr)")
    print(f"  Blended Store CPA: ₹{blended_cpa:.2f} | Blended Store ROAS: {blended_roas:.2f}x")

print("\n=== MARGINAL SCALING EFFICIENCY (DELTA ANALYSIS) ===")
# Delta Plan 1 -> Plan 2
d_spend_1_2 = sum(plans[1]['spend_m']) - sum(plans[0]['spend_m'])
d_rev_1_2 = sum(plans[1]['store_rev']) - sum(plans[0]['store_rev'])
d_ord_1_2 = sum(plans[1]['store_orders']) - sum(plans[0]['store_orders'])
m_roas_1_2 = d_rev_1_2 / d_spend_1_2
m_cpa_1_2 = (d_spend_1_2 * 1e5) / d_ord_1_2
print(f"Plan 1 → Plan 2:")
print(f"  Incremental Spend: +₹{d_spend_1_2:.2f}L (+{d_spend_1_2/sum(plans[0]['spend_m'])*100:.1f}%)")
print(f"  Incremental Revenue: +₹{d_rev_1_2:.2f}L (+₹{d_rev_1_2/100:.2f} Cr, +{d_rev_1_2/sum(plans[0]['store_rev'])*100:.1f}%)")
print(f"  Incremental Store Orders: +{d_ord_1_2:,.0f} orders (+{d_ord_1_2/sum(plans[0]['store_orders'])*100:.1f}%)")
print(f"  Marginal ROAS: {m_roas_1_2:.2f}x | Marginal CPA: ₹{m_cpa_1_2:.2f}")

# Delta Plan 2 -> Plan 3
d_spend_2_3 = sum(plans[2]['spend_m']) - sum(plans[1]['spend_m'])
d_rev_2_3 = sum(plans[2]['store_rev']) - sum(plans[1]['store_rev'])
d_ord_2_3 = sum(plans[2]['store_orders']) - sum(plans[1]['store_orders'])
m_roas_2_3 = d_rev_2_3 / d_spend_2_3
m_cpa_2_3 = (d_spend_2_3 * 1e5) / d_ord_2_3
print(f"\nPlan 2 → Plan 3:")
print(f"  Incremental Spend: +₹{d_spend_2_3:.2f}L (+{d_spend_2_3/sum(plans[1]['spend_m'])*100:.1f}%)")
print(f"  Incremental Revenue: +₹{d_rev_2_3:.2f}L (+₹{d_rev_2_3/100:.2f} Cr, +{d_rev_2_3/sum(plans[1]['store_rev'])*100:.1f}%)")
print(f"  Incremental Store Orders: +{d_ord_2_3:,.0f} orders (+{d_ord_2_3/sum(plans[1]['store_orders'])*100:.1f}%)")
print(f"  Marginal ROAS: {m_roas_2_3:.2f}x | Marginal CPA: ₹{m_cpa_2_3:.2f}")
