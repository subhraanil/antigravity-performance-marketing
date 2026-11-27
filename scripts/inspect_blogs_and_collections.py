import csv
import sys
if sys.stdout.encoding != 'utf-8': sys.stdout.reconfigure(encoding='utf-8')

sf_internal_path = r'website audit/makemealabel.com/internal_all.csv'

with open(sf_internal_path, 'r', encoding='utf-8-sig', errors='ignore') as f:
    reader = csv.DictReader(f)
    print("=== BLOG POSTS & ARTICLES ===")
    for row in reader:
        u = row.get("Address", "")
        if "/blogs/" in u:
            print(f"URL: {u}")
            print(f"  Title: {row.get('Title 1')}")
            print(f"  H1: {row.get('H1-1')}")
            print(f"  Words: {row.get('Word Count')} | Indexability: {row.get('Indexability')}\n")

with open(sf_internal_path, 'r', encoding='utf-8-sig', errors='ignore') as f:
    reader = csv.DictReader(f)
    print("=== ALL COLLECTION PAGES ===")
    for row in reader:
        u = row.get("Address", "")
        if "/collections/" in u:
            print(f"URL: {u}")
            print(f"  Title: {row.get('Title 1')}")
            print(f"  Meta Desc: {row.get('Meta Description 1')[:80]}...")
            print(f"  H1: '{row.get('H1-1')}'")
            print(f"  Words: {row.get('Word Count')}\n")
