# Script to audit the 3 forecast plans provided by the user

plans_data = {
    "Plan 1 (Base / Recommended - Spend: 30L / 35L / 40L = 105L Total)": {
        "months": [
            {
                "month": "2026-12",
                "shopify": {
                    "orders": 8804.545455,
                    "gross_sale": 11525150.0,
                    "spend": 3000000.0,
                    "blended_cpa": 340.7330924,
                    "aov": 1309.0,
                    "roas": 3.841716667,
                    "paid_orders": 5454.545455,
                    "organic": 1650.0,
                    "others": 1700.0
                },
                "total_paid": {
                    "purchase": 5454.545455,
                    "gross_sale": 7140000.0,
                    "spend": 3000000.0,
                    "cpa": 550.0,
                    "aov": 1309.0,
                    "roas": 2.38
                },
                "google": {
                    "orders": 3454.545455,
                    "gross_sale": 4522000.0,
                    "spend": 1900000.0,
                    "cpa": 550.0,
                    "aov": 1309.0,
                    "roas": 2.38
                },
                "meta": {
                    "orders": 2000.0,
                    "gross_sale": 2618000.0,
                    "spend": 1100000.0,
                    "cpa": 550.0,
                    "aov": 1309.0,
                    "roas": 2.38
                }
            },
            {
                "month": "2027-01",
                "shopify": {
                    "orders": 10186.66667,
                    "gross_sale": 14261333.33,
                    "spend": 3500000.0,
                    "blended_cpa": 343.5863874,
                    "aov": 1400.0,
                    "roas": 4.074666667,
                    "paid_orders": 6666.666667,
                    "organic": 1650.0,
                    "others": 1870.0
                },
                "total_paid": {
                    "purchase": 6666.666667,
                    "gross_sale": 9333333.333,
                    "spend": 3500000.0,
                    "cpa": 525.0,
                    "aov": 1400.0,
                    "roas": 2.666666667
                },
                "google": {
                    "orders": 4190.47619,
                    "gross_sale": 5866666.667,
                    "spend": 2200000.0,
                    "cpa": 525.0,
                    "aov": 1400.0,
                    "roas": 2.666666667
                },
                "meta": {
                    "orders": 2476.190476,
                    "gross_sale": 3466666.667,
                    "spend": 1300000.0,
                    "cpa": 525.0,
                    "aov": 1400.0,
                    "roas": 2.666666667
                }
            },
            {
                "month": "2027-02",
                "shopify": {
                    "orders": 11707.0,
                    "gross_sale": 17560500.0,
                    "spend": 4000000.0,
                    "blended_cpa": 341.6759204,
                    "aov": 1500.0,
                    "roas": 4.390125,
                    "paid_orders": 8000.0,
                    "organic": 1650.0,
                    "others": 2057.0
                },
                "total_paid": {
                    "purchase": 8000.0,
                    "gross_sale": 12000000.0,
                    "spend": 4000000.0,
                    "cpa": 500.0,
                    "aov": 1500.0,
                    "roas": 3.0
                },
                "google": {
                    "orders": 5000.0,
                    "gross_sale": 7500000.0,
                    "spend": 2500000.0,
                    "cpa": 500.0,
                    "aov": 1500.0,
                    "roas": 3.0
                },
                "meta": {
                    "orders": 3000.0,
                    "gross_sale": 4500000.0,
                    "spend": 1500000.0,
                    "cpa": 500.0,
                    "aov": 1500.0,
                    "roas": 3.0
                }
            }
        ]
    },
    "Plan 2 (Moderate - Spend: 35L / 41L / 46L = 122L Total)": {
        "months": [
            {
                "month": "2026-12",
                "shopify": {
                    "orders": 9713.636364,
                    "gross_sale": 12715150.0,
                    "spend": 3500000.0,
                    "blended_cpa": 360.3182031,
                    "aov": 1309.0,
                    "roas": 3.6329,
                    "paid_orders": 6363.636364,
                    "organic": 1650.0,
                    "others": 1700.0
                },
                "total_paid": {
                    "purchase": 6363.636364,
                    "gross_sale": 8330000.0,
                    "spend": 3500000.0,
                    "cpa": 550.0,
                    "aov": 1309.0,
                    "roas": 2.38
                },
                "google": {
                    "orders": 4000.0,
                    "gross_sale": 5236000.0,
                    "spend": 2200000.0,
                    "cpa": 550.0,
                    "aov": 1309.0,
                    "roas": 2.38
                },
                "meta": {
                    "orders": 2363.636364,
                    "gross_sale": 3094000.0,
                    "spend": 1300000.0,
                    "cpa": 550.0,
                    "aov": 1309.0,
                    "roas": 2.38
                }
            },
            {
                "month": "2027-01",
                "shopify": {
                    "orders": 11329.52381,
                    "gross_sale": 15861333.33,
                    "spend": 4100000.0,
                    "blended_cpa": 361.8863484,
                    "aov": 1400.0,
                    "roas": 3.868617886,
                    "paid_orders": 7809.52381,
                    "organic": 1650.0,
                    "others": 1870.0
                },
                "total_paid": {
                    "purchase": 7809.52381,
                    "gross_sale": 10933333.33,
                    "spend": 4100000.0,
                    "cpa": 525.0,
                    "aov": 1400.0,
                    "roas": 2.666666667
                },
                "google": {
                    "orders": 4952.380952,
                    "gross_sale": 6933333.333,
                    "spend": 2600000.0,
                    "cpa": 525.0,
                    "aov": 1400.0,
                    "roas": 2.666666667
                },
                "meta": {
                    "orders": 2857.142857,
                    "gross_sale": 4000000.0,
                    "spend": 1500000.0,
                    "cpa": 525.0,
                    "aov": 1400.0,
                    "roas": 2.666666667
                }
            },
            {
                "month": "2027-02",
                "shopify": {
                    "orders": 12907.0,
                    "gross_sale": 19360500.0,
                    "spend": 4600000.0,
                    "blended_cpa": 356.3957542,
                    "aov": 1500.0,
                    "roas": 4.208804348,
                    "paid_orders": 9200.0,
                    "organic": 1650.0,
                    "others": 2057.0
                },
                "total_paid": {
                    "purchase": 9200.0,
                    "gross_sale": 13800000.0,
                    "spend": 4600000.0,
                    "cpa": 500.0,
                    "aov": 1500.0,
                    "roas": 3.0
                },
                "google": {
                    "orders": 5800.0,
                    "gross_sale": 8700000.0,
                    "spend": 2900000.0,
                    "cpa": 500.0,
                    "aov": 1500.0,
                    "roas": 3.0
                },
                "meta": {
                    "orders": 3400.0,
                    "gross_sale": 5100000.0,
                    "spend": 1700000.0,
                    "cpa": 500.0,
                    "aov": 1500.0,
                    "roas": 3.0
                }
            }
        ]
    },
    "Plan 3 (Aggressive - Spend: 40L / 47L / 54L = 141L Total)": {
        "months": [
            {
                "month": "2026-12",
                "shopify": {
                    "orders": 10622.72727,
                    "gross_sale": 13905150.0,
                    "spend": 4000000.0,
                    "blended_cpa": 376.5511339,
                    "aov": 1309.0,
                    "roas": 3.4762875,
                    "paid_orders": 7272.727273,
                    "organic": 1650.0,
                    "others": 1700.0
                },
                "total_paid": {
                    "purchase": 7272.727273,
                    "gross_sale": 9520000.0,
                    "spend": 4000000.0,
                    "cpa": 550.0,
                    "aov": 1309.0,
                    "roas": 2.38
                },
                "google": {
                    "orders": 4545.454545,
                    "gross_sale": 5950000.0,
                    "spend": 2500000.0,
                    "cpa": 550.0,
                    "aov": 1309.0,
                    "roas": 2.38
                },
                "meta": {
                    "orders": 2727.272727,
                    "gross_sale": 3570000.0,
                    "spend": 1500000.0,
                    "cpa": 550.0,
                    "aov": 1309.0,
                    "roas": 2.38
                }
            },
            {
                "month": "2027-01",
                "shopify": {
                    "orders": 12472.38095,
                    "gross_sale": 17461333.33,
                    "spend": 4700000.0,
                    "blended_cpa": 376.8326206,
                    "aov": 1400.0,
                    "roas": 3.715177305,
                    "paid_orders": 8952.380952,
                    "organic": 1650.0,
                    "others": 1870.0
                },
                "total_paid": {
                    "purchase": 8952.380952,
                    "gross_sale": 12533333.33,
                    "spend": 4700000.0,
                    "cpa": 525.0,
                    "aov": 1400.0,
                    "roas": 2.666666667
                },
                "google": {
                    "orders": 5714.285714,
                    "gross_sale": 8000000.0,
                    "spend": 3000000.0,
                    "cpa": 525.0,
                    "aov": 1400.0,
                    "roas": 2.666666667
                },
                "meta": {
                    "orders": 3238.095238,
                    "gross_sale": 4533333.333,
                    "spend": 1700000.0,
                    "cpa": 525.0,
                    "aov": 1400.0,
                    "roas": 2.666666667
                }
            },
            {
                "month": "2027-02",
                "shopify": {
                    "orders": 14507.0,
                    "gross_sale": 21760500.0,
                    "spend": 5400000.0,
                    "blended_cpa": 372.2340939,
                    "aov": 1500.0,
                    "roas": 4.029722222,
                    "paid_orders": 10800.0,
                    "organic": 1650.0,
                    "others": 2057.0
                },
                "total_paid": {
                    "purchase": 10800.0,
                    "gross_sale": 16200000.0,
                    "spend": 5400000.0,
                    "cpa": 500.0,
                    "aov": 1500.0,
                    "roas": 3.0
                },
                "google": {
                    "orders": 6800.0,
                    "gross_sale": 10200000.0,
                    "spend": 3400000.0,
                    "cpa": 500.0,
                    "aov": 1500.0,
                    "roas": 3.0
                },
                "meta": {
                    "orders": 4000.0,
                    "gross_sale": 6000000.0,
                    "spend": 2000000.0,
                    "cpa": 500.0,
                    "aov": 1500.0,
                    "roas": 3.0
                }
            }
        ]
    }
}

