import urllib.request
import pandas as pd

url = 'https://docs.google.com/spreadsheets/d/1crkBH4x06SUx1GXE72ErKsVPq36U5kfJu9MczHE_NGg/export?format=csv&gid=1779414189'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as resp:
        content = resp.read().decode('utf-8')
    with open('scripts/fb_google_sheet_export.csv', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Saved Google Sheet to scripts/fb_google_sheet_export.csv successfully.")
    
    df = pd.read_csv('scripts/fb_google_sheet_export.csv')
    print("Shape:", df.shape)
    print("Columns:", [str(c) for c in df.columns[:10]])
    print(df.tail(15).to_string())
except Exception as e:
    print("Error:", e)
