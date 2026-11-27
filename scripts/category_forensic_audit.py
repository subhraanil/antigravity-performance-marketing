import pandas as pd
import numpy as np
import re
from collections import Counter

f_all = r'.\data\IHLS\Search terms report - all time.xlsx'
f_oct = r'.\data\IHLS\Search terms report.xlsx'
f_details = r'.\data\IHLS\Negative keyword details report.xlsx'
f_rep = r'.\data\IHLS\Negative keyword report.xlsx'

df_all = pd.read_excel(f_all, skiprows=2)
df_all = df_all[~df_all['Search term'].astype(str).str.startswith('Total:')].copy()

df_oct = pd.read_excel(f_oct, skiprows=2)
df_oct = df_oct[~df_oct['Search term'].astype(str).str.startswith('Total:')].copy()

for col in ['Cost', 'Conversions', 'Clicks', 'Conv. rate', 'Cost / conv.']:
    df_all[col] = pd.to_numeric(df_all[col], errors='coerce').fillna(0)
    df_oct[col] = pd.to_numeric(df_oct[col], errors='coerce').fillna(0)

# Converting search terms
conv_terms = df_all[df_all['Conversions'] > 0].groupby(df_all['Search term'].str.lower().str.strip()).agg({
    'Conversions': 'sum',
    'Cost': 'sum',
    'Clicks': 'sum'
}).reset_index()
conv_terms_dict = dict(zip(conv_terms['Search term'], conv_terms['Conversions']))
conv_terms_set = set(conv_terms['Search term'])

print(f"Total converting terms: {len(conv_terms_set)}")

# Aggregate all search terms
all_terms_agg = df_all.groupby(df_all['Search term'].str.lower().str.strip()).agg({
    'Cost': 'sum',
    'Conversions': 'sum',
    'Clicks': 'sum',
    'Campaign': lambda x: list(set(x))
}).reset_index()

all_terms_agg['Conv'] = all_terms_agg['Conversions']

