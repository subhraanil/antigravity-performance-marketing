import pandas as pd

df = pd.read_csv('scripts/fb_google_sheet_export.csv')
for col in df.columns:
    if df[col].dtype == object:
        df[col] = df[col].astype(str).str.replace('₹', '').str.replace(',', '').str.strip()

for col in ['Impression', 'Clicks', 'Leads', 'Cost']:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# Compare Oct 1 to Oct 22 vs Oct 23 to Nov 4
df['Date_dt'] = pd.to_datetime(df['Date'], format='%d-%b-%Y', errors='coerce')

period1 = df[(df['Date_dt'] >= '2026-10-01') & (df['Date_dt'] <= '2026-10-22')]
period2 = df[(df['Date_dt'] >= '2026-10-23') & (df['Date_dt'] <= '2026-11-04')]

print("=== PERIOD 1: Oct 1 - Oct 22 (22 days) ===")
cost1 = period1['Cost'].sum()
leads1 = period1['Leads'].sum()
clicks1 = period1['Clicks'].sum()
imps1 = period1['Impression'].sum()
print(f"Cost: Rs {cost1:.2f} (Daily: Rs {cost1/22:.2f})")
print(f"Clicks: {clicks1} (Daily: {clicks1/22:.1f})")
print(f"Impressions: {imps1} (Daily: {imps1/22:.1f})")
print(f"Leads: {leads1} (Daily: {leads1/22:.2f})")
print(f"Avg CPC: Rs {cost1/clicks1:.2f}")
print(f"Avg CTR: {(clicks1/imps1)*100:.2f}%")
print(f"CvR: {(leads1/clicks1)*100:.2f}%")
print(f"CPA: Rs {cost1/leads1:.2f}")

print("\n=== PERIOD 2: Oct 23 - Nov 4 (13 days) ===")
cost2 = period2['Cost'].sum()
leads2 = period2['Leads'].sum()
clicks2 = period2['Clicks'].sum()
imps2 = period2['Impression'].sum()
print(f"Cost: Rs {cost2:.2f} (Daily: Rs {cost2/13:.2f})")
print(f"Clicks: {clicks2} (Daily: {clicks2/13:.1f})")
print(f"Impressions: {imps2} (Daily: {imps2/13:.1f})")
print(f"Leads: {leads2} (Daily: {leads2/13:.2f})")
print(f"Avg CPC: Rs {cost2/clicks2:.2f}")
print(f"Avg CTR: {(clicks2/imps2)*100:.2f}%")
print(f"CvR: {(leads2/clicks2)*100:.2f}%")
print(f"CPA: Rs {cost2/leads2:.2f}")
