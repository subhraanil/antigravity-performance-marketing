with open(r"C:\Users\test\Videos\Office\scripts\build_perfect_report.py", "r", encoding="utf-8") as f:
    text = f.read()

# Update Table 7.4 in build_perfect_report.py
old_chan_table = """    chan_table_data = [
        ["Month", "Google spend", "Google CPA target", "Google orders", "Meta spend", "Meta CPA target", "Meta orders", "Combined paid orders"],
        ["Dec 2026", "₹16.0L", "₹450", "3,556", "₹10.0L", "₹450", "2,222", "5,778"],
        ["Jan 2027", "₹20.0L", "₹430", "4,651", "₹11.0L", "₹410", "2,683", "7,334"],
        ["Feb 2027", "₹22.0L", "₹410", "5,366", "₹12.1L", "₹385", "3,143", "8,509"]
    ]"""

new_chan_table = """    chan_table_data = [
        ["Month", "Google spend (55/60%)", "Google CPA target", "Google orders", "Meta spend (45/40%)", "Meta CPA target", "Meta orders", "Combined paid orders"],
        ["Dec 2026", "₹14.30L (55%)", "₹460", "3,109", "₹11.70L (45%)", "₹430", "2,721", "5,830"],
        ["Jan 2027", "₹18.60L (60%)", "₹440", "4,227", "₹12.40L (40%)", "₹400", "3,100", "7,327"],
        ["Feb 2027", "₹20.46L (60%)", "₹420", "4,871", "₹13.64L (40%)", "₹380", "3,589", "8,460"]
    ]"""

if old_chan_table in text:
    text = text.replace(old_chan_table, new_chan_table)

with open(r"C:\Users\test\Videos\Office\scripts\build_perfect_report.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Updated Table 7.4 in build_perfect_report.py successfully.")