# Check categories of waste
categories = {
    'Hair Removal / Electrolysis / Waxing': [
        r'\bremoval\b', r'\bremove\b', r'\belectrolysis\b', r'\bwaxing\b', r'\bdepilat\w*', r'\bipl hair\b',
        r'\blaser hair removal\b', r'\bshaving\b', r'\bepilat\w*', r'\bbrazilian\b', r'\bbikini\b'
    ],
    'Hair Salons / Barbers / Haircuts / Styling': [
        r'\bbarber\b', r'\bbarbers\b', r'\bhairdresser\b', r'\bhairdressers\b', r'\bhairdressing\b',
        r'\bhaircut\b', r'\bhaircuts\b', r'\bsalon\b', r'\bsalons\b', r'\bcoiffeur\b', r'\bcoiffure\b',
        r'\bhairmart\b', r'\bbooksy\b', r'\bfresha\b', r'\bbraid\w*', r'\bdreadlock\w*', r'\bstraightening\b',
        r'\bnanoplasty\b', r'\bkeratin\b', r'\bperm\b', r'\btaper\b', r'\bfade\b', r'\bhair dye\b',
        r'\bbleach\w*\b', r'\bcolour\w*\b', r'\bhighlight\w*\b', r'\bupdo\b', r'\bbalayage\b', r'\bweft\b'
    ],
    'Animals & Pets': [
        r'\bdog\b', r'\bdogs\b', r'\bcat\b', r'\bcats\b', r'\bpuppy\b', r'\bkitten\b', r'\bhorse\b',
        r'\bpet\b', r'\bpets\b', r'\bvet\b', r'\bveterinar\w*', r'\bmange\b', r'\bcanine\b', r'\bfeline\b'
    ],
    'Body Hair / Anatomy (Unrelated)': [
        r'\bpubic\b', r'\barmpit\b', r'\bchest hair\b', r'\bnose hair\b', r'\bleg hair\b', r'\bingrown\b',
        r'\bdown there\b', r'\bvagina\b', r'\bpenis\b', r'\btesticle\w*', r'\bbutt\b', r'\bback hair\b'
    ],
    'DIY, Home Remedies & Natural Oils': [
        r'\bonion\b', r'\brosemary\b', r'\bcastor oil\b', r'\bcoconut oil\b', r'\brice water\b',
        r'\bclove\b', r'\bgarlic\b', r'\bhomemade\b', r'\bdiy\b', r'\bhome remed\w*', r'\bnatural remed\w*',
        r'\blemon\b', r'\bfenugreek\b', r'\bayurved\w*', r'\bhomeopath\w*'
    ],
    'Retail Stores & Mass Market Products': [
        r'\bchemist warehouse\b', r'\bpriceline\b', r'\bcoles\b', r'\bwoolworths\b', r'\bkmart\b',
        r'\btarget\b', r'\bbig w\b', r'\bamazon\b', r'\bebay\b', r'\biherb\b', r'\bsephora\b', r'\bmecca\b',
        r'\bpantene\b', r'\bhead and shoulders\b', r'\btresemme\b', r'\bloreal\b', r'\bgarnier\b',
        r'\baphogee\b', r'\bk18\b', r'\bolaplex\b'
    ],
    'Jobs, Courses, Training & Careers': [
        r'\bjobs?\b', r'\bsalary\b', r'\bcareer\w*\b', r'\bhiring\b', r'\bemployment\b', r'\bcourses?\b',
        r'\btraining\b', r'\binternship\b', r'\bacadem\w*\b', r'\bresume\b', r'\bcertificat\w*\b', r'\bdegree\b', r'\btafe\b'
    ],
    'Informational & Non-Commercial': [
        r'\bmeaning\b', r'\bdefinition\b', r'\bcauses of\b', r'\bwhy is my\b', r'\breddit\b',
        r'\bquora\b', r'\bwikipedia\b', r'\bpdf\b', r'\byoutube\b', r'\bforum\b', r'\bstudy\b', r'\bfree\b'
    ],
    'Wrong Geographies (Non-WA / International)': [
        r'\bmelbourne\b', r'\bsydney\b', r'\bbrisbane\b', r'\badelaide\b', r'\bgold coast\b',
        r'\bcanberra\b', r'\bhobart\b', r'\bdarwin\b', r'\bnewcastle\b', r'\bgeelong\b', r'\bqueensland\b',
        r'\bvictoria\b', r'\bnsw\b', r'\bturkey\b', r'\bindia\b', r'\bdelhi\b', r'\bmumbai\b',
        r'\buk\b', r'\blondon\b', r'\busa\b', r'\bcanada\b', r'\bnew zealand\b', r'\bbali\b', r'\bthailand\b'
    ],
    'Competitors (Clinics / Online Telehealth)': [
        r'\bgro clinics?\b', r'\bashley\s*(and|&)?\s*martin\b', r'\bbioscor\b', r'\bsvenson\b',
        r'\bmosh\b', r'\bpilot\b', r'\bhims\b', r'\bkeeps\b', r'\bmira clinic\b', r'\beste medical\b',
        r'\bmedihair\b', r'\bcliniq\b', r'\bstranature\b', r'\bnorwood\b', r'\bman cave\b', r'\bhair doctors\b'
    ],
    'TGA High Risk & Unapproved Medical Queries': [
        r'\bexosome\w*\b', r'\bdutexome\b', r'\bfinasteride\b', r'\bdutasteride\b', r'\bminoxidil\b',
        r'\bpropecia\b', r'\brogaine\b', r'\bregaine\b', r'\bsteroid\w*\b', r'\btestosterone\b',
        r'\banavar\b', r'\bsperm\b', r'\berectile\b', r'\blibido\b'
    ],
    'Pediatric / Oncological / Severe Medical': [
        r'\bchemo\w*\b', r'\bradiation\b', r'\bcancer\b', r'\btrichotillomania\b', r'\bcradle cap\b',
        r'\blice\b', r'\bnits\b', r'\bringworm\b', r'\btinea\b', r'\bdecalvans\b', r'\bplanopilaris\b'
    ]
}

category_stats = {}
for cat, patterns in categories.items():
    combined_regex = '|'.join(patterns)
    matched = all_terms_agg[all_terms_agg['Search term'].str.contains(combined_regex, regex=True, na=False)]
    
    total_cost = matched['Cost'].sum()
    total_conv = matched['Conversions'].sum()
    conv_matching = matched[matched['Conversions'] > 0]
    non_conv_cost = matched[matched['Conversions'] == 0]['Cost'].sum()
    term_count = len(matched)
    
    category_stats[cat] = {
        'term_count': term_count,
        'total_cost': total_cost,
        'total_conv': total_conv,
        'non_conv_cost': non_conv_cost,
        'conv_term_count': len(conv_matching),
        'sample_converting': conv_matching[['Search term', 'Conversions', 'Cost']].head(3).to_dict('records') if len(conv_matching) > 0 else []
    }

print("\n=== CATEGORY FORENSIC AUDIT ===")
for cat, stats in category_stats.items():
    print(f"\n[{cat}]")
    print(f"  Terms: {stats['term_count']} | Total Cost: ${stats['total_cost']:.2f} | Conversions: {stats['total_conv']:.2f}")
    print(f"  Wasted Cost (0 conversions): ${stats['non_conv_cost']:.2f}")
    if stats['conv_term_count'] > 0:
        print(f"  WARNING: {stats['conv_term_count']} converting terms matched pattern: {stats['sample_converting']}")
