path = r"C:\Users\test\Videos\Office\scripts\generate_client_forensic_doc_and_pdf.py"

with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# Replace the broken string
broken_text = '''    p_f_intro = doc.add_paragraph(
        "To provide 100% confidence, zero execution risk, and predictable recovery, this financial model rejects aggressive or speculative budget expansion. "
        "Instead, it establishes a conservative 3-month stabilization path where performance gains in Month 1 (December 2026) are driven entirely by waste elimination: "
        "purging the 110 broken 404 URLs in Google Merchant Center, removing all 'Glam+' copy-paste assets, terminating the ₹50,000 dead IG traffic ad, and enforcing 30-day customer exclusions on Meta retargeting.

"
        "Paid ad spend is maintained strictly at ₹30.0 Lakhs in December (actually reducing Meta spend by ₹2.0L to cut unprofitable burn and reallocating ₹50,000 to high-ROAS Google Ads). "
        "By February 2027 (Month 3), the account merely recovers to its proven pre-competitor August 2026 performance baseline (Google CPA of ₹280 vs ₹279.79 in August; Meta CPA of ₹360 vs ₹343.83 in August)."
    )'''

fixed_text = '''    p_f_intro = doc.add_paragraph(
        "To provide 100% confidence, zero execution risk, and predictable recovery, this financial model rejects aggressive or speculative budget expansion. "
        "Instead, it establishes a conservative 3-month stabilization path where performance gains in Month 1 (December 2026) are driven entirely by waste elimination: "
        "purging the 110 broken 404 URLs in Google Merchant Center, removing all 'Glam+' copy-paste assets, terminating the ₹50,000 dead IG traffic ad, and enforcing 30-day customer exclusions on Meta retargeting. "
        "Paid ad spend is maintained strictly at ₹30.0 Lakhs in December (actually reducing Meta spend by ₹2.0L to cut unprofitable burn and reallocating ₹50,000 to high-ROAS Google Ads). "
        "By February 2027 (Month 3), the account merely recovers to its proven pre-competitor August 2026 performance baseline (Google CPA of ₹280 vs ₹279.79 in August; Meta CPA of ₹360 vs ₹343.83 in August)."
    )'''

if broken_text in text:
    text = text.replace(broken_text, fixed_text)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("SUCCESS: Fixed broken string in generate_client_forensic_doc_and_pdf.py")
else:
    # Try regex fix if exact match fails
    import re
    text = re.sub(
        r'p_f_intro = doc\.add_paragraph\([\s\S]*?p_f_intro\.paragraph_format\.line_spacing = 1\.15',
        fixed_text + '\n    p_f_intro.paragraph_format.line_spacing = 1.15',
        text
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("SUCCESS: Applied regex fix for p_f_intro")
