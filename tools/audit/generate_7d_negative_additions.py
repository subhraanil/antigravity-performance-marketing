import pandas as pd
import openpyxl
import os
import shutil

out_dir = r'.\data\IHLS'
excel_path = os.path.join(out_dir, 'New_Negative_Additions_Last7Days.xlsx')
csv_path = os.path.join(out_dir, 'New_Negative_Additions_Last7Days.csv')

additions_7d = [
    # Local Perth Hair Salons (High Priority - Wasted $36+ in 7 days)
    {'Negative Keyword': 'djura', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"djura"', 'Category': 'Local Perth Salons', 'Reason': 'Djura Hair & Spa in Fremantle ($12.16 wasted in PMax)'},
    {'Negative Keyword': 'morris mead', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"morris mead"', 'Category': 'Local Perth Salons', 'Reason': 'Morris Mead Hairdressing in Perth ($7.07 wasted in PMax)'},
    {'Negative Keyword': 'floreat hair', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"floreat hair"', 'Category': 'Local Perth Salons', 'Reason': 'Floreat Hair Salon ($4.67 wasted in PMax)'},
    {'Negative Keyword': 'hair dresser', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"hair dresser"', 'Category': 'Local Perth Salons', 'Reason': 'Hairdresser searches ($6.16 wasted on "hair dresser nesr me" in Search)'},
    
    # Pet & Veterinary Medication
    {'Negative Keyword': 'meloxidyl', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"meloxidyl"', 'Category': 'Veterinary / Pet Drugs', 'Reason': 'Veterinary arthritis NSAID for dogs/cats ($18.33 wasted on 2 clicks in PMax)'},
    
    # Retail Salon Chains & E-Commerce Stores
    {'Negative Keyword': 'hairhouse', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"hairhouse"', 'Category': 'Retail Chains & Salons', 'Reason': 'Hairhouse Warehouse salon chain ($12.24 wasted in Midland/Belmont)'},
    {'Negative Keyword': 'uniwigs', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"uniwigs"', 'Category': 'Retail Wig Stores', 'Reason': 'UniWigs online e-commerce wig store ($3.80 wasted)'},
    
    # OTC Hair Supplements & Chemical Compounds
    {'Negative Keyword': 'nourkrin', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"nourkrin"', 'Category': 'OTC Supplements & Tablets', 'Reason': 'Nourkrin Man hair supplement tablets ($5.61 wasted)'},
    {'Negative Keyword': 'cecred', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"cecred"', 'Category': 'Retail Celebrity Brands', 'Reason': 'Beyoncé Cécred hair drops ($6.04 wasted in Search)'},
    {'Negative Keyword': 'gond katira', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"gond katira"', 'Category': 'DIY / Home Remedies', 'Reason': 'Edible gum DIY hair mask (unrelated herbal inquiry)'},
    {'Negative Keyword': 'ghk cu', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"ghk cu"', 'Category': 'Research Peptides / Chemicals', 'Reason': 'GHK-Cu copper peptide research chemical query'},
    {'Negative Keyword': 'dekohair', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"dekohair"', 'Category': 'OTC Retail Lotions', 'Reason': 'DekoHair OTC cosmetic hair lotion online shopping query'},
    {'Negative Keyword': 'chinamed', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"chinamed"', 'Category': 'Chinese Herbal Remedies', 'Reason': 'ChinaMed OTC herbal formula query'},
    
    # TGA Biologicals (Exosomes) - Re-affirm account-level enforcement
    {'Negative Keyword': 'exosomes', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"exosomes"', 'Category': 'TGA Compliance Hazard (Biologicals)', 'Reason': 'Exosome hair queries ($8.50 wasted in PMax; TGA biological compliance risk)'},
    {'Negative Keyword': 'exosome', 'Match Type': 'PHRASE', 'Google Ads Syntax': '"exosome"', 'Category': 'TGA Compliance Hazard (Biologicals)', 'Reason': 'Single term phrase to permanently block all exosome query bleeding in PMax'}
]

df_add = pd.DataFrame(additions_7d)
df_add.to_csv(csv_path, index=False, encoding='utf-8-sig')

with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
    df_add.to_excel(writer, sheet_name='New 7-Day Negatives', index=False)

artifact_dir = r'C:\Users\test\.gemini\antigravity\brain\df28e754-e5af-4512-9dfa-8b5ee40a4aed'
shutil.copy(excel_path, os.path.join(artifact_dir, 'New_Negative_Additions_Last7Days.xlsx'))
shutil.copy(csv_path, os.path.join(artifact_dir, 'New_Negative_Additions_Last7Days.csv'))

print("7-Day Negative Additions files created successfully!")
