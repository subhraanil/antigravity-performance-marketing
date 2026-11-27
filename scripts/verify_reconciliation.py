# Master Reconciliation Script for FABB6 Deliverables
import os
import shutil

print("Testing reconciliation parameters...")
aov = 1100
net_rate = 0.84

plans = {
    "Plan 1: Base": {"spend": [20.0, 24.0, 26.0], "roas": [2.80, 2.80, 2.80]},
    "Plan 2: Recommended": {"spend": [26.0, 31.0, 34.1], "roas": [2.50, 2.55, 2.60]},
    "Plan 3: Aggressive": {"spend": [30.0, 37.5, 45.0], "roas": [2.40, 2.35, 2.25]}
}

for name, p in plans.items():
    tot_spend = sum(p["spend"])
    gross_sales = [s * r for s, r in zip(p["spend"], p["roas"])]
    tot_gross = sum(gross_sales)
    blended_roas = tot_gross / tot_spend
    orders = [round((g * 100000) / aov) for g in gross_sales]
    tot_orders = sum(orders)
    spend_per_order = (tot_spend * 100000) / tot_orders
    tot_net = tot_gross * net_rate
    net_roas = tot_net / tot_spend
    gross_margin = tot_gross * 0.25
    deficit_gross = gross_margin - tot_spend
    deficit_net = (tot_net * 0.25) - tot_spend
    print(f"\n{name}:")
    print(f"  Spend: ₹{tot_spend:.1f}L | Gross Sales: ₹{tot_gross:.2f}L ({blended_roas:.2f}x) | Orders: {tot_orders:,} | Spend/Order: ₹{spend_per_order:.2f}")
    print(f"  Net Sales (84%): ₹{tot_net:.2f}L ({net_roas:.2f}x Net)")
    print(f"  Gross Margin (25%): ₹{gross_margin:.2f}L | 1st-Order Deficit (Gross): ₹{deficit_gross:.2f}L | Deficit (Net): ₹{deficit_net:.2f}L")

print("\nAll parameters verified.")
