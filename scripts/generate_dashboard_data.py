import pandas as pd
import json
import os

def analyze_and_export():
    excel_path = r'c:\Users\test\Videos\Office\data\kuri-users-2026-08-19.xlsx'
    csv_path = r'c:\Users\test\Videos\Office\data\kuri-users-2026-08-19.csv'
    cache_path = r'c:\Users\test\Videos\Office\data\pincode_cache.json'
    out_json = r'c:\Users\test\Videos\Office\data\dashboard_data.json'

    if os.path.exists(excel_path):
        df = pd.read_excel(excel_path)
    elif os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        raise FileNotFoundError("No data source file found!")

    # Clean column names
    df.columns = [c.strip() for c in df.columns]

    # Name cleanup
    if 'name' in df.columns:
        df['name'] = df['name'].fillna('').astype(str).str.strip()
    elif 'first name' in df.columns:
        df['name'] = (df['first name'].fillna('').astype(str) + ' ' + df['last name'].fillna('').astype(str)).str.strip()

    df['name'] = df['name'].replace('', 'Anonymous User')
    df['email'] = df['email'].fillna('N/A').astype(str).str.strip()
    df['phone'] = df['phone'].fillna(0).astype(str).str.replace(r'\.0$', '', regex=True)

    # Pincode cleanup
    df['pincode_str'] = df['pincode'].fillna(0).astype(int).astype(str).str.zfill(6)
    df.loc[df['pincode_str'] == '000000', 'pincode_str'] = 'N/A'

    # Load pincode cache
    pc = {}
    if os.path.exists(cache_path):
        with open(cache_path, 'r', encoding='utf-8') as f:
            pc = json.load(f)

    # Clean & standardize City
    def resolve_city(row):
        explicit_city = str(row.get('city', '')).strip()
        if explicit_city and explicit_city.lower() not in ['nan', 'none', '', 'null', 'n/a']:
            # Standardize common variations
            c_low = explicit_city.lower()
            if 'bangalore' in c_low or 'bengaluru' in c_low:
                return 'Bengaluru'
            elif 'mumbai' in c_low or 'thane' in c_low:
                return 'Mumbai (MMR)'
            elif 'delhi' in c_low or 'new delhi' in c_low:
                return 'Delhi (NCR)'
            elif 'hyderabad' in c_low or 'rangareddy' in c_low:
                return 'Hyderabad'
            elif 'pune' in c_low:
                return 'Pune'
            elif 'gurgaon' in c_low or 'gurugram' in c_low:
                return 'Gurugram (NCR)'
            elif 'noida' in c_low or 'ghaziabad' in c_low:
                return 'Noida / Ghaziabad (NCR)'
            elif 'chennai' in c_low:
                return 'Chennai'
            elif 'kolkata' in c_low:
                return 'Kolkata'
            elif 'ahmedabad' in c_low:
                return 'Ahmedabad'
            return explicit_city.title()
        
        # Fallback to pincode cache
        pin = row.get('pincode_str', 'N/A')
        return pc.get(pin, {}).get('city', 'Unknown')

    df['city_clean'] = df.apply(resolve_city, axis=1)
    df['district'] = df['pincode_str'].apply(lambda x: pc.get(x, {}).get('district', 'N/A'))
    df['state_clean'] = df.apply(lambda r: str(r.get('state', '')).title() if str(r.get('state', '')).lower() not in ['nan', '', 'none'] else pc.get(r.get('pincode_str', ''), {}).get('state', 'N/A'), axis=1)

    # Auth Provider
    df['authProvider'] = df['authProvider'].fillna('Unknown').astype(str).str.title()
    auth_counts = df['authProvider'].value_counts().to_dict()

    # Dates & Monthly Trends
    df['createdAt_dt'] = pd.to_datetime(df['createdAt'], errors='coerce')
    df['lastOrderAt_dt'] = pd.to_datetime(df['lastOrderAt'], errors='coerce')

    df['created_month'] = df['createdAt_dt'].dt.strftime('%Y-%m').fillna('Unknown')
    monthly_acquisitions = df[df['created_month'] != 'Unknown']['created_month'].value_counts().sort_index().to_dict()

    df['order_month'] = df['lastOrderAt_dt'].dt.strftime('%Y-%m').fillna('Unknown')
    monthly_revenue = df[df['order_month'] != 'Unknown'].groupby('order_month')['totalSpend'].sum().to_dict()

    # Funnel Tracking
    started_checkout = int(df['checkoutStartedAt'].notnull().sum()) if 'checkoutStartedAt' in df.columns else 0
    completed_checkout = int(df['checkoutCompletedAt'].notnull().sum()) if 'checkoutCompletedAt' in df.columns else 0
    abandoned_checkout = int(started_checkout - completed_checkout)

    # KPIs
    total_users = int(len(df))
    total_spend = int(df['totalSpend'].sum())
    total_orders = int(df['totalOrders'].sum())
    active_buyers = int((df['totalOrders'] > 0).sum())
    repeat_buyers = int((df['totalOrders'] >= 2).sum())
    non_buyers = int((df['totalOrders'] == 0).sum())
    avg_aov = round(float(df[df['totalOrders'] > 0]['averageOrderValue'].mean()), 2) if active_buyers > 0 else 0

    users_with_cart = int((df['cartItemCount'] > 0).sum())
    total_cart_items = int(df['cartItemCount'].sum())
    high_intent_abandoners = int(((df['totalOrders'] == 0) & (df['cartItemCount'] > 0)).sum())

    users_with_wishlist = int((df['wishlistItemCount'] > 0).sum())
    total_wishlist_items = int(df['wishlistItemCount'].sum())

    # Order Breakdown
    order_dist = df['totalOrders'].value_counts().sort_index().to_dict()
    order_breakdown = {
        '0 Orders': int(order_dist.get(0, 0)),
        '1 Order': int(order_dist.get(1, 0)),
        '2 Orders': int(order_dist.get(2, 0)),
        '3 Orders': int(order_dist.get(3, 0)),
        '4+ Orders': int(sum(v for k, v in order_dist.items() if k >= 4))
    }

    # Spend Segments
    def spend_tier(spend):
        if spend == 0:
            return '₹0 (Non-Spender)'
        elif spend < 500:
            return '₹1 - ₹499 (Low)'
        elif spend < 1500:
            return '₹500 - ₹1,499 (Medium)'
        elif spend < 3000:
            return '₹1,500 - ₹2,999 (High)'
        else:
            return '₹3,000+ (VIP)'

    df['spend_tier'] = df['totalSpend'].apply(spend_tier)
    spend_tier_counts = df['spend_tier'].value_counts().to_dict()

    # City Stats
    city_stats = df.groupby('city_clean').agg(
        user_count=('name', 'count'),
        total_revenue=('totalSpend', 'sum'),
        total_orders=('totalOrders', 'sum'),
        cart_users=('cartItemCount', lambda x: (x > 0).sum())
    ).reset_index().rename(columns={'city_clean': 'city'}).sort_values(by='total_orders', ascending=False).to_dict(orient='records')

    # Top Pincodes Stats (excluding N/A)
    pincode_df = df[df['pincode_str'] != 'N/A']
    pincode_stats = pincode_df.groupby(['pincode_str', 'district', 'city_clean']).agg(
        user_count=('name', 'count'),
        total_revenue=('totalSpend', 'sum'),
        total_orders=('totalOrders', 'sum')
    ).reset_index().rename(columns={'city_clean': 'city'}).sort_values(by='total_orders', ascending=False).head(25).to_dict(orient='records')

    # Top VIP Spenders
    top_spenders = df.sort_values(by='totalSpend', ascending=False).head(15)[[
        'name', 'email', 'phone', 'pincode_str', 'city_clean', 'district', 'totalOrders', 'totalSpend', 'averageOrderValue', 'cartItemCount'
    ]].rename(columns={'pincode_str': 'pincode', 'city_clean': 'city'}).to_dict(orient='records')

    # Customer Records
    records = []
    for _, row in df.iterrows():
        records.append({
            'name': row['name'],
            'email': row['email'],
            'phone': row['phone'] if row['phone'] != '0' else 'N/A',
            'auth': row['authProvider'],
            'pincode': row['pincode_str'],
            'city': row['city_clean'],
            'district': row['district'],
            'state': row['state_clean'],
            'orders': int(row['totalOrders']),
            'spend': int(row['totalSpend']),
            'aov': round(float(row['averageOrderValue']), 2),
            'cart': int(row['cartItemCount']),
            'wishlist': int(row['wishlistItemCount']),
            'tier': row['spend_tier'],
            'joined': str(row['createdAt'])[:10] if pd.notnull(row['createdAt']) else 'N/A'
        })

    payload = {
        'kpis': {
            'total_users': total_users,
            'total_spend': total_spend,
            'total_orders': total_orders,
            'avg_aov': avg_aov,
            'active_buyers': active_buyers,
            'repeat_buyers': repeat_buyers,
            'non_buyers': non_buyers,
            'users_with_cart': users_with_cart,
            'total_cart_items': total_cart_items,
            'high_intent_abandoners': high_intent_abandoners,
            'users_with_wishlist': users_with_wishlist,
            'total_wishlist_items': total_wishlist_items,
            'started_checkout': started_checkout,
            'completed_checkout': completed_checkout,
            'abandoned_checkout': abandoned_checkout,
            'top_city': city_stats[0]['city'] if city_stats else 'N/A',
            'top_city_orders': city_stats[0]['total_orders'] if city_stats else 0
        },
        'auth_counts': auth_counts,
        'monthly_acquisitions': monthly_acquisitions,
        'monthly_revenue': monthly_revenue,
        'order_breakdown': order_breakdown,
        'spend_tiers': spend_tier_counts,
        'city_stats': city_stats,
        'pincode_stats': pincode_stats,
        'top_spenders': top_spenders,
        'users': records
    }

    os.makedirs(os.path.dirname(out_json), exist_ok=True)
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2)

    print(f"Excel Data exported successfully to {out_json}")
    print(f"Summary: {total_users} users, Rs.{total_spend:,} revenue, {total_orders} orders.")

if __name__ == '__main__':
    analyze_and_export()
