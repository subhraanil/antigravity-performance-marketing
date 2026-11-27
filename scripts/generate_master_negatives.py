import pandas as pd
import numpy as np
import re
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

# File paths
f_all = r'.\data\IHLS\Search terms report - all time.xlsx'
f_oct = r'.\data\IHLS\Search terms report.xlsx'
f_details = r'.\data\IHLS\Negative keyword details report.xlsx'
f_rep = r'.\data\IHLS\Negative keyword report.xlsx'

df_all = pd.read_excel(f_all, skiprows=2)
df_all = df_all[~df_all['Search term'].astype(str).str.startswith('Total:')].copy()

df_oct = pd.read_excel(f_oct, skiprows=2)
df_oct = df_oct[~df_oct['Search term'].astype(str).str.startswith('Total:')].copy()

df_d = pd.read_excel(f_details, skiprows=2)
df_r = pd.read_excel(f_rep, skiprows=2)

for col in ['Cost', 'Conversions', 'Clicks', 'Conv. rate', 'Cost / conv.']:
    df_all[col] = pd.to_numeric(df_all[col], errors='coerce').fillna(0)
    df_oct[col] = pd.to_numeric(df_oct[col], errors='coerce').fillna(0)

# 1. Extract Converting Search Terms
conv_df = df_all[df_all['Conversions'] > 0].groupby(df_all['Search term'].str.lower().str.strip()).agg({
    'Conversions': 'sum',
    'Cost': 'sum',
    'Clicks': 'sum'
}).reset_index().sort_values(by='Conversions', ascending=False)
conv_queries = set(conv_df['Search term'])
print(f"Total converting queries to protect: {len(conv_queries)}")

# Helper to clean keyword strings
def clean_kw(kw):
    if pd.isna(kw): return ''
    kw = str(kw).strip().lower()
    if kw.startswith('"') and kw.endswith('"'): kw = kw[1:-1]
    if kw.startswith('[') and kw.endswith(']'): kw = kw[1:-1]
    return kw.strip()

# Protected core business tokens - NEVER block these
PROTECTED_TOKENS = {
    'ihls', 'subiaco', 'perth', 'clinic', 'clinics', 'treatment', 'treatments',
    'specialist', 'specialists', 'loss', 'hair', 'growth', 'regrowth', 'hairloss',
    'doctor', 'doctors', 'dermatologist', 'dermatologists', 'trichologist', 'trichologists',
    'restoration', 'transplant', 'transplants', 'system', 'systems', 'consultation', 'analysis',
    'female', 'male', 'women', 'womens', 'men', 'mens', 'scalp', 'thinning', 'alopecia',
    'androgenetic', 'pattern', 'follicle', 'follicles', 'therapy', 'therapies'
}

DANGEROUS_STOPWORDS = {
    'is', 'am', 'do', 'can', 'how', 'who', 'why', 'the', 'e', 'new', 'tip', 'way', 'kit', 'map', 'gas',
    'act', 'app', 'cd', 'cv', 'eds', 'faq', 'gnu', 'jpg', 'lab', 'law', 'max', 'mg', 'nax', 'pen', 'pix',
    'prf', 'red', 'sex', 'spa', 'tax', 'tea', 'toy', 'xxx', '100', '20', '35', '5', '植发'
}

# 2. Identify Harmful Existing Negatives
df_d['clean'] = df_d['keyword_text'].apply(clean_kw)
df_r['clean'] = df_r['Negative keyword'].apply(clean_kw)

removed_harmful = []
existing_list_d = []
for idx, r in df_d.iterrows():
    kw = r['clean']
    mt = str(r['match_type']).strip().upper()
    if kw in PROTECTED_TOKENS or kw in DANGEROUS_STOPWORDS:
        removed_harmful.append({
            'Source': 'Negative keyword details (Shared List)',
            'Negative Keyword': r['keyword_text'],
            'Match Type': r['match_type'],
            'Campaign / Context': 'Shared List Negatives',
            'Reason for Removal': 'Blocks core converting traffic' if kw in PROTECTED_TOKENS else 'Dangerous single word / stopword'
        })
    else:
        if kw:
            existing_list_d.append((kw, mt))

