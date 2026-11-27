import pandas as pd

f = r'c:\Users\test\Videos\Office\data\IAOL\Search terms report.xlsx'
df = pd.read_excel(f, skiprows=2)
num_cols = ['Cost', 'Clicks', 'Conversions', 'Avg. CPC']
for c in num_cols: df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', '').str.replace(' --', '0').str.replace('--', '0').str.strip(), errors='coerce').fillna(0)
df = df[df['Search term'].notnull() & (~df['Search term'].astype(str).str.startswith('Total'))]

# Check existing negatives
neg_file = r"c:\Users\test\Videos\Office\data\IAOL\Negative keyword details report.xlsx"
df_neg = pd.read_excel(neg_file, skiprows=2)
existing_negs = set(df_neg['keyword_text'].dropna().astype(str).str.strip().str.lower().tolist())

# Look for low intent / noise queries
keywords_to_check = [
    'kaha se', 'sikhe', 'dw', 'deutsche welle', 'sppu', 'pune university', 'mumbai university',
    'duolingo', 'free', 'job', 'salary', 'syllabus', 'meaning', 'translation', 'translate',
    'kids', 'child', 'school', 'cbse', 'icse', 'exam', 'testdaf', 'goethe', 'certificate',
    'b2', 'c1', 'c2', 'tutor', 'tuition', 'youtube', 'notes', 'pdf', 'app', 'online free',
    'thane', 'navi mumbai', 'chembur', 'mira road', 'mulund', 'indiranagar'
]

print("=== CHECKING NOISE & LOW INTENT SEARCH TERMS ===")
for kw in keywords_to_check:
    matches = df[df['Search term'].astype(str).str.lower().str.contains(kw, na=False)]
    if len(matches) > 0:
        tot_spend = matches['Cost'].sum()
        tot_conv = matches['Conversions'].sum()
        print(f"Keyword '{kw}': {len(matches)} queries | Spend: Rs.{tot_spend:,.2f} | Conv: {tot_conv} | In Negs: {kw in existing_negs}")
        for _, r in matches.iterrows():
            if r['Cost'] > 0:
                print(f"   [{r['Campaign']}] '{r['Search term']}' -> Rs.{r['Cost']:.2f} | Clicks: {r['Clicks']} | Conv: {r['Conversions']}")
