import pandas as pd
import openpyxl
import os
import shutil

out_dir = r'.\data\IHLS'
excel_path = os.path.join(out_dir, 'New_Negative_Additions_Last14Days.xlsx')
csv_path = os.path.join(out_dir, 'New_Negative_Additions_Last14Days.csv')

additions = [
    {'Negative Keyword': 'mounjaro', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"mounjaro"', 'Category': 'GLP-1 / Weight Loss Drugs', 'Reason': 'Hair loss side effect queries from weight loss injections ($11.56 wasted)'},
    {'Negative Keyword': 'ozempic', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"ozempic"', 'Category': 'GLP-1 / Weight Loss Drugs', 'Reason': 'GLP-1 weight loss drug shedding queries'},
    {'Negative Keyword': 'wegovy', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"wegovy"', 'Category': 'GLP-1 / Weight Loss Drugs', 'Reason': 'GLP-1 weight loss drug shedding queries'},
    {'Negative Keyword': 'meloxidyl', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"meloxidyl"', 'Category': 'Veterinary / Pet Drugs', 'Reason': 'Dog/cat arthritis painkiller ($18.33 wasted on 2 clicks)'},
    {'Negative Keyword': 'hairhouse', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"hairhouse"', 'Category': 'Retail Salons & Chains', 'Reason': 'Hairhouse Warehouse salon & body piercing store ($14.42 wasted)'},
    {'Negative Keyword': 'bouf', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"bouf"', 'Category': 'Local Hair Salons (Subiaco)', 'Reason': 'Bouf Hair Salon in Subiaco ($8.79 wasted)'},
    {'Negative Keyword': 'jamie lee hair', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"jamie lee hair"', 'Category': 'Local Hair Salons (Perth)', 'Reason': 'Hairdressing salon ($10.89 wasted)'},
    {'Negative Keyword': 'cecred', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"cecred"', 'Category': 'Celebrity / Retail Hair Brands', 'Reason': 'Beyonce retail hair product line ($6.04 wasted)'},
    {'Negative Keyword': 'zova', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"zova"', 'Category': 'Competitor Products', 'Reason': 'Zova hair product queries ($20.91 wasted)'},
    {'Negative Keyword': 'absci', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"absci"', 'Category': 'Biotech / Pharma Research', 'Reason': 'Biotech drug research query ($11.21 wasted)'},
    {'Negative Keyword': 'rejuva', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"rejuva"', 'Category': 'Aesthetic & Injector Clinics', 'Reason': 'Rejuva cosmetic clinic in Como ($19.40 wasted)'},
    {'Negative Keyword': 'luume', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"luume"', 'Category': 'Aesthetic & Injector Clinics', 'Reason': 'Luume Aesthetics cosmetic injector clinic ($11.13 wasted)'},
    {'Negative Keyword': 'elevated aesthetics', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"elevated aesthetics"', 'Category': 'Aesthetic & Injector Clinics', 'Reason': 'Cosmetic aesthetics clinic ($5.75 wasted)'},
    {'Negative Keyword': 'treatment', 'Match Type': 'EXACT', 'Google Ads Syntax': '[treatment]', 'Category': 'Broad Match Trap', 'Reason': 'Prevents Broad match from bidding $14.60 on the single word "treatment"'},
    {'Negative Keyword': 'dermatology', 'Match Type': 'EXACT', 'Google Ads Syntax': '[dermatology]', 'Category': 'Broad Match Trap', 'Reason': 'Prevents Broad match from bidding on standalone single word "dermatology"'},
    {'Negative Keyword': 'fue clinics perth', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"fue clinics perth"', 'Category': 'Surgical Hair Transplants', 'Reason': 'Surgical transplant clinics ($22.80 wasted in 14d)'},
    {'Negative Keyword': 'fue clinics', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"fue clinics"', 'Category': 'Surgical Hair Transplants', 'Reason': 'Surgical FUE transplant clinics'}
]

df_add = pd.DataFrame(additions)
df_add.to_csv(csv_path, index=False, encoding='utf-8-sig')

with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
    df_add.to_excel(writer, sheet_name='New Negatives to Add', index=False)

artifact_dir = r'C:\Users\test\.gemini\antigravity\brain\df28e754-e5af-4512-9dfa-8b5ee40a4aed'
shutil.copy(excel_path, os.path.join(artifact_dir, 'New_Negative_Additions_Last14Days.xlsx'))
shutil.copy(csv_path, os.path.join(artifact_dir, 'New_Negative_Additions_Last14Days.csv'))

print("New 14-day negative additions generated successfully!")