existing_list_r = []
for idx, r in df_r.iterrows():
    kw = r['clean']
    mt = str(r['Match type']).strip()
    if 'Phrase' in mt:
        mt_clean = 'PHRASE'
    elif 'Exact' in mt:
        mt_clean = 'EXACT'
    elif 'Broad' in mt:
        mt_clean = 'BROAD'
    else:
        mt_clean = 'PHRASE'
    if kw in PROTECTED_TOKENS or kw in DANGEROUS_STOPWORDS:
        removed_harmful.append({
            'Source': 'Negative keyword report (Campaign Level)',
            'Negative Keyword': r['Negative keyword'],
            'Match Type': r['Match type'],
            'Campaign / Context': str(r['Campaign']),
            'Reason for Removal': 'Blocks core converting traffic' if kw in PROTECTED_TOKENS else 'Dangerous single word / stopword'
        })
    else:
        if kw:
            existing_list_r.append((kw, mt_clean))

df_removed_harmful = pd.DataFrame(removed_harmful).drop_duplicates(subset=['Negative Keyword', 'Campaign / Context'])
print(f"Total harmful existing negatives identified for removal: {len(df_removed_harmful)}")

# 3. Categorized Negative Keyword Taxonomy
CATEGORIES_TAXONOMY = {
    '1. Hair Salons, Barbers & Hair Styling': {
        'description': 'Queries seeking haircuts, barber shops, braiding, perms, bleaching, styling or salon supplies.',
        'keywords': [
            ('barber', 'PHRASE'), ('barbers', 'PHRASE'), ('barber shop', 'PHRASE'), ('barbershop', 'PHRASE'),
            ('hairdresser', 'PHRASE'), ('hairdressers', 'PHRASE'), ('hairdressing', 'PHRASE'),
            ('haircut', 'PHRASE'), ('haircuts', 'PHRASE'), ('hair cut', 'PHRASE'), ('hair salon', 'PHRASE'),
            ('hair salons', 'PHRASE'), ('hair salon perth', 'PHRASE'), ('coiffeur', 'PHRASE'), ('coiffure', 'PHRASE'),
            ('hairmart', 'PHRASE'), ('booksy', 'PHRASE'), ('fresha', 'PHRASE'), ('circles of hair', 'PHRASE'),
            ('hair collaborative dianella', 'PHRASE'), ('dianella hair', 'PHRASE'), ('fade haircut', 'PHRASE'),
            ('taper fade', 'PHRASE'), ('low fade', 'PHRASE'), ('skin fade', 'PHRASE'), ('buzz cut', 'PHRASE'),
            ('hair dye', 'PHRASE'), ('hair colour', 'PHRASE'), ('hair coloring', 'PHRASE'), ('bleach hair', 'PHRASE'),
            ('bleaching hair', 'PHRASE'), ('balayage', 'PHRASE'), ('highlights hair', 'PHRASE'),
            ('perm hair', 'PHRASE'), ('hair perm', 'PHRASE'), ('perming', 'PHRASE'),
            ('nanoplasty', 'PHRASE'), ('hair straightening', 'PHRASE'), ('japanese straightening', 'PHRASE'),
            ('braids', 'PHRASE'), ('hair braiding', 'PHRASE'), ('dreadlocks', 'PHRASE'), ('dreads', 'PHRASE'),
            ('cornrows', 'PHRASE'), ('hair extensions salon', 'PHRASE'), ('clip in extensions', 'PHRASE'),
            ('tape hair extensions', 'PHRASE'), ('weft extensions', 'PHRASE'), ('keratin smoothing', 'PHRASE')
        ]
    },
    '2. Laser Hair Removal & Depilation': {
        'description': 'Queries looking to REMOVE hair (waxing, laser hair removal, IPL, electrolysis).',
        'keywords': [
            ('hair removal', 'PHRASE'), ('laser hair removal', 'PHRASE'), ('ipl hair removal', 'PHRASE'),
            ('electrolysis hair removal', 'PHRASE'), ('electrolysis', 'EXACT'), ('waxing', 'PHRASE'),
            ('hair waxing', 'PHRASE'), ('depilatory', 'PHRASE'), ('depilation', 'PHRASE'), ('epilator', 'PHRASE'),
            ('epilation', 'PHRASE'), ('shaving cream', 'PHRASE'), ('laser hair removal perth cost', 'PHRASE'),
            ('underarm hair removal', 'PHRASE'), ('facial hair removal', 'PHRASE'), ('face hair removal', 'PHRASE'),
            ('bikini hair removal', 'PHRASE'), ('brazilian hair removal', 'PHRASE'), ('pubic hair removal', 'PHRASE'),
            ('body hair removal', 'PHRASE'), ('chest hair removal', 'PHRASE'), ('leg hair removal', 'PHRASE')
        ]
    },
    '3. Animals & Pets Hair Loss': {
        'description': 'Veterinary hair loss queries for dogs, cats, and pets.',
        'keywords': [
            ('dog hair loss', 'PHRASE'), ('dog losing hair', 'PHRASE'), ('cat hair loss', 'PHRASE'),
            ('cat losing hair', 'PHRASE'), ('puppy hair loss', 'PHRASE'), ('kitten hair loss', 'PHRASE'),
            ('pet hair loss', 'PHRASE'), ('dog alopecia', 'PHRASE'), ('cat alopecia', 'PHRASE'),
            ('dog mange', 'PHRASE'), ('mange treatment', 'PHRASE'), ('veterinary hair loss', 'PHRASE'),
            ('vet hair loss', 'PHRASE'), ('dog skin hair loss', 'PHRASE')
        ]
    },
    '4. Unrelated Body Anatomy & Intimate Areas': {
        'description': 'Queries for body, pubic, nasal, or intimate hair issues.',
        'keywords': [
            ('pubic hair', 'PHRASE'), ('armpit hair', 'PHRASE'), ('underarm hair', 'PHRASE'),
            ('chest hair', 'PHRASE'), ('nose hair', 'PHRASE'), ('ear hair', 'PHRASE'),
            ('butt hair', 'PHRASE'), ('leg hair', 'PHRASE'), ('back hair', 'PHRASE'),
            ('ingrown hair', 'PHRASE'), ('ingrown hairs', 'PHRASE'), ('pubic hair loss', 'PHRASE'),
            ('vaginal hair', 'PHRASE'), ('vagina hair', 'PHRASE'), ('scrotal hair', 'PHRASE')
        ]
    },
    '5. DIY, Home Remedies & Cooking Ingredients': {
        'description': 'Users looking for free kitchen recipes, oils, and DIY concoctions.',
        'keywords': [
            ('onion juice for hair', 'PHRASE'), ('onion hair mask', 'PHRASE'), ('rosemary oil for hair', 'PHRASE'),
            ('castor oil for hair', 'PHRASE'), ('coconut oil for hair loss', 'PHRASE'), ('rice water hair', 'PHRASE'),
            ('clove water for hair', 'PHRASE'), ('garlic for hair loss', 'PHRASE'), ('fenugreek for hair', 'PHRASE'),
            ('diy hair regrowth', 'PHRASE'), ('diy hair loss', 'PHRASE'), ('homemade hair regrowth', 'PHRASE'),
            ('homemade shampoo', 'PHRASE'), ('natural home remedies for hair loss', 'PHRASE'),
            ('ayurvedic hair loss cure', 'PHRASE'), ('homeopathy hair loss cure', 'PHRASE')
        ]
    },
    '6. Retail Stores, Supermarkets & Mass Consumer Brands': {
        'description': 'Shoppers looking for cheap OTC supermarket/chemist products.',
        'keywords': [
            ('chemist warehouse hair', 'PHRASE'), ('chemist warehouse hair loss', 'PHRASE'),
            ('priceline hair', 'PHRASE'), ('priceline shampoo', 'PHRASE'),
            ('coles hair', 'PHRASE'), ('woolworths hair', 'PHRASE'),
            ('kmart hair', 'PHRASE'), ('target hair', 'PHRASE'), ('big w hair', 'PHRASE'),
            ('amazon hair regrowth', 'PHRASE'), ('ebay hair loss', 'PHRASE'), ('iherb hair', 'PHRASE'),
            ('sephora hair', 'PHRASE'), ('mecca hair', 'PHRASE'),
            ('pantene', 'PHRASE'), ('head and shoulders', 'PHRASE'), ('tresemme', 'PHRASE'),
            ('loreal elvive', 'PHRASE'), ('garnier fructis', 'PHRASE'), ('aphogee', 'PHRASE'),
            ('a ph ogee', 'PHRASE'), ('k18 hair mask', 'PHRASE'), ('k18 future iq', 'PHRASE'),
            ('olaplex no 3', 'PHRASE'), ('hairmart near me', 'PHRASE'), ('pantogar', 'PHRASE')
        ]
    },
    '7. Competitor Hair Clinics & Telehealth Platforms': {
        'description': 'Direct competitor clinic brand names with high non-converting spend.',
        'keywords': [
            ('gro clinics', 'PHRASE'), ('gro clinics perth', 'PHRASE'), ('gro hair transplant', 'PHRASE'),
            ('ashley and martin cost', 'PHRASE'), ('ashley and martin reviews', 'PHRASE'),
            ('ashley and martin scam', 'PHRASE'), ('bioscor', 'PHRASE'), ('bioscor perth', 'PHRASE'),
            ('svenson hair', 'PHRASE'), ('mosh hair', 'PHRASE'), ('getmosh', 'PHRASE'),
            ('pilot hair', 'PHRASE'), ('thepilot', 'PHRASE'), ('hims hair', 'PHRASE'),
            ('keeps hair', 'PHRASE'), ('mira clinic perth', 'PHRASE'), ('mira clinic', 'PHRASE'),
            ('este medical', 'PHRASE'), ('medihair', 'PHRASE'), ('cliniq perth', 'PHRASE'),
            ('stranature', 'PHRASE'), ('norwood clinic', 'PHRASE'), ('man cave perth', 'PHRASE'),
            ('hair doctors perth', 'PHRASE'), ('peptonik', 'PHRASE'), ('peptonix', 'PHRASE'),
            ('peptonix australia', 'PHRASE'), ('yoracare', 'PHRASE'), ('floxhair', 'PHRASE'),
            ('regrowl', 'PHRASE'), ('novocabelo', 'PHRASE'), ('novocabelohair', 'PHRASE'),
            ('rejuva como', 'PHRASE'), ('lushair', 'PHRASE'), ('pansidil', 'PHRASE')
        ]
    },
    '8. Jobs, Careers, Training & Trichology Education': {
        'description': 'Job seekers, recruiters, salary researchers, and student queries.',
        'keywords': [
            ('hair clinic jobs', 'PHRASE'), ('trichologist salary', 'PHRASE'), ('trichologist job', 'PHRASE'),
            ('hair loss consultant salary', 'PHRASE'), ('hair clinic hiring', 'PHRASE'),
            ('trichology course', 'PHRASE'), ('trichology training', 'PHRASE'), ('trichology certification', 'PHRASE'),
            ('hair loss course', 'PHRASE'), ('hair technician jobs', 'PHRASE'), ('hair transplant doctor salary', 'PHRASE'),
            ('tafe trichology', 'PHRASE'), ('hair loss internship', 'PHRASE'), ('hair clinic careers', 'PHRASE')
        ]
    },
    '9. Informational, Academic & Zero-Intent Queries': {
        'description': 'Information seekers looking for free downloads, Wikipedia, Reddit, or causal definitions.',
        'keywords': [
            ('hair loss reddit', 'PHRASE'), ('hair loss quora', 'PHRASE'), ('hair loss wikipedia', 'PHRASE'),
            ('hair loss pdf', 'PHRASE'), ('hair loss research paper', 'PHRASE'), ('hair loss forum', 'PHRASE'),
            ('hair loss scientific study', 'PHRASE'), ('definition of alopecia', 'PHRASE'),
            ('meaning of alopecia', 'PHRASE'), ('hair loss slideshare', 'PHRASE'), ('free hair transplant', 'PHRASE')
        ]
    },
    '10. Non-Target Geographies (Interstate & International)': {
        'description': 'Location-specific queries outside WA / Perth.',
        'keywords': [
            ('melbourne hair clinic', 'PHRASE'), ('hair loss clinic melbourne', 'PHRASE'), ('hair transplant melbourne', 'PHRASE'),
            ('sydney hair clinic', 'PHRASE'), ('hair loss clinic sydney', 'PHRASE'), ('hair transplant sydney', 'PHRASE'),
            ('brisbane hair clinic', 'PHRASE'), ('hair loss clinic brisbane', 'PHRASE'), ('hair transplant brisbane', 'PHRASE'),
            ('adelaide hair clinic', 'PHRASE'), ('hair loss clinic adelaide', 'PHRASE'), ('hair transplant adelaide', 'PHRASE'),
            ('gold coast hair clinic', 'PHRASE'), ('canberra hair clinic', 'PHRASE'), ('hobart hair clinic', 'PHRASE'),
            ('darwin hair clinic', 'PHRASE'), ('geelong hair clinic', 'PHRASE'), ('newcastle hair clinic', 'PHRASE'),
            ('hair transplant turkey', 'PHRASE'), ('turkey hair transplant cost', 'PHRASE'),
            ('hair transplant india', 'PHRASE'), ('hair transplant thailand', 'PHRASE'),
            ('hair transplant uk', 'PHRASE'), ('hair transplant london', 'PHRASE'),
            ('hair clinic delhi', 'PHRASE'), ('hair clinic mumbai', 'PHRASE'), ('hair clinic new zealand', 'PHRASE')
        ]
    },
    '11. TGA Compliance & High Regulatory Risk Queries': {
        'description': 'Biologicals, unapproved prescription compounds, and substances carrying TGA compliance penalties.',
        'keywords': [
            ('exosomes for hair near me', 'PHRASE'), ('exosome hair treatment near me', 'PHRASE'),
            ('dutexome', 'PHRASE'), ('dutexome hair treatment', 'PHRASE'), ('exosome therapy cost', 'PHRASE'),
            ('buy finasteride online australia', 'PHRASE'), ('cheap finasteride', 'PHRASE'),
            ('finasteride without prescription', 'PHRASE'), ('buy oral minoxidil australia', 'PHRASE'),
            ('minoxidel', 'PHRASE'), ('steroid hair loss', 'PHRASE'), ('anavar hair loss', 'PHRASE'),
            ('testosterone hair loss cycle', 'PHRASE'), ('sperm count hair loss', 'PHRASE'),
            ('finasteride erectile dysfunction', 'PHRASE'), ('dutasteride sperm count', 'PHRASE')
        ]
    },
    '12. Severe Medical, Pediatric & Oncological Conditions': {
        'description': 'Medical conditions requiring specialized hospital / oncological / infectious care.',
        'keywords': [
            ('chemotherapy hair loss', 'PHRASE'), ('chemo hair loss', 'PHRASE'), ('radiation hair loss', 'PHRASE'),
            ('cancer hair loss', 'PHRASE'), ('trichotillomania', 'PHRASE'), ('trichotillomania treatment', 'PHRASE'),
            ('cradle cap', 'PHRASE'), ('baby cradle cap', 'PHRASE'), ('head lice', 'PHRASE'), ('head lice treatment', 'PHRASE'),
            ('nits treatment', 'PHRASE'), ('ringworm scalp', 'PHRASE'), ('tinea capitis', 'PHRASE'),
            ('folliculitis decalvans', 'PHRASE'), ('lichen planopilaris', 'PHRASE'), ('frontal fibrosing alopecia', 'PHRASE')
        ]
    }
}

