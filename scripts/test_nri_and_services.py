import pandas as pd
import numpy as np

path = r'C:\Users\test\Videos\Office\data\Share Samadhan\All_Enquiry_List_2026.11.23.06.28.18.csv'
df = pd.read_csv(path, low_memory=False)

def check_nri(row):
    # Check NRI landing page
    if str(row['Source']).strip() == 'NRI Landing Page':
        return True, 'NRI Landing Page'
    
    # Check text fields for nri keyword
    for col in ['Campaign Name', 'Campaign Source', 'Reference']:
        val = str(row[col]).lower()
        if 'nri' in val:
            return True, f'{col}: NRI'
            
    # Check Country Code
    raw_cc = str(row['Country Code']).strip().replace('+', '')
    if pd.notna(row['Country Code']) and raw_cc not in ['', 'nan', 'none']:
        # India is 91. Note: sometimes 91 is entered as 919879885902 (full phone)
        if raw_cc == '91' or (raw_cc.startswith('91') and len(raw_cc) > 9):
            return False, 'India'
        else:
            return True, f'Country Code: +{raw_cc}'
            
    # Check City if international
    city = str(row['City']).strip().lower()
    intl_cities = ['dubai', 'london', 'singapore', 'new york', 'california', 'texas', 'sydney', 'toronto', 'melbourne', 'sharjah', 'abu dhabi', 'doha', 'riyadh', 'kuwait', 'muscat', 'chicago', 'houston', 'fremont', 'new jersey']
    for ic in intl_cities:
        if ic in city:
            return True, f'City: {city}'
            
    return False, 'India / Domestic'

res = df.apply(check_nri, axis=1)
df['Is_NRI'] = [r[0] for r in res]
df['NRI_Reason'] = [r[1] for r in res]

print(f"Total NRI Leads: {df['Is_NRI'].sum():,} ({df['Is_NRI'].sum()/len(df)*100:.2f}%)")
print("\nNRI Leads by Reason/Origin:")
print(df[df['Is_NRI']]['NRI_Reason'].value_counts().head(20))
