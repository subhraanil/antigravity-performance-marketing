with open(r"C:\Users\test\Videos\Office\scripts\build_perfect_report.py", "r", encoding="utf-8") as f:
    text = f.read()

target = 'add_body(" on a planned ad spend of ₹91.1 Lakhs, the forecast delivers about ₹3.56 Cr of Total Sales Revenue (3.91x blended ROAS) across 31,574 store orders (₹288.53 blended CPA), with conservative (3.00x / ₹2.73 Cr) and stretch (4.20x / ₹3.82 Cr) sensitivity scenarios. The forecast is built on Total Sales Revenue, the primary sales metric in the financial model (Section 7).", bold_prefix="Forecast (Dec 2026 – Feb 2027):")'

replacement = 'add_body(" on a planned ad spend of ₹91.1 Lakhs, the Recommended Plan delivers about ₹2.33 Cr of Gross Sales (2.55x blended ROAS) across 21,155 store orders (₹431 spend per order), with Base (2.80x / ₹1.96 Cr / ~17.8k orders) and Aggressive (2.32x / ₹2.61 Cr / ~23.8k orders) scenarios. Order volumes are calibrated using an empirical ₹1,100 AOV baseline, and marginal returns confirm Plan 2 as the profit-maximizing choice (Section 7).", bold_prefix="Forecast (Dec 2026 – Feb 2027):")'

if target in text:
    text = text.replace(target, replacement)
    with open(r"C:\Users\test\Videos\Office\scripts\build_perfect_report.py", "w", encoding="utf-8") as f:
        f.write(text)
    print("Successfully updated Page 1 executive summary.")
else:
    print("Target not found.")
