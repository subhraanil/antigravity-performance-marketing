import pandas as pd

# Define the models
models = {
    "1. Optimized Standard Plan (Maintain Current ~Rs 9,200/day Budget)": {
        "German-Mumbai": {"budget": 2200, "target_cpa": 580, "current_spend": 1804, "current_leads": 2.63, "current_cpa": 685},
        "German-Pune": {"budget": 1800, "target_cpa": 720, "current_spend": 1471, "current_leads": 1.73, "current_cpa": 849},
        "German-Bangalore": {"budget": 1600, "target_cpa": 650, "current_spend": 1203, "current_leads": 1.37, "current_cpa": 880},
        "German-Hydrabad": {"budget": 1600, "target_cpa": 680, "current_spend": 1574, "current_leads": 1.43, "current_cpa": 1098},
        "French-Mumbai": {"budget": 1200, "target_cpa": 780, "current_spend": 1757, "current_leads": 1.43, "current_cpa": 1226},
        "French-Bangalore": {"budget": 800, "target_cpa": 850, "current_spend": 1323, "current_leads": 1.00, "current_cpa": 1323},
    },
    "2. High Efficiency Plan (Lean Spend ~Rs 7,500/day)": {
        "German-Mumbai": {"budget": 2000, "target_cpa": 580},
        "German-Pune": {"budget": 1500, "target_cpa": 720},
        "German-Bangalore": {"budget": 1400, "target_cpa": 650},
        "German-Hydrabad": {"budget": 1300, "target_cpa": 680},
        "French-Mumbai": {"budget": 800, "target_cpa": 780},
        "French-Bangalore": {"budget": 500, "target_cpa": 850},
    },
    "3. Aggressive Scale Plan (~Rs 12,000/day)": {
        "German-Mumbai": {"budget": 3000, "target_cpa": 600},
        "German-Pune": {"budget": 2400, "target_cpa": 750},
        "German-Bangalore": {"budget": 2200, "target_cpa": 680},
        "German-Hydrabad": {"budget": 2200, "target_cpa": 700},
        "French-Mumbai": {"budget": 1400, "target_cpa": 800},
        "French-Bangalore": {"budget": 800, "target_cpa": 850},
    }
}

for title, camps in models.items():
    print("=" * 75)
    print(title)
    print("=" * 75)
    tot_b = sum(v["budget"] for v in camps.values())
    tot_leads_d = sum(v["budget"] / v["target_cpa"] for v in camps.values())
    blended_cpa = tot_b / tot_leads_d
    print(f"Total Daily Spend:  Rs. {tot_b:,.0f}/day  (Rs. {tot_b*30:,.0f}/month)")
    print(f"Target Daily Leads: {tot_leads_d:.1f} leads/day ({tot_leads_d*30:.0f} leads/month)")
    print(f"Blended Target CPA: Rs. {blended_cpa:.2f}")
    print("-" * 75)
    print(f"{'Campaign':<18} | {'Daily Budget':<12} | {'Monthly Budget':<14} | {'Target CPA':<10} | {'Daily Leads':<11} | {'Monthly Leads'}")
    print("-" * 75)
    for cname, v in camps.items():
        d_leads = v["budget"] / v["target_cpa"]
        m_leads = d_leads * 30
        print(f"{cname:<18} | Rs. {v['budget']:<8} | Rs. {v['budget']*30:<10,.0f} | Rs. {v['target_cpa']:<6} | {d_leads:<11.1f} | {m_leads:.0f} leads")
    print("\n")
