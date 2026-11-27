import os

md_path = r"C:\Users\test\.gemini\antigravity\brain\29f77e0a-5ed5-4d24-842c-443d9957274c\fabb6_final_client_master_deliverable_report.md"

with open(md_path, "r", encoding="utf-8") as f:
    text = f.read()

# Update Section 3
target_sec3 = """5. **Off-category search queries:** A campaign named 'Search-Brand' used broad match and triggered queries unrelated to beauty (for example, gym equipment and a badminton ankle support). The spend on these queries is not yet quantified; it will be after a full search terms export.

---"""

replacement_sec3 = """5. **Off-category search queries:** A campaign named 'Search-Brand' used broad match and triggered queries unrelated to beauty (for example, gym equipment and a badminton ankle support). The spend on these queries is not yet quantified; it will be after a full search terms export.
6. **Merchant Center SKU click bleed & feed misallocation (Sep 1 – Nov 19, 2026):** Official Merchant Center performance exports across 3,411 SKUs show 6.14 Crore impressions and 6,29,968 clicks, yet only 48.77 purchases were tracked (0.0077% conversion rate) due to the severed conversion action. Furthermore, 86.2% of all clicks (5,42,808 clicks) were concentrated on 3,358 products that produced ZERO purchases because campaigns ran on 'All Products' without custom label margin filtering. Cheap single-use entry items and low-margin products cannibalized the budget without margin exclusions (Exhibit G).

#### Top Zero-Converting Click Bleeder SKUs in Google Merchant Center (Sep 1 – Nov 19, 2026)

| Top Bleeding SKU (Zero Purchases) | Price / Tier | Margin Class | Impressions | Clicks | Tracked Purchases |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Raaga Professional De-Tan Cream (single use)** | ₹69 (T1 Entry) | mid_20_28 | 1,261,144 | 27,648 | 0.00 |
| **DOT & KEY Strawberry Dew Tinted Sunscreen 50ml** | ₹549 (T2 Core) | mid_20_28 | 669,332 | 17,485 | 0.00 |
| **Loreal Paris Hair Spa Deep Nourish 490g** | ₹650 (T2 Core) | mid_20_28 | 766,242 | 13,249 | 0.00 |
| **Matrix Mega Smooth Masque 500g** | ₹750 (T2 Core) | mid_20_28 | 810,808 | 9,192 | 0.00 |
| **Loreal Majirel 3.0 Combo + Developer 1000ml** | ₹755 (T2 Core) | high_28plus | 673,069 | 9,142 | 0.00 |
| **Floractive Professional W One Nanoplastia 1000ml** | ₹5,500 (T4 Pro) | high_28plus | 1,357,589 | 6,921 | 0.00 |
| **Total Top 6 Zero-Converting Bleeders** | — | — | **5,538,184** | **83,637** | **0.00** |

*Products flagged `EXCLUDE_lowmargin` served 8.47L impressions and 9,354 clicks, while low-margin items (<20% margin) took 1.07L clicks. These bleeders will be hard-excluded in Phase 1.*

---"""

if target_sec3 in text:
    text = text.replace(target_sec3, replacement_sec3)

# Update Section 6 Phase 1
target_p1 = """* Pause 'IG-Traffic' and the iOS and Android app install campaigns."""
replacement_p1 = """* Pause 'IG-Traffic' and the iOS and Android app install campaigns.
* Hard-exclude the top 20 zero-converting click bleeder SKUs identified in Merchant Center (e.g., Raaga single-use de-tan cream and unsegmented core SKUs)."""

if target_p1 in text:
    text = text.replace(target_p1, replacement_p1)

# Update Section 6 Phase 2
target_p2 = """* Segment Performance Max into Hero Best-Sellers (60% of budget), Long-Tail Catalog (20%) and Search/Brand (20%)."""
replacement_p2 = """* Segment Performance Max and Standard Shopping strictly by Custom Label 1 (Price Tier) and Custom Label 4 (Margin Class): Hero Best-Sellers (high_28plus & T4 Pro/Salon, 60% of budget), Core Catalog (mid_20_28, 20%), and Brand Search (20%). Hard-exclude EXCLUDE_lowmargin and unbundled T1 Entry single sachets."""

if target_p2 in text:
    text = text.replace(target_p2, replacement_p2)

# Update Appendix A
target_app_a = """* **Exhibit F:** Meta link clicks versus Shopify landing page views."""
replacement_app_a = """* **Exhibit F:** Meta link clicks versus Shopify landing page views.
* **Exhibit G:** Google Merchant Center product performance export (Sep 1 – Nov 19, 2026) and catalog audit showing 86.2% zero-conversion click concentration and price/margin tier misallocation."""

if target_app_a in text:
    text = text.replace(target_app_a, replacement_app_a)

with open(md_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Updated fabb6_final_client_master_deliverable_report.md successfully.")
