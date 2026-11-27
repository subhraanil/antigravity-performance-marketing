# Contribution Analysis at 25% Gross Product Margin
# Gross Sales -> 25% Margin -> Spend -> First-Order Media Contribution -> Net Sales (at 84% realization)

plans = [
    ('Plan 1: Base', 70.0, 196.0, 2.80, 17818),
    ('Plan 2: Recommended', 91.1, 232.71, 2.554, 21155),
    ('Plan 3: Aggressive', 112.5, 261.375, 2.323, 23761),
]

print(f"{'Plan':<22} | {'Spend':<8} | {'Gross':<8} | {'ROAS':<6} | {'Margin (25%)':<12} | {'1st-Order Gap':<15} | {'Net Sales (84%)':<16} | {'Net ROAS':<8}")
print('-'*115)
for name, spend, gross, roas, orders in plans:
    margin = gross * 0.25
    deficit = margin - spend
    net_sales = gross * 0.84
    net_roas = net_sales / spend
    print(f"{name:<22} | ₹{spend:>5.1f}L | ₹{gross:>5.1f}L | {roas:>5.2f}x | ₹{margin:>10.2f}L | ₹{deficit:>13.2f}L | ₹{net_sales:>14.2f}L | {net_roas:>7.2f}x")

# Marginal analysis
print('\nMarginal Transitions:')
inc_spend_1_2 = 91.1 - 70.0
inc_gross_1_2 = 232.71 - 196.0
inc_margin_1_2 = inc_gross_1_2 * 0.25
inc_orders_1_2 = 21155 - 17818
marginal_roas_1_2 = inc_gross_1_2 / inc_spend_1_2
cost_per_inc_order_1_2 = (inc_spend_1_2 * 100000) / inc_orders_1_2

inc_spend_2_3 = 112.5 - 91.1
inc_gross_2_3 = 261.375 - 232.71
inc_margin_2_3 = inc_gross_2_3 * 0.25
inc_orders_2_3 = 23761 - 21155
marginal_roas_2_3 = inc_gross_2_3 / inc_spend_2_3
cost_per_inc_order_2_3 = (inc_spend_2_3 * 100000) / inc_orders_2_3

print(f"Plan 1 -> 2: +₹{inc_spend_1_2:.1f}L spend -> +₹{inc_gross_1_2:.2f}L gross ({marginal_roas_1_2:.2f}x) | +{inc_orders_1_2} orders @ ₹{cost_per_inc_order_1_2:.0f}/order | Inc Margin: ₹{inc_margin_1_2:.2f}L (Media Gap: ₹{inc_margin_1_2 - inc_spend_1_2:.2f}L)")
print(f"Plan 2 -> 3: +₹{inc_spend_2_3:.1f}L spend -> +₹{inc_gross_2_3:.2f}L gross ({marginal_roas_2_3:.2f}x) | +{inc_orders_2_3} orders @ ₹{cost_per_inc_order_2_3:.0f}/order | Inc Margin: ₹{inc_margin_2_3:.2f}L (Media Gap: ₹{inc_margin_2_3 - inc_spend_2_3:.2f}L)")
