import json
import pandas as pd

with open('data/dashboard_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=== GOOGLE ANALYTICS & E-COMMERCE SUMMARY DATA FOR FABB6 ===")
print("\n--- Core KPIs ---")
for k, v in data['kpis'].items():
    print(f"  {k}: {v}")

print("\n--- Authentication / Traffic Source Counts ---")
for k, v in data['auth_counts'].items():
    print(f"  {k}: {v}")

print("\n--- Monthly User Acquisitions ---")
for k, v in data['monthly_acquisitions'].items():
    print(f"  {k}: {v}")

print("\n--- Monthly Revenue (INR) ---")
for k, v in data['monthly_revenue'].items():
    print(f"  {k}: Rs. {v:,.2f}")

print("\n--- Order Breakdown (Customer Loyalty) ---")
for k, v in data['order_breakdown'].items():
    print(f"  {k}: {v} users")

print("\n--- Top Cities by Traffic & Orders ---")
city_df = pd.DataFrame(data['city_stats'])
print(city_df.head(10).to_string(index=False))

print("\n--- Top Pincodes by Traffic & Orders ---")
pin_df = pd.DataFrame(data['pincode_stats'])
print(pin_df.head(10).to_string(index=False))