# 4. Integrate Existing Valid Negatives
all_master_rows = []

# Add taxonomy
for cat_name, cat_data in CATEGORIES_TAXONOMY.items():
    for kw, mt in cat_data['keywords']:
        all_master_rows.append({
            'Negative Keyword': kw,
            'Match Type': mt,
            'Category': cat_name,
            'Source': 'Forensic Query Mining (Audit)'
        })

# Add valid existing negatives
for kw, mt in existing_list_d + existing_list_r:
    if kw not in [r['Negative Keyword'] for r in all_master_rows]:
        all_master_rows.append({
            'Negative Keyword': kw,
            'Match Type': mt,
            'Category': '13. Existing Valid Account Negatives (Deduplicated)',
            'Source': 'Existing Account Negatives'
        })

df_master = pd.DataFrame(all_master_rows).drop_duplicates(subset=['Negative Keyword'])
print(f"Total Master Negative Keywords before conflict check: {len(df_master)}")

# 5. Verification: Check Against Converting Queries
conflicts = []
for idx, row in df_master.iterrows():
    neg = row['Negative Keyword']
    mt = row['Match Type']
    
    for c_query in conv_queries:
        if mt == 'EXACT':
            if neg == c_query:
                conflicts.append((neg, mt, c_query, 'Exact match conflict'))
        elif mt == 'PHRASE':
            if re.search(r'\b' + re.escape(neg) + r'\b', c_query):
                conflicts.append((neg, mt, c_query, 'Phrase match conflict'))
        elif mt == 'BROAD':
            neg_tokens = neg.split()
            if all(re.search(r'\b' + re.escape(t) + r'\b', c_query) for t in neg_tokens):
                conflicts.append((neg, mt, c_query, 'Broad match conflict'))

