import pandas as pd
import openpyxl
import os
import shutil

out_dir = r'.\data\IHLS'
os.makedirs(out_dir, exist_ok=True)
excel_path = os.path.join(out_dir, 'New_Negative_Additions_Last30Days.xlsx')
csv_path = os.path.join(out_dir, 'New_Negative_Additions_Last30Days.csv')

additions_30d = [
    # 1. Retail Products, Gadgets & Home Remedies
    {'Negative Keyword': 'organicbeautytransformation', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"organicbeautytransformation"', 'Category': 'Retail & Competitor URLs', 'Reason': 'URL/brand search "neet mann organicbeautytransformation" ($10.34 wasted)'},
    {'Negative Keyword': 'neet mann', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"neet mann"', 'Category': 'Retail & Competitor URLs', 'Reason': 'Specific influencer/brand query ($10.34 wasted)'},
    {'Negative Keyword': 'arata', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"arata"', 'Category': 'OTC Retail Products', 'Reason': 'Arata Mito Active retail hair product ($9.89 wasted)'},
    {'Negative Keyword': 'lumicub', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"lumicub"', 'Category': 'Retail Laser Gadgets', 'Reason': 'Lumicub red light laser helmet ($9.78 wasted)'},
    {'Negative Keyword': 'force factor', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"force factor"', 'Category': 'OTC Supplements', 'Reason': 'Force Factor hair growth accelerator ($10.05 wasted)'},
    {'Negative Keyword': 'nordic biolabs', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"nordic biolabs"', 'Category': 'Retail Subscription Brands', 'Reason': 'Scandinavian hair serum brand ($4.22 wasted)'},
    {'Negative Keyword': 'cystiphane', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"cystiphane"', 'Category': 'OTC Pharmacy Supplements', 'Reason': 'Cystiphane Biorga hair supplement ($3.85 wasted)'},
    {'Negative Keyword': 'bay leaf', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"bay leaf"', 'Category': 'DIY / Home Remedies', 'Reason': 'Cooking bay leaf hair growth recipe ($3.80 wasted on 2 clicks)'},
    {'Negative Keyword': 'head tapping', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"head tapping"', 'Category': 'DIY Tools & Gadgets', 'Reason': 'Head tapping tool gadget ($2.45 wasted)'},
    {'Negative Keyword': 'olivia quido', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"olivia quido"', 'Category': 'Unrelated Cosmetics', 'Reason': 'Sunscreen brand search ($1.31 wasted)'},
    {'Negative Keyword': 'md hair', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"md hair"', 'Category': 'Competitor Subscription Products', 'Reason': 'MDhair retail custom kit ($2.13 wasted)'},
    
    # 2. Injections & Biologicals (High Risk & Unrelated)
    {'Negative Keyword': 'polynucleotides', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"polynucleotides"', 'Category': 'Cosmetic Injections (Non-Core)', 'Reason': 'Polynucleotide salmon DNA skin booster injection ($9.92 wasted)'},
    {'Negative Keyword': 'hair injections', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"hair injections"', 'Category': 'Injections / Steroids', 'Reason': 'Hair injections for hair growth query ($12.43 wasted)'},
    {'Negative Keyword': 'vesicles', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"vesicles"', 'Category': 'Biologicals / Exosomes', 'Reason': 'Extracellular vesicles biological term ($0.66 wasted)'},
    
    # 3. Local Perth Salons & Hairdressers
    {'Negative Keyword': 'velona', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"velona"', 'Category': 'Local Perth Salons', 'Reason': 'Velona Hair Design in Subiaco/Perth'},
    {'Negative Keyword': 'miss paris', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"miss paris"', 'Category': 'Local Perth Salons', 'Reason': 'Miss Paris Hair Studio Victoria Park'},
    {'Negative Keyword': 'djura', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"djura"', 'Category': 'Local Perth Salons', 'Reason': 'Djura Hair & Spa in Fremantle ($12.16 wasted)'},
    {'Negative Keyword': 'morris mead', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"morris mead"', 'Category': 'Local Perth Salons', 'Reason': 'Morris Mead Hairdressing in Perth ($7.07 wasted)'},
    {'Negative Keyword': 'floreat hair', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"floreat hair"', 'Category': 'Local Perth Salons', 'Reason': 'Floreat Hair Salon ($4.67 wasted)'},
    {'Negative Keyword': 'hairhouse', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"hairhouse"', 'Category': 'Retail Chains & Salons', 'Reason': 'Hairhouse Warehouse salon chain ($14.42 wasted)'},
    
    # 4. Competitor Misspellings & Telehealth
    {'Negative Keyword': 'ashley n martin', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"ashley n martin"', 'Category': 'Competitor Clinics', 'Reason': 'Misspelling of Ashley & Martin ($7.48 wasted)'},
    {'Negative Keyword': 'peptonix', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"peptonix"', 'Category': 'Competitor Clinics', 'Reason': 'Peptonix hair clinic ($11.76 wasted)'},
    {'Negative Keyword': 'absci', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"absci"', 'Category': 'Biotech / Pharma Research', 'Reason': 'Absci research query ($11.21 wasted)'},
    {'Negative Keyword': 'rejuva', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"rejuva"', 'Category': 'Cosmetic & Aesthetic Clinics', 'Reason': 'Rejuva cosmetic clinic in Como ($19.40 wasted)'},
    {'Negative Keyword': 'luume', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"luume"', 'Category': 'Cosmetic & Aesthetic Clinics', 'Reason': 'Luume Aesthetics cosmetic injector clinic ($11.13 wasted)'},
    
    # 5. Non-English & International Queries
    {'Negative Keyword': '美容 室', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"美容 室"', 'Category': 'Non-English / Foreign Salon', 'Reason': 'Japanese for "beauty salon" ($6.13 wasted)'},
    {'Negative Keyword': 'haartransplantatie', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"haartransplantatie"', 'Category': 'Non-English / International', 'Reason': 'Dutch for "hair transplant" ($9.89 wasted)'},
    {'Negative Keyword': 'saç ekimi', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"saç ekimi"', 'Category': 'Non-English / Turkey Transplant', 'Reason': 'Turkish for "hair transplant" ($2.97 wasted)'},
    
    # 6. Pet / Veterinary & GLP-1 Weight Loss Drugs
    {'Negative Keyword': 'meloxidyl', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"meloxidyl"', 'Category': 'Veterinary Drugs', 'Reason': 'Veterinary arthritis painkiller for dogs/cats ($18.33 wasted)'},
    {'Negative Keyword': 'mounjaro', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"mounjaro"', 'Category': 'GLP-1 Weight Loss Drugs', 'Reason': 'Weight loss injection hair shedding query ($11.56 wasted)'},
    {'Negative Keyword': 'ozempic', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"ozempic"', 'Category': 'GLP-1 Weight Loss Drugs', 'Reason': 'Weight loss injection hair shedding query'},
    {'Negative Keyword': 'wegovy', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"wegovy"', 'Category': 'GLP-1 Weight Loss Drugs', 'Reason': 'Weight loss injection hair shedding query'}
]

df_add = pd.DataFrame(additions_30d)
df_add.to_csv(csv_path, index=False, encoding='utf-8-sig')

with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
    df_add.to_excel(writer, sheet_name='New 30-Day Negatives', index=False)

# Copy to brain artifact directory as well
artifact_dir = r'C:\Users\test\.gemini\antigravity\brain\df28e754-e5af-4512-9dfa-8b5ee40a4aed'
shutil.copy(excel_path, os.path.join(artifact_dir, 'New_Negative_Additions_Last30Days.xlsx'))
shutil.copy(csv_path, os.path.join(artifact_dir, 'New_Negative_Additions_Last30Days.csv'))

print(f"Generated {len(df_add)} new negative keywords for 30-day report!")
