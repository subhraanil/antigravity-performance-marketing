import re

path = r"C:\Users\test\Videos\Office\scripts\generate_client_forensic_doc_and_pdf.py"

with open(path, "r", encoding="utf-8") as f:
    text = f.read()

target_pattern = r"(    # ---------------------------------------------------------------------------\n    # SECTION 8: ONBOARDING & TRANSITION PROTOCOL[\s\S]*?)(    # Save DOCX)"

replacement = """    # ---------------------------------------------------------------------------
    # SECTION 8: OPERATIONAL EXECUTION & IMMEDIATE ACCOUNT RESTORATION
    # ---------------------------------------------------------------------------
    h8 = doc.add_heading("8. Operational Execution & Immediate Account Restoration Protocol", level=1)
    h8.paragraph_format.space_before = Pt(14)

    p_ob = doc.add_paragraph(
        "Techno Exponent has already verified full Admin access across Google Ads, Meta Business Suite, "
        "Google Merchant Center, and Shopify (assigned to subhranilnaskar@technoexponent.com). With access fully confirmed, "
        "the team is initiating the following immediate 48-hour execution sprint to halt budget bleed and stabilize account economics:"
    )
    p_ob.paragraph_format.line_spacing = 1.15

    ob_steps = [
        ("Step 1 (Immediate - Hours 0 to 4): Access Verified & Emergency Bleed Termination", "Admin access confirmed. Immediately pause the ₹50,000 dead IG-Traffic link-click campaign, pause zombie app promotion ads, and purge all 'Glam+' copy-paste assets from Google PMax asset groups."),
        ("Step 2 (Day 1 - Hours 4 to 24): Catalog Hygiene & 404 URL Exclusion", "Disapprove and exclude all 110 broken 404 URLs in Google Merchant Center to halt zero-conversion click drain. Verify Google Ads Enhanced Conversions tracking and test Meta CAPI server-side event deduplication on Shopify."),
        ("Step 3 (Day 2 - Hours 24 to 48): Audience Exclusions & Retargeting Reset", "Inject 30-day and 180-day customer exclusion custom audiences into Meta Dynamic Product Ads (DPA) to immediately cure the ₹513 retargeting CPA inversion. Implement frequency capping at ≤ 2.2 impressions/week."),
        ("Step 4 (Day 2+): Restructured Campaign Launch", "Deploy 1 Master TOF Advantage+ Shopping Campaign (ASC) with a 20% existing customer budget cap, 1 Clean DPA Retargeting set, and 1 High-Margin PMax structure with segmented listing groups.")
    ]
    for st_title, st_desc in ob_steps:
        bp = doc.add_paragraph(style='List Bullet')
        r1 = bp.add_run(st_title + ": ")
        r1.bold = True
        r1.font.name = "Calibri"
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = navy_color
        r2 = bp.add_run(st_desc)
        r2.font.name = "Calibri"
        r2.font.size = Pt(9.5)
        bp.paragraph_format.space_after = Pt(2)

"""

new_text = re.sub(target_pattern, replacement + r"\2", text)

if new_text == text:
    print("ERROR: Could not match Section 8 pattern!")
else:
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_text)
    print("SUCCESS: Updated Section 8 in generate_client_forensic_doc_and_pdf.py")
