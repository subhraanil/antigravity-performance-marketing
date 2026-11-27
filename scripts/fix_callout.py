path = r"C:\Users\test\Videos\Office\scripts\generate_client_forensic_doc_and_pdf.py"

with open(path, "r", encoding="utf-8") as f:
    text = f.read()

import re

old_callout = """    add_callout_box(
        doc,
        "Why This 3-Month Plan Is 100% Achievable & Risk-Free",
        "1. Zero Speculative Budget Surge: December total spend is capped at ₹30.0L (Meta spend is reduced by ₹2.0L to cut waste, and ₹50k is reallocated to Google PMax).
"
        "2. Gains Come Exclusively from Waste Elimination: Pausing the ₹50,000 dead link-click traffic campaign, removing 110 broken 404 URLs, and excluding 30-day purchasers fixes the broken economics immediately.
"
        "3. Re-Anchored to Proven Historical Reality: In August 2026, FABB6 generated 8,953 paid orders at ₹335 blended CPA on ₹30L spend. February 2027 targets (₹345 CPA, 9,842 paid orders) merely restore the account back to this verified pre-competitor level."
    )"""

new_callout = """    add_callout_box(
        doc,
        "Why This 3-Month Plan Is 100% Achievable & Risk-Free",
        "1. Zero Speculative Budget Surge: December total spend is capped at ₹30.0L (Meta spend is reduced by ₹2.0L to cut waste, and ₹50k is reallocated to Google PMax). "
        "2. Gains Come Exclusively from Waste Elimination: Pausing the ₹50,000 dead link-click traffic campaign, removing 110 broken 404 URLs, and excluding 30-day purchasers fixes the broken economics immediately. "
        "3. Re-Anchored to Proven Historical Reality: In August 2026, FABB6 generated 8,953 paid orders at ₹335 blended CPA on ₹30L spend. February 2027 targets (₹345 CPA, 9,842 paid orders) merely restore the account back to this verified pre-competitor level."
    )"""

if old_callout in text:
    text = text.replace(old_callout, new_callout)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("SUCCESS: Fixed callout box string")
else:
    # Regex fallback
    text = re.sub(
        r'add_callout_box\(\s*doc,\s*"Why This 3-Month Plan Is 100% Achievable & Risk-Free",[\s\S]*?\)\s*# ---',
        new_callout + '\n    # ---',
        text
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("SUCCESS: Applied regex fallback for callout box")
