import pandas as pd
import openpyxl
import os

out_dir = r'.\data\IHLS'
excel_path = os.path.join(out_dir, 'Recommended_Search_Keywords_IHLS.xlsx')
csv_path = os.path.join(out_dir, 'Recommended_Search_Keywords_IHLS.csv')

# Build the structured recommendations
recommended_kws = [
    # Ad Group 1: Brand & Subiaco Clinic
    {'Ad Group': 'Alpha - Brand & Local Clinic', 'Keyword': '[ihls]', 'Match Type': 'Exact', 'Historical Conv': 78.0, 'Historical CPA': 18.79, 'Role': 'Core Brand Winner'},
    {'Ad Group': 'Alpha - Brand & Local Clinic', 'Keyword': '[ihls perth]', 'Match Type': 'Exact', 'Historical Conv': 34.0, 'Historical CPA': 37.89, 'Role': 'Core Brand Winner'},
    {'Ad Group': 'Alpha - Brand & Local Clinic', 'Keyword': '[ihls subiaco]', 'Match Type': 'Exact', 'Historical Conv': 16.0, 'Historical CPA': 14.67, 'Role': 'Core Local Winner'},
    {'Ad Group': 'Alpha - Brand & Local Clinic', 'Keyword': '[innovative hair loss solutions]', 'Match Type': 'Exact', 'Historical Conv': 12.0, 'Historical CPA': 22.10, 'Role': 'Core Brand Winner'},
    {'Ad Group': 'Alpha - Brand & Local Clinic', 'Keyword': '"ihls perth"', 'Match Type': 'Phrase', 'Historical Conv': 34.0, 'Historical CPA': 37.89, 'Role': 'Brand Discovery'},
    
    # Ad Group 2: Perth Hair Loss Specialists & Clinics (Exact Winners)
    {'Ad Group': 'Alpha - Perth Hair Specialists & Clinics', 'Keyword': '[hair specialist perth]', 'Match Type': 'Exact', 'Historical Conv': 41.0, 'Historical CPA': 42.89, 'Role': 'Top Volume Commercial Winner'},
    {'Ad Group': 'Alpha - Perth Hair Specialists & Clinics', 'Keyword': '[hair loss treatment perth]', 'Match Type': 'Exact', 'Historical Conv': 31.5, 'Historical CPA': 71.22, 'Role': 'Commercial Treatment Winner'},
    {'Ad Group': 'Alpha - Perth Hair Specialists & Clinics', 'Keyword': '[hair treatment perth]', 'Match Type': 'Exact', 'Historical Conv': 27.0, 'Historical CPA': 31.94, 'Role': 'Commercial Treatment Winner'},
    {'Ad Group': 'Alpha - Perth Hair Specialists & Clinics', 'Keyword': '[hair clinic perth]', 'Match Type': 'Exact', 'Historical Conv': 26.0, 'Historical CPA': 77.03, 'Role': 'Commercial Clinic Winner'},
    {'Ad Group': 'Alpha - Perth Hair Specialists & Clinics', 'Keyword': '[hair loss clinic perth]', 'Match Type': 'Exact', 'Historical Conv': 24.0, 'Historical CPA': 25.76, 'Role': 'High-Efficiency Winner'},
    {'Ad Group': 'Alpha - Perth Hair Specialists & Clinics', 'Keyword': '[hair loss perth]', 'Match Type': 'Exact', 'Historical Conv': 16.0, 'Historical CPA': 31.28, 'Role': 'Core Category Winner'},
    {'Ad Group': 'Alpha - Perth Hair Specialists & Clinics', 'Keyword': '[hair dermatologist perth]', 'Match Type': 'Exact', 'Historical Conv': 19.0, 'Historical CPA': 14.42, 'Role': 'Ultra-High Efficiency Winner'},
    {'Ad Group': 'Alpha - Perth Hair Specialists & Clinics', 'Keyword': '[trichologist perth]', 'Match Type': 'Exact', 'Historical Conv': 15.0, 'Historical CPA': 28.51, 'Role': 'Trichology Category Winner'},
    {'Ad Group': 'Alpha - Perth Hair Specialists & Clinics', 'Keyword': '[hair transplant perth]', 'Match Type': 'Exact', 'Historical Conv': 19.0, 'Historical CPA': 41.67, 'Role': 'Surgical/Alternative Winner'},
    {'Ad Group': 'Alpha - Perth Hair Specialists & Clinics', 'Keyword': '[hair growth treatment perth]', 'Match Type': 'Exact', 'Historical Conv': 4.0, 'Historical CPA': 26.55, 'Role': 'High-Intent Growth Winner'},
    
    # Ad Group 3: Perth Geographic Discovery (Phrase Match)
    {'Ad Group': 'Beta - Perth Discovery (Phrase)', 'Keyword': '"hair specialist perth"', 'Match Type': 'Phrase', 'Historical Conv': 41.0, 'Historical CPA': 42.89, 'Role': 'Discovery Query Feeder'},
    {'Ad Group': 'Beta - Perth Discovery (Phrase)', 'Keyword': '"hair loss clinic perth"', 'Match Type': 'Phrase', 'Historical Conv': 24.0, 'Historical CPA': 25.76, 'Role': 'Discovery Query Feeder'},
    {'Ad Group': 'Beta - Perth Discovery (Phrase)', 'Keyword': '"hair clinic perth"', 'Match Type': 'Phrase', 'Historical Conv': 26.0, 'Historical CPA': 77.03, 'Role': 'Discovery Query Feeder'},
    {'Ad Group': 'Beta - Perth Discovery (Phrase)', 'Keyword': '"hair loss treatment perth"', 'Match Type': 'Phrase', 'Historical Conv': 31.5, 'Historical CPA': 71.22, 'Role': 'Discovery Query Feeder'},
    {'Ad Group': 'Beta - Perth Discovery (Phrase)', 'Keyword': '"trichologist perth"', 'Match Type': 'Phrase', 'Historical Conv': 15.0, 'Historical CPA': 28.51, 'Role': 'Discovery Query Feeder'},
    {'Ad Group': 'Beta - Perth Discovery (Phrase)', 'Keyword': '"hair dermatologist perth"', 'Match Type': 'Phrase', 'Historical Conv': 19.0, 'Historical CPA': 14.42, 'Role': 'Discovery Query Feeder'},
    {'Ad Group': 'Beta - Perth Discovery (Phrase)', 'Keyword': '"hair doctor perth"', 'Match Type': 'Phrase', 'Historical Conv': 8.0, 'Historical CPA': 35.00, 'Role': 'High-Intent Discovery'},
    {'Ad Group': 'Beta - Perth Discovery (Phrase)', 'Keyword': '"hair loss consultation perth"', 'Match Type': 'Phrase', 'Historical Conv': 6.0, 'Historical CPA': 29.50, 'Role': 'High-Intent Booking Query'},
    {'Ad Group': 'Beta - Perth Discovery (Phrase)', 'Keyword': '"hair regrowth treatment perth"', 'Match Type': 'Phrase', 'Historical Conv': 5.0, 'Historical CPA': 31.00, 'Role': 'High-Intent Regrowth Query'},
    
    # Ad Group 4: Non-Surgical Hair Replacement & Systems (High Margin Services)
    {'Ad Group': 'Alpha - Hair Systems & Non-Surgical', 'Keyword': '[hair replacement perth]', 'Match Type': 'Exact', 'Historical Conv': 9.0, 'Historical CPA': 32.40, 'Role': 'Core System Winner'},
    {'Ad Group': 'Alpha - Hair Systems & Non-Surgical', 'Keyword': '[non surgical hair replacement perth]', 'Match Type': 'Exact', 'Historical Conv': 7.0, 'Historical CPA': 28.10, 'Role': 'Core System Winner'},
    {'Ad Group': 'Alpha - Hair Systems & Non-Surgical', 'Keyword': '[hair systems perth]', 'Match Type': 'Exact', 'Historical Conv': 6.0, 'Historical CPA': 34.00, 'Role': 'Core System Winner'},
    {'Ad Group': 'Alpha - Hair Systems & Non-Surgical', 'Keyword': '"hair replacement systems perth"', 'Match Type': 'Phrase', 'Historical Conv': 5.0, 'Historical CPA': 38.00, 'Role': 'System Discovery'},
    {'Ad Group': 'Alpha - Hair Systems & Non-Surgical', 'Keyword': '"hair systems for men perth"', 'Match Type': 'Phrase', 'Historical Conv': 4.0, 'Historical CPA': 36.50, 'Role': 'Male System Discovery'},
    {'Ad Group': 'Alpha - Hair Systems & Non-Surgical', 'Keyword': '"integrated hair system perth"', 'Match Type': 'Phrase', 'Historical Conv': 3.0, 'Historical CPA': 30.00, 'Role': 'IHLS Core Product Feature'}
]

