with open(r"C:\Users\test\.gemini\antigravity\brain\29f77e0a-5ed5-4d24-842c-443d9957274c\fabb6_final_client_master_deliverable_report.md", "r", encoding="utf-8") as f:
    text = f.read()

# Update Section 1
old_s1 = "Forecast (Dec 2026 – Feb 2027): on a planned ad spend of ₹91.1 Lakhs, the forecast delivers about ₹3.56 Cr of Total Sales Revenue (3.91x blended ROAS) across 31,574 store orders (₹288.53 blended CPA), with conservative (3.00x / ₹2.73 Cr) and stretch (4.20x / ₹3.82 Cr) sensitivity scenarios. The forecast is built on Total Sales Revenue, the primary sales metric in the financial model (Section 7)."

new_s1 = "Forecast (Dec 2026 – Feb 2027): on a planned ad spend of ₹91.1 Lakhs, the Recommended Plan delivers about ₹2.33 Cr of Gross Sales (2.55x blended ROAS) across 21,155 store orders (₹431 spend per order), with Base (2.80x / ₹1.96 Cr / ~17.8k orders) and Aggressive (2.32x / ₹2.61 Cr / ~23.8k orders) scenarios. Order volumes are calibrated using an empirical ₹1,100 AOV baseline, and marginal returns confirm Plan 2 as the profit-maximizing choice (Section 7)."

if old_s1 in text:
    text = text.replace(old_s1, new_s1)

# Update Scaling rule
old_scale = "scale a step only if trailing seven-day Total Sales ROAS is at least **2.4x** and CPA is within target. Hold spend between **2.2x and 2.4x**. Roll back the last increase if the ratio stays below **2.2x** for seven consecutive days."

new_scale = "scale a step only if trailing seven-day confirmed ROAS is at least **2.50x** and CPA is within target. Hold spend between **2.30x and 2.50x**. Roll back the last increase if the ratio stays below **2.30x** for seven consecutive days."

if old_scale in text:
    text = text.replace(old_scale, new_scale)

# Update Section 7.2 table
old_tab_7_2 = """| Month | Ad spend (Google / Meta) | Paid orders | Orders from others | Total store orders | Total Sales Revenue | Blended CPA | Total Sales ROAS |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Dec 2026** | ₹26.0L (₹16.0L / ₹10.0L) | 5,778 | 3,096 | 8,874 | ₹89.98L | ₹293.00 | **3.46x** |
| **Jan 2027** | ₹31.0L (₹20.0L / ₹11.0L) | 7,334 | 3,313 | 10,647 | ₹117.43L (₹1.17 Cr) | ₹291.17 | **3.79x** |
| **Feb 2027** | ₹34.1L (₹22.0L / ₹12.1L) | 8,509 | 3,545 | 12,053 | ₹148.50L (₹1.48 Cr) | ₹282.91 | **4.35x** |
| **Total Q1 Plan** | **₹91.1L** (₹58.0L / ₹33.1L) | **21,621** | **9,953** | **31,574** | **₹355.91L (₹3.56 Cr)** | **₹288.53** | **3.91x** |"""

new_tab_7_2 = """| Month | Ad spend (Google / Meta) | Paid orders | Repeat / Organic | Total store orders | Gross Sales Revenue | Spend / Order | Confirmed ROAS |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Dec 2026** | ₹26.0L (₹16.0L / ₹10.0L) | 4,667 | 1,242 | 5,909 | ₹65.00L | ₹440.01 | **2.50x** |
| **Jan 2027** | ₹31.0L (₹20.0L / ₹11.0L) | 5,732 | 1,454 | 7,186 | ₹79.05L | ₹431.39 | **2.55x** |
| **Feb 2027** | ₹34.1L (₹22.0L / ₹12.1L) | 6,500 | 1,560 | 8,060 | ₹88.66L | ₹423.08 | **2.60x** |
| **Total Q1 Plan** | **₹91.1L** (₹58.0L / ₹33.1L) | **16,899** | **4,256** | **21,155** | **₹232.71L (~₹2.33 Cr)** | **₹430.63** | **2.55x** |"""

if old_tab_7_2 in text:
    text = text.replace(old_tab_7_2, new_tab_7_2)

# Update Section 7.3 table
old_tab_7_3 = """| Scenario | Total Sales ROAS (Dec / Jan / Feb) | Dec Total Sales | Jan Total Sales | Feb Total Sales | Quarter Total Revenue | Quarter ROAS |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Conservative Scenario** | 3.00x / 3.00x / 3.00x | ₹78.0L | ₹93.0L | ₹102.3L | **₹273.3L (₹2.73 Cr)** | **3.00x** |
| **Target Plan (Master Forecast)** | 3.46x / 3.79x / 4.35x | ₹89.98L | ₹117.43L | ₹148.50L | **₹355.91L (₹3.56 Cr)** | **3.91x** |
| **Stretch Scenario** | 3.70x / 4.10x / 4.65x | ₹96.2L | ₹127.1L | ₹158.6L | **₹381.9L (₹3.82 Cr)** | **4.19x** |"""

new_tab_7_3 = """| Scenario | Confirmed ROAS (Dec / Jan / Feb) | Dec Gross Sales | Jan Gross Sales | Feb Gross Sales | Total Gross Sales | Quarter ROAS |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Plan 1: Base (Capital Preservation)** | 2.80x / 2.80x / 2.80x | ₹56.00L | ₹67.20L | ₹72.80L | **₹196.0L (₹1.96 Cr)** | **2.80x** |
| **Plan 2: Recommended (Target Turnaround)** | 2.50x / 2.55x / 2.60x | ₹65.00L | ₹79.05L | ₹88.66L | **₹232.7L (~₹2.33 Cr)** | **2.55x** |
| **Plan 3: Aggressive (Market Share Expansion)** | 2.40x / 2.35x / 2.25x | ₹72.00L | ₹88.13L | ₹101.25L | **₹261.4L (~₹2.61 Cr)** | **2.32x** |"""

if old_tab_7_3 in text:
    text = text.replace(old_tab_7_3, new_tab_7_3)

with open(r"C:\Users\test\.gemini\antigravity\brain\29f77e0a-5ed5-4d24-842c-443d9957274c\fabb6_final_client_master_deliverable_report.md", "w", encoding="utf-8") as f:
    f.write(text)

print("Updated fabb6_final_client_master_deliverable_report.md successfully.")
