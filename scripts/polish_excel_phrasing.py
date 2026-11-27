path = r"C:\Users\test\Videos\Office\scripts\build_all_forecasts_master_excel.py"

with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# Replace phrasing
text = text.replace('"100% Achievable Low-Risk Recovery"', '"Q1 2027 Structured Turnaround Plan"')
text = text.replace('"Conservative 3-Month Plan (Recommended)"', '"Calibrated 3-Month Plan (Recommended)"')
text = text.replace('"Risk-Free Model: Spend flat/reduced in Dec, CPA gains from waste elimination, returning to August 2026 baseline"', '"Phased Performance Model: Waste elimination, CPA normalization, and profitable order scaling"')
text = text.replace('"Cumulative Low-Risk Recovery Plan"', '"Q1 2027 Cumulative Turnaround Plan"')
text = text.replace('"Conservative 3M - Blended"', '"3-Month Plan - Blended"')
text = text.replace('"Conservative 3M - Google Ads"', '"3-Month Plan - Google Ads"')
text = text.replace('"Conservative 3M - Meta Ads"', '"3-Month Plan - Meta Ads"')
text = text.replace('"FABB6 — Conservative 3-Month Blended Store Turnaround Forecast"', '"FABB6 — Calibrated 3-Month Blended Store Turnaround Forecast"')
text = text.replace('"FABB6 — Google Ads Conservative 3-Month Recovery Forecast"', '"FABB6 — Google Ads 3-Month Performance Recovery Forecast"')
text = text.replace('"FABB6 — Meta Ads Conservative 3-Month Recovery Forecast"', '"FABB6 — Meta Ads 3-Month Performance Recovery Forecast"')

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("SUCCESS: Updated Excel build script phrasing.")
