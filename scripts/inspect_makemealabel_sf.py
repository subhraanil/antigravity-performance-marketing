import csv
import os
import sys

# Ensure utf-8 stdout
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

sf_issues_path = r'website audit/makemealabel.com/issues_overview_report.csv'
sf_internal_path = r'website audit/makemealabel.com/internal_all.csv'

print("=== 1. ISSUES OVERVIEW REPORT ===")
if os.path.exists(sf_issues_path):
    with open(sf_issues_path, 'r', encoding='utf-8-sig', errors='ignore') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if row:
                # filter out 0 count issues if possible
                print(" | ".join(row[:4]))
else:
    print("Issues report not found")

print("\n=== 2. INTERNAL ALL CSV STATS ===")
if os.path.exists(sf_internal_path):
    with open(sf_internal_path, 'r', encoding='utf-8-sig', errors='ignore') as f:
        reader = csv.reader(f)
        header = next(reader)
        print("Total Columns:", len(header))
        print("Header Preview:", header[:20])
        
        status_counts = {}
        content_types = {}
        indexability_counts = {}
        sample_urls = []
        
        url_idx = 0
        status_idx = header.index("Status Code") if "Status Code" in header else 2
        ct_idx = header.index("Content Type") if "Content Type" in header else -1
        idx_idx = header.index("Indexability") if "Indexability" in header else -1
        
        total_rows = 0
        for row in reader:
            if not row: continue
            total_rows += 1
            u = row[url_idx]
            if len(sample_urls) < 15:
                sample_urls.append(u)
            
            st = row[status_idx] if status_idx < len(row) else "Unknown"
            status_counts[st] = status_counts.get(st, 0) + 1
            
            if ct_idx != -1 and ct_idx < len(row):
                ct = row[ct_idx].split(";")[0]
                content_types[ct] = content_types.get(ct, 0) + 1
                
            if idx_idx != -1 and idx_idx < len(row):
                idx_val = row[idx_idx]
                indexability_counts[idx_val] = indexability_counts.get(idx_val, 0) + 1
                
        print(f"Total Rows: {total_rows}")
        print("Status Counts:", status_counts)
        print("Content Types:", content_types)
        print("Indexability:", indexability_counts)
        print("\nSample URLs:")
        for su in sample_urls:
            print(" ", su)
