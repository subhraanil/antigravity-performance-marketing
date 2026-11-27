import csv
from collections import Counter

html_csv = r"C:\Users\test\Videos\Personal\data\Paid Media World\Paid Media World - internal_html.csv"

with open(html_csv, mode="r", encoding="utf-8-sig", errors="replace") as f:
    r = csv.DictReader(f)
    rows = list(r)

print(f"Total rows: {len(rows)}")

indexable_rows = [r for r in rows if r.get("Indexability") == "Indexable"]
non_indexable_rows = [r for r in rows if r.get("Indexability") == "Non-Indexable"]
print(f"Indexable: {len(indexable_rows)}")
print(f"Non-Indexable: {len(non_indexable_rows)}")

# Missing Canonicals
missing_canons = [r for r in indexable_rows if not r.get("Canonical Link Element 1")]
print(f"Indexable missing canonicals: {len(missing_canons)} / {len(indexable_rows)}")

# Titles > 60 chars
long_titles = [r for r in indexable_rows if int(r.get("Title 1 Length", 0) or 0) > 60]
print(f"Titles > 60 chars: {len(long_titles)} / {len(indexable_rows)}")

# Meta descriptions > 155 chars
long_meta = [r for r in indexable_rows if int(r.get("Meta Description 1 Length", 0) or 0) > 155]
print(f"Meta descriptions > 155 chars: {len(long_meta)} / {len(indexable_rows)}")

# Missing meta descriptions
missing_meta = [r for r in indexable_rows if not r.get("Meta Description 1")]
print(f"Missing meta descriptions: {len(missing_meta)} / {len(indexable_rows)}")

# Missing H1
missing_h1 = [r for r in indexable_rows if not r.get("H1-1")]
print(f"Missing H1: {len(missing_h1)} / {len(indexable_rows)}")

# Multiple H1
mult_h1 = [r for r in indexable_rows if r.get("H1-2")]
print(f"Multiple H1: {len(mult_h1)} / {len(indexable_rows)}")

# Word count analysis
word_counts = [int(r.get("Word Count", 0) or 0) for r in indexable_rows]
print(f"Word counts: Min={min(word_counts)}, Max={max(word_counts)}, Avg={sum(word_counts)/len(word_counts):.1f}")
thin_pages = [r for r in indexable_rows if int(r.get("Word Count", 0) or 0) < 300]
print(f"Thin pages (< 300 words): {len(thin_pages)}")
for tp in thin_pages:
    print(f"  {tp['Address']} | Words: {tp.get('Word Count')}")

# HTML Entities in Title or H1
entity_titles = [r for r in indexable_rows if "&#" in r.get("Title 1", "") or "&amp;" in r.get("Title 1", "")]
print(f"Titles with raw HTML entities: {len(entity_titles)}")
for et in entity_titles[:5]:
    print(f"  {et['Address']} | Title: {et.get('Title 1')}")
