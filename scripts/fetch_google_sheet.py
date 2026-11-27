import os

output_path = 'reports/google_sheet_data.csv'

with open(output_path, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

print(f"Total lines in downloaded Google Sheet: {len(lines)}")
for i, line in enumerate(lines):
    clean_line = line.strip().replace('\u20b9', 'INR ')
    print(f"Line {i+1}: {clean_line}")
