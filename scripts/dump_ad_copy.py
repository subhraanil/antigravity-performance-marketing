import pandas as pd

f_ad = r'c:\Users\test\Videos\Office\data\IAOL\Ad report (2).xlsx'
df_ad = pd.read_excel(f_ad, skiprows=2)
df_ad = df_ad[df_ad['Campaign'].notnull() & (df_ad['Campaign'] != '--') & (df_ad['Ad group'].notnull())]

for idx, r in df_ad.iterrows():
    print(f"\n=======================================================")
    print(f"AD #{idx} | Campaign: {r['Campaign']} | Ad Group: {r['Ad group']}")
    print(f"Metrics: Clicks={r['Clicks']} | Impr={r['Impr.']} | CPC={r['Avg. CPC']} | Cost={r['Cost']} | Conv={r['Conversions']} | Cost/Conv={r['Cost / conv.']}")
    print(f"URL: {r['Final URL']}")
    print("Headlines:")
    for i in range(1, 16):
        h = r.get(f'Headline {i}')
        pos = r.get(f'Headline {i} position')
        if pd.notnull(h) and str(h).strip() not in ['--', 'nan', '']:
            pin_str = f" [Pinned: {pos}]" if pd.notnull(pos) and str(pos).strip() not in ['--', 'nan', ''] else ""
            print(f"  H{i}: {h}{pin_str}")
    print("Descriptions:")
    for i in range(1, 5):
        d = r.get(f'Description {i}')
        pos = r.get(f'Description {i} position')
        if pd.notnull(d) and str(d).strip() not in ['--', 'nan', '']:
            pin_str = f" [Pinned: {pos}]" if pd.notnull(pos) and str(pos).strip() not in ['--', 'nan', ''] else ""
            print(f"  D{i}: {d}{pin_str}")