print(f"\nInitial conflicts found against converting queries: {len(conflicts)}")
if conflicts:
    print("Conflict samples:")
    for c in conflicts[:15]:
        print(f"  Negative '{c[0]}' ({c[1]}) conflicts with converting query: '{c[2]}'")

conflicting_kws = set([c[0] for c in conflicts])
df_master_clean = df_master[~df_master['Negative Keyword'].isin(conflicting_kws)].copy()
print(f"\nMaster Negative Keywords after conflict resolution: {len(df_master_clean)}")

def format_for_gads(row):
    kw = row['Negative Keyword']
    mt = row['Match Type']
    if mt == 'EXACT':
        return f"[{kw}]"
    elif mt == 'PHRASE':
        return f'"{kw}"'
    else:
        return kw

df_master_clean['Google Ads Formatted'] = df_master_clean.apply(format_for_gads, axis=1)

# Sort master clean by category and keyword
df_master_clean = df_master_clean.sort_values(by=['Category', 'Negative Keyword']).reset_index(drop=True)

# 6. Save Excel and CSV in data/IHLS
out_dir = r'.\data\IHLS'
excel_path = os.path.join(out_dir, 'Master_Negative_Keywords_IHLS.xlsx')
csv_path = os.path.join(out_dir, 'Master_Negative_Keywords_IHLS.csv')

