import csv

issues_csv = r"C:\Users\test\Videos\Personal\data\Paid Media World\Paid Media World - issues_overview_report.csv"

with open(issues_csv, mode="r", encoding="utf-8-sig", errors="replace") as f:
    r = csv.reader(f)
    headers = next(r)
    rows = list(r)

print(f"Total issues listed: {len(rows)}")
print(f"{headers[0]:<45} | {headers[1]:<12} | {headers[2]:<8} | {headers[3]:<6} | {headers[4]}")
print("-" * 90)
for row in sorted(rows, key=lambda x: (0 if x[2]=='High' else (1 if x[2]=='Medium' else 2), -int(x[3]) if x[3].isdigit() else 0)):
    if any(row):
        print(f"{row[0]:<45} | {row[1]:<12} | {row[2]:<8} | {row[3]:<6} | {row[4]}%")
