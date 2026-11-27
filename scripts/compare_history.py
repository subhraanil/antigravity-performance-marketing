# Script to benchmark the 3 forecast plans against the historical data

history = [
    {"m": "Dec 2025", "orders": 3307, "gross": 2951001.04, "spend": 420867.85, "aov": 892.35, "store_roas": 7.01, "paid_cpa": 260.69, "paid_roas": 3.51, "paid_orders": 1614.45, "paid_share": 0.488},
    {"m": "Jan 2026", "orders": 7850, "gross": 6613526.56, "spend": 1216539.84, "aov": 842.49, "store_roas": 5.44, "paid_cpa": 285.57, "paid_roas": 3.01, "paid_orders": 4260.0, "paid_share": 0.543},
    {"m": "Feb 2026", "orders": 8250, "gross": 7610564.12, "spend": 1797004.61, "aov": 922.49, "store_roas": 4.24, "paid_cpa": 373.05, "paid_roas": 2.43, "paid_orders": 4817.0, "paid_share": 0.584},
    {"m": "Mar 2026", "orders": 11285, "gross": 10105021.03, "spend": 2784073.76, "aov": 895.44, "store_roas": 3.63, "paid_cpa": 438.37, "paid_roas": 1.93, "paid_orders": 6351.0, "paid_share": 0.563},
    {"m": "Apr 2026", "orders": 10591, "gross": 10032210.79, "spend": 3255207.89, "aov": 947.24, "store_roas": 3.08, "paid_cpa": 608.45, "paid_roas": 1.42, "paid_orders": 5350.0, "paid_share": 0.505},
    {"m": "May 2026", "orders": 12215, "gross": 11956645.70, "spend": 4021303.60, "aov": 978.85, "store_roas": 2.97, "paid_cpa": 568.30, "paid_roas": 1.59, "paid_orders": 7076.0, "paid_share": 0.579},
    {"m": "Jun 2026", "orders": 12877, "gross": 12287034.35, "spend": 4286498.43, "aov": 954.18, "store_roas": 2.87, "paid_cpa": 625.67, "paid_roas": 1.39, "paid_orders": 6851.0, "paid_share": 0.532},
    {"m": "Jul 2026", "orders": 13420, "gross": 12231397.80, "spend": 4362222.49, "aov": 911.43, "store_roas": 2.80, "paid_cpa": 524.75, "paid_roas": 1.64, "paid_orders": 8313.0, "paid_share": 0.619},
    {"m": "Aug 2026", "orders": 11069, "gross": 11120133.60, "spend": 4791163.06, "aov": 1004.62, "store_roas": 2.32, "paid_cpa": 436.95, "paid_roas": 2.26, "paid_orders": 10965.0, "paid_share": 0.991},
    {"m": "Sep 2026", "orders": 3112, "gross": 4147467.35, "spend": 627052.85, "aov": 1332.73, "store_roas": 6.61, "paid_cpa": 782.84, "paid_roas": 1.71, "paid_orders": 801.0, "paid_share": 0.257},
    {"m": "Oct 2026", "orders": 9143, "gross": 12093428.35, "spend": 4246579.26, "aov": 1322.70, "store_roas": 2.85, "paid_cpa": 474.58, "paid_roas": 2.19, "paid_orders": 8948.0, "paid_share": 0.979},
    {"m": "Nov 2026", "orders": 6061, "gross": 7934601.85, "spend": 2078199.14, "aov": 1309.12, "store_roas": 3.82, "paid_cpa": 457.95, "paid_roas": 2.57, "paid_orders": 4538.0, "paid_share": 0.749}
]

print("=== HISTORICAL BENCHMARK SUMMARY ===")
print("Metric                    | Dec'25-Jul'26 Avg | Aug 2026   | Oct 2026   | Nov 2026 MTD | Q1 Plan Range")
print("-" * 95)
print(f"Store AOV (Gross)         | ₹920.89           | ₹1,004.62  | ₹1,322.70  | ₹1,309.12    | ₹1,309 → ₹1,500")
print(f"Blended Paid CPA          | ₹462.81           | ₹436.95    | ₹474.58    | ₹457.95      | ₹550 → ₹500")
print(f"Blended Paid ROAS         | 2.05x             | 2.26x      | 2.19x      | 2.57x        | 2.38x → 3.00x")
print(f"Blended Store ROAS        | 3.89x             | 2.32x      | 2.85x      | 3.82x        | 3.48x → 4.39x")
print(f"Paid Orders Share         | 55.8%             | 99.1%      | 97.9%      | 74.9%        | 61.9% → 74.4%")
print("-" * 95)