# Google Ads upload format CSV (just the formatted keyword or columns: Keyword, Match type)
gads_upload_df = pd.DataFrame({
    'Negative Keyword': df_master_clean['Negative Keyword'],
    'Match Type': df_master_clean['Match Type'],
    'Google Ads Syntax': df_master_clean['Google Ads Formatted']
})
gads_upload_df.to_csv(csv_path, index=False, encoding='utf-8-sig')

# Create multi-tab Excel workbook
with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
    # Tab 1: Master Negative Keywords List
    df_master_clean[['Google Ads Formatted', 'Negative Keyword', 'Match Type', 'Category', 'Source']].to_excel(
        writer, sheet_name='Master Negative List', index=False
    )
    
    # Tab 2: Categorized Summary
    cat_summary = df_master_clean.groupby(['Category', 'Match Type']).size().unstack(fill_value=0).reset_index()
    cat_summary['Total'] = cat_summary.sum(axis=1, numeric_only=True)
    cat_summary.to_excel(writer, sheet_name='Category Summary', index=False)
    
    # Tab 3: Harmful Negatives to Remove
    df_removed_harmful.to_excel(writer, sheet_name='Harmful Negatives to Remove', index=False)
    
    # Tab 4: Top Wasted Search Terms Audited
    # Group zero-conv terms with spend >= $20
    high_waste_st = df_all[df_all['Conversions'] == 0].groupby(df_all['Search term'].str.lower().str.strip()).agg({
        'Cost': 'sum',
        'Clicks': 'sum',
        'Campaign': lambda x: ', '.join(set(x))
    }).reset_index().sort_values(by='Cost', ascending=False)
    high_waste_st.head(100).to_excel(writer, sheet_name='Top 100 Wasted Queries', index=False)
    
    # Tab 5: October 2026 Wasted Queries Audited
    oct_waste_st = df_oct[df_oct['Conversions'] == 0].groupby(df_oct['Search term'].str.lower().str.strip()).agg({
        'Cost': 'sum',
        'Clicks': 'sum',
        'Campaign': lambda x: ', '.join(set(x))
    }).reset_index().sort_values(by='Cost', ascending=False)
    oct_waste_st.head(100).to_excel(writer, sheet_name='Oct 2026 Wasted Queries', index=False)
    
    # Tab 6: Protected Converting Queries (Alpha Winners)
    conv_df.head(100).to_excel(writer, sheet_name='Protected Converting Terms', index=False)

print(f"\nSuccessfully generated Master Excel at: {excel_path}")
print(f"Successfully generated Master CSV at: {csv_path}")
print(f"Total entries in master list: {len(df_master_clean)}")