print("=== FORENSIC ARITHMETIC AUDIT OF 3 PLANS ===")

for plan_name, pdata in plans_data.items():
    print(f"\n" + "="*80)
    print(f"AUDITING: {plan_name}")
    print("="*80)
    
    tot_spend = sum(m['shopify']['spend'] for m in pdata['months'])
    tot_rev = sum(m['shopify']['gross_sale'] for m in pdata['months'])
    tot_orders = sum(m['shopify']['orders'] for m in pdata['months'])
    tot_paid_orders = sum(m['total_paid']['purchase'] for m in pdata['months'])
    tot_paid_rev = sum(m['total_paid']['gross_sale'] for m in pdata['months'])
    tot_paid_spend = sum(m['total_paid']['spend'] for m in pdata['months'])
    
    print(f"3-Month Total Media Spend: ₹{tot_spend:,.2f} (₹{tot_spend/1e5:.2f}L)")
    print(f"3-Month Total Gross Revenue: ₹{tot_rev:,.2f} (₹{tot_rev/1e7:.2f} Cr)")
    print(f"3-Month Total Store Orders: {tot_orders:,.1f}")
    print(f"3-Month Blended Store ROAS: {tot_rev / tot_spend:.2f}x")
    print(f"3-Month Blended Store CPA: ₹{tot_spend / tot_orders:.2f}")
    print(f"3-Month Paid ROAS: {tot_paid_rev / tot_paid_spend:.2f}x")
    print(f"3-Month Paid CPA: ₹{tot_paid_spend / tot_paid_orders:.2f}")
    
    for m in pdata['months']:
        m_name = m['month']
        s = m['shopify']
        tp = m['total_paid']
        g = m['google']
        meta = m['meta']
        
        # 1. Order additivity: Paid + Organic + Others == Total Orders?
        calc_orders = s['paid_orders'] + s['organic'] + s['others']
        ord_diff = abs(calc_orders - s['orders'])
        
        # 2. Revenue calculation: Orders * AOV == Gross Sale?
        calc_rev = s['orders'] * s['aov']
        rev_diff = abs(calc_rev - s['gross_sale'])
        
        # 3. Blended CPA: Spend / Orders == Blended CPA?
        calc_blended_cpa = s['spend'] / s['orders']
        cpa_diff = abs(calc_blended_cpa - s['blended_cpa'])
        
        # 4. Store ROAS: Gross Sale / Spend == ROAS on Total?
        calc_roas = s['gross_sale'] / s['spend']
        roas_diff = abs(calc_roas - s['roas'])
        
        # 5. Paid Orders sum: Google + Meta == Total Paid Purchase?
        calc_paid_orders = g['orders'] + meta['orders']
        paid_ord_diff = abs(calc_paid_orders - tp['purchase'])
        
        # 6. Paid Spend sum: Google + Meta == Total Paid Spend?
        calc_paid_spend = g['spend'] + meta['spend']
        paid_spend_diff = abs(calc_paid_spend - tp['spend'])
        
        # 7. Paid Revenue: Total Paid Purchase * AOV == Total Paid Gross Sale?
        calc_paid_rev = tp['purchase'] * tp['aov']
        paid_rev_diff = abs(calc_paid_rev - tp['gross_sale'])
        
        # 8. Channel CPA: Google Spend / Google Orders == Google CPA?
        calc_gcpa = g['spend'] / g['orders']
        gcpa_diff = abs(calc_gcpa - g['cpa'])
        
        # 9. Channel CPA: Meta Spend / Meta Orders == Meta CPA?
        calc_mcpa = meta['spend'] / meta['orders']
        mcpa_diff = abs(calc_mcpa - meta['cpa'])
        
        print(f"\n--- Month {m_name} ---")
        print(f"  Shopify Orders: stated={s['orders']:.2f}, Paid({s['paid_orders']:.1f}) + Org({s['organic']}) + Oth({s['others']}) = {calc_orders:.2f} | Diff: {ord_diff:.4f}")
        print(f"  Shopify Revenue: stated=₹{s['gross_sale']:,.2f}, Orders * AOV = ₹{calc_rev:,.2f} | Diff: ₹{rev_diff:.2f}")
        print(f"  Blended CPA: stated=₹{s['blended_cpa']:.2f}, Spend/Orders = ₹{calc_blended_cpa:.2f} | Diff: ₹{cpa_diff:.4f}")
        print(f"  Store ROAS: stated={s['roas']:.4f}x, Rev/Spend = {calc_roas:.4f}x | Diff: {roas_diff:.6f}")
        print(f"  Paid Orders: stated={tp['purchase']:.2f}, Google({g['orders']:.2f}) + Meta({meta['orders']:.2f}) = {calc_paid_orders:.2f} | Diff: {paid_ord_diff:.4f}")
        print(f"  Paid Spend: stated=₹{tp['spend']:,.2f}, Google({g['spend']:,.2f}) + Meta({meta['spend']:,.2f}) = ₹{calc_paid_spend:,.2f} | Diff: ₹{paid_spend_diff:.2f}")
        print(f"  Paid Revenue: stated=₹{tp['gross_sale']:,.2f}, Paid Orders * AOV = ₹{calc_paid_rev:,.2f} | Diff: ₹{paid_rev_diff:.2f}")
        print(f"  Google CPA: stated=₹{g['cpa']:.2f}, Spend/Orders = ₹{calc_gcpa:.2f} | Diff: ₹{gcpa_diff:.4f}")
        print(f"  Meta CPA: stated=₹{meta['cpa']:.2f}, Spend/Orders = ₹{calc_mcpa:.2f} | Diff: ₹{mcpa_diff:.4f}")
        print(f"  Google Spend Share: {g['spend']/tp['spend']*100:.1f}%, Meta Spend Share: {meta['spend']/tp['spend']*100:.1f}%")
