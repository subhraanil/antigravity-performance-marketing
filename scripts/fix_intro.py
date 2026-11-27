path = r"C:\Users\test\Videos\Office\scripts\generate_client_forensic_doc_and_pdf.py"

with open(path, "r", encoding="utf-8") as f:
    text = f.read()

import re

broken = '''    p_f_intro = doc.add_paragraph(
        "The financial turnaround model for Q1 (December 2026 – February 2027) establishes a structured, phased pathway "
        "to rapidly normalize customer acquisition costs (CPA) and expand monthly order volume. Growth in Month 1 (December) "
        "is unlocked through decisive waste elimination: purging 110 broken 404 URLs in Google Merchant Center, removing all "
        "foreign 'Glam+' copy-paste assets, terminating the ₹50,000 non-converting IG traffic campaign, and enforcing 30-day "
        "customer exclusions on Meta retargeting.

"
        "Paid ad spend is maintained at ₹30.0 Lakhs in December (optimizing Meta spend by ₹2.0L to cut unprofitable burn and "
        "reallocating ₹50,000 to high-ROAS Google Ads). As asset groups and audience signals stabilize, the account scales systematically "
        "to 14,592 total store orders by February 2027, expanding net monthly revenue to ₹2.03 Cr+ at a 5.99x blended ROAS."
    )'''

fixed = '''    p_f_intro = doc.add_paragraph(
        "The financial turnaround model for Q1 (December 2026 – February 2027) establishes a structured, phased pathway "
        "to rapidly normalize customer acquisition costs (CPA) and expand monthly order volume. Growth in Month 1 (December) "
        "is unlocked through decisive waste elimination: purging 110 broken 404 URLs in Google Merchant Center, removing all "
        "foreign 'Glam+' copy-paste assets, terminating the ₹50,000 non-converting IG traffic campaign, and enforcing 30-day "
        "customer exclusions on Meta retargeting. "
        "Paid ad spend is maintained at ₹30.0 Lakhs in December (optimizing Meta spend by ₹2.0L to cut unprofitable burn and "
        "reallocating ₹50,000 to high-ROAS Google Ads). As asset groups and audience signals stabilize, the account scales systematically "
        "to 14,592 total store orders by February 2027, expanding net monthly revenue to ₹2.03 Cr+ at a 5.99x blended ROAS."
    )'''

if broken in text:
    text = text.replace(broken, fixed)
else:
    text = re.sub(
        r'p_f_intro = doc\.add_paragraph\([\s\S]*?p_f_intro\.paragraph_format\.line_spacing = 1\.15',
        fixed + '\n    p_f_intro.paragraph_format.line_spacing = 1.15',
        text
    )

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("SUCCESS: Fixed p_f_intro paragraph.")
