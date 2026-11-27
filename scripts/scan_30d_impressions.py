import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

f_30d = r'.\data\IHLS\Search terms report.xlsx'
df = pd.read_excel(f_30d, skiprows=2)
df_clean = df[~df['Search term'].astype(str).str.startswith('Total:')].copy()

# Look at zero-click terms that had impressions
impr_terms = df_clean[df_clean['Clicks'] == 0].copy()
print(f"Total zero-click search terms: {len(impr_terms)}")

# Check for junk patterns in impressions
junk_patterns = [
    'salon', 'barber', 'waxing', 'removal', 'electrolysis', 'braid', 'fade', 'taper',
    'dye', 'bleach', 'perm', 'straightening', 'dog', 'cat', 'puppy', 'mange',
    'pubic', 'ingrown', 'armpit', 'onion', 'rosemary', 'castor', 'clove', 'rice water',
    'chemist warehouse', 'priceline', 'coles', 'woolworths', 'kmart', 'amazon', 'ebay',
    'course', 'salary', 'jobs', 'hiring', 'training', 'reddit', 'quora', 'pdf', 'wiki',
    'melbourne', 'sydney', 'brisbane', 'adelaide', 'turkey', 'india', 'uk',
    'finasteride', 'minoxidil', 'dutasteride', 'steroid', 'sperm', 'erectile',
    'chemo', 'cancer', 'radiation', 'lice', 'nits', 'ringworm', 'cradle cap'
]

matched_impr = []
for p in junk_patterns:
    m = impr_terms[impr_terms['Search term'].str.lower().str.contains(r'\b' + p)]
    if len(m) > 0:
        matched_impr.append((p, len(m), m['Search term'].head(3).tolist()))

print("\nJunk impressions blocked/appearing:")
for p, count, ex in matched_impr:
    print(f"  Pattern '{p}': {count} queries, e.g. {ex}")