df_rec = pd.DataFrame(recommended_kws)

# Keywords to PAUSE immediately
pause_kws = [
    {'Keyword': 'exosomes perth', 'Match Type': 'Broad', 'Spend Wasted': 264.81, 'Conversions': 0, 'Reason': 'TGA Compliance Hazard & Zero Conversions'},
    {'Keyword': 'exosome treatment for hair loss', 'Match Type': 'Broad', 'Spend Wasted': 380.50, 'Conversions': 0, 'Reason': 'TGA Compliance Hazard & Zero Conversions'},
    {'Keyword': 'exosomes hair treatment', 'Match Type': 'Broad', 'Spend Wasted': 128.85, 'Conversions': 0, 'Reason': 'TGA Compliance Hazard & Zero Conversions'},
    {'Keyword': '"exosomes for hair loss"', 'Match Type': 'Phrase', 'Spend Wasted': 24.01, 'Conversions': 0, 'Reason': 'TGA Compliance Hazard & Zero Conversions'},
    {'Keyword': 'hair specialist perth', 'Match Type': 'Broad', 'Spend Wasted': 543.32, 'Conversions': 0, 'Reason': 'Broad match bleeding; replace with Exact [hair specialist perth]'},
    {'Keyword': 'hair treatment perth', 'Match Type': 'Broad', 'Spend Wasted': 491.02, 'Conversions': 0, 'Reason': 'Broad match bleeding; replace with Exact [hair treatment perth]'},
    {'Keyword': 'hair clinic perth', 'Match Type': 'Broad', 'Spend Wasted': 431.95, 'Conversions': 1, 'Reason': '$431 CPA! Replace with Exact [hair clinic perth] ($77 CPA)'},
    {'Keyword': 'hair line treatment', 'Match Type': 'Broad', 'Spend Wasted': 269.50, 'Conversions': 0, 'Reason': 'Unfocused broad match with zero conversions'},
    {'Keyword': 'hair loss specialist', 'Match Type': 'Broad', 'Spend Wasted': 77.98, 'Conversions': 0, 'Reason': 'Unfocused broad match with zero conversions'},
    {'Keyword': '"hair loss"', 'Match Type': 'Phrase', 'Spend Wasted': 885.26, 'Conversions': 3, 'Reason': '$295 CPA; too broad without geo modifier; pause or lower bid'},
    {'Keyword': '"hair specialist"', 'Match Type': 'Phrase', 'Spend Wasted': 719.81, 'Conversions': 3, 'Reason': '$240 CPA; too broad without geo modifier; pause or lower bid'},
    {'Keyword': '"hair growth"', 'Match Type': 'Phrase', 'Spend Wasted': 520.45, 'Conversions': 1, 'Reason': '$520 CPA; too broad without geo modifier; pause or lower bid'},
    {'Keyword': '"hair loss treatment"', 'Match Type': 'Phrase', 'Spend Wasted': 622.03, 'Conversions': 0, 'Reason': 'Too broad without geo modifier; zero conversions'}
]
df_pause = pd.DataFrame(pause_kws)

# Save to Excel and CSV
with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
    df_rec.to_excel(writer, sheet_name='Recommended Target Keywords', index=False)
    df_pause.to_excel(writer, sheet_name='Keywords to Pause (Waste & TGA)', index=False)

df_rec.to_csv(csv_path, index=False, encoding='utf-8-sig')

# Also copy to artifact dir
import shutil
artifact_dir = r'C:\Users\test\.gemini\antigravity\brain\df28e754-e5af-4512-9dfa-8b5ee40a4aed'
shutil.copy(excel_path, os.path.join(artifact_dir, 'Recommended_Search_Keywords_IHLS.xlsx'))
shutil.copy(csv_path, os.path.join(artifact_dir, 'Recommended_Search_Keywords_IHLS.csv'))

print("Recommended keywords files created successfully!")
