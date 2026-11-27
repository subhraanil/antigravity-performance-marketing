import pandas as pd
import json
import os
import urllib.request
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# Standard fallback mapping by 2-digit PIN prefix
PREFIX_MAP = {
    '11': ('Delhi', 'Delhi / NCR'),
    '12': ('Gurugram / HR', 'Delhi / NCR'),
    '13': ('Haryana', 'North Region'),
    '14': ('Punjab', 'North Region'),
    '16': ('Chandigarh', 'North Region'),
    '20': ('Noida / Ghaziabad', 'Delhi / NCR'),
    '22': ('Lucknow', 'Lucknow / UP'),
    '24': ('Bareilly / UP', 'Uttar Pradesh'),
    '30': ('Jaipur', 'Jaipur / Rajasthan'),
    '38': ('Ahmedabad', 'Ahmedabad / Gujarat'),
    '40': ('Mumbai', 'Mumbai / MMR'),
    '41': ('Pune', 'Pune / MH'),
    '42': ('Thane / Nashik', 'Mumbai / MMR'),
    '50': ('Hyderabad', 'Hyderabad / TS'),
    '56': ('Bengaluru', 'Bengaluru / KA'),
    '57': ('Mysuru / KA', 'Karnataka'),
    '60': ('Chennai', 'Chennai / TN'),
    '68': ('Kochi / KL', 'Kerala'),
    '70': ('Kolkata', 'Kolkata / WB'),
    '78': ('Guwahati / AS', 'Assam / NE'),
}

cache_lock = threading.Lock()

def get_fallback(pin):
    prefix = pin[:2] if len(pin) >= 2 else ''
    dist, city = PREFIX_MAP.get(prefix, ('Unknown District', 'Other'))
    return {
        'district': dist,
        'state': 'India',
        'locality': f'PIN {pin}',
        'city': city
    }

def fetch_pincode_info(pin):
    if not pin or pin == '000000' or pin == 'N/A' or len(pin) < 6:
        return pin, {'district': 'N/A', 'state': 'N/A', 'locality': 'N/A', 'city': 'Unknown / Missing'}
    
    url = f'https://api.postalpincode.in/pincode/{pin}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=1.5) as resp:
            data = json.loads(resp.read().decode())
            if data and data[0].get('Status') == 'Success':
                po = data[0]['PostOffice'][0]
                district = po.get('District', 'Unknown')
                state = po.get('State', 'Unknown')
                locality = po.get('Name', 'Unknown')
                
                city = district
                if 'Bangalore' in district or 'Bengaluru' in district:
                    city = 'Bengaluru'
                elif 'Mumbai' in district or 'Thane' in district:
                    city = 'Mumbai (MMR)'
                elif 'Delhi' in district:
                    city = 'Delhi (NCR)'
                elif 'Hyderabad' in district or 'Rangareddy' in district:
                    city = 'Hyderabad'
                elif 'Pune' in district:
                    city = 'Pune'
                elif 'Gurgaon' in district or 'Gautam Buddha Nagar' in district:
                    city = 'Delhi / NCR (Noida/Gurugram)'

                return pin, {
                    'district': district,
                    'state': state,
                    'locality': locality,
                    'city': city
                }
    except Exception:
        pass
    
    return pin, get_fallback(pin)

def run_enrichment():
    csv_path = r'c:\Users\test\Videos\Office\data\kuri-users-2026-08-19.csv'
    cache_path = r'c:\Users\test\Videos\Office\data\pincode_cache.json'

    df = pd.read_csv(csv_path)
    pins = df['pincode'].fillna(0).astype(int).astype(str).str.zfill(6).unique().tolist()
    
    cache = {}
    if os.path.exists(cache_path):
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                cache = json.load(f)
        except Exception:
            cache = {}

    pins_to_fetch = [p for p in pins if p not in cache and p != '000000' and p != 'N/A']
    print(f"Total unique pincodes: {len(pins)}. Need to fetch: {len(pins_to_fetch)}")

    if pins_to_fetch:
        with ThreadPoolExecutor(max_workers=25) as executor:
            future_to_pin = {executor.submit(fetch_pincode_info, pin): pin for pin in pins_to_fetch}
            completed = 0
            for future in as_completed(future_to_pin):
                pin, result = future.result()
                with cache_lock:
                    cache[pin] = result
                completed += 1
                if completed % 100 == 0 or completed == len(pins_to_fetch):
                    print(f"Progress: {completed}/{len(pins_to_fetch)} pincodes fetched.")

        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(cache, f, indent=2)

    print(f"Pincode cache ready with {len(cache)} entries.")

if __name__ == '__main__':
    run_enrichment()
