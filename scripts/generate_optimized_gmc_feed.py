import urllib.request
import json
import ssl
import re
import html
import os
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# 1. Fetch live products from Shopify
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(
    'https://petmode.co.uk/products.json?limit=250',
    headers={'User-Agent': 'Mozilla/5.0'}
)
with urllib.request.urlopen(req, context=ctx) as resp:
    catalog_data = json.loads(resp.read().decode('utf-8'))

all_products = catalog_data.get('products', [])
prod_by_handle = {p['handle']: p for p in all_products}
print(f"Loaded {len(all_products)} live products from store.")

def clean_html_desc(raw_html):
    if not raw_html:
        return "High quality pet accessories and essentials from Pet Mode UK. Fast UK delivery."
    clean = re.sub(r'<[^>]+>', ' ', raw_html)
    clean = html.unescape(clean)
    clean = clean.replace('\ufffd', ' ').replace('', ' ')
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean[:4900]

# Strategic Feed Rules based on October Order Audit + Search Terms Analysis
feed_rules = [
    {
        'handle': 'smart-automatic-anti-barking-dog-collar',
        'rank': 'Rank 1 - Top Profit Scaler',
        'tier': 'Tier 1 - Hero Profit Driver',
        'category_label': 'Bark Control & Training',
        'season': 'Winter Indoor Focus',
        'google_cat': 'Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Collars & Harnesses',
        'prod_type': 'Dog Supplies > Bark Collars & Training',
        'title_prefix': 'Pet Mode Humane Anti Bark Collar for Dogs - Sound & Vibration Only (No Shock) - Waterproof Rechargeable'
    },
    {
        'handle': 'teeth-cleaning-dog-toothbrush',
        'rank': 'Rank 2 - Volume Hero',
        'tier': 'Tier 1 - Hero Volume Driver',
        'category_label': 'Dental & Oral Care',
        'season': 'All Year Focus',
        'google_cat': 'Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Toys',
        'prod_type': 'Dog Supplies > Dental Chew Toys & Toothbrushes',
        'title_prefix': 'Pet Mode Dog Toothbrush Chew Toy - Molar Teeth Cleaning Stick for Plaque & Tartar Removal'
    },
    {
        'handle': 'self-adhesive-cat-scratching-carpet-trim-to-fit-scratch-pad-for-cat-trees-furniture',
        'rank': 'Rank 3 - High ROAS Cat Winner',
        'tier': 'Tier 1 - Hero Profit Driver',
        'category_label': 'Cat Furniture Protection',
        'season': 'Indoor Winter Focus',
        'google_cat': 'Animals & Pet Supplies > Pet Supplies > Cat Supplies > Cat Furniture > Cat Scratching Posts & Pads',
        'prod_type': 'Cat Supplies > Furniture Protectors & Scratchers',
        'title_prefix': 'Pet Mode Self-Adhesive Cat Scratching Mat - Trim-to-Fit Replacement Carpet for Cat Tree, Shelves & Wall'
    },
    {
        'handle': 'large-orthopaedic-dog-bed-waterproof',
        'rank': 'Rank 4 - High AOV Bestseller',
        'tier': 'Tier 1 - High AOV Scaler',
        'category_label': 'Orthopaedic Beds & Comfort',
        'season': 'Winter Indoor Focus',
        'google_cat': 'Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Beds',
        'prod_type': 'Dog Supplies > Orthopaedic Waterproof Beds',
        'title_prefix': 'Pet Mode Large Orthopaedic Dog Bed Waterproof - Memory Foam Joint Relief with Washable Cover'
    },
    {
        'handle': 'dog-car-seat-bed-for-small-dogs-washable-booster-seat-with-safety-straps-storage-pockets',
        'rank': 'Rank 5 - High AOV Travel Hero',
        'tier': 'Tier 1 - High AOV Scaler',
        'category_label': 'Travel & Car Safety',
        'season': 'All Year Focus',
        'google_cat': 'Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Car Seats & Seat Covers',
        'prod_type': 'Dog Supplies > Car Booster Seats & Travel Beds',
        'title_prefix': 'Pet Mode Dog Car Booster Seat Bed with Safety Harness Restraint - Washable Travel Cushion (Non-ISOFIX)'
    },
    {
        'handle': 'reflective-airtag-cat-collar-breakaway-safety-collar-with-bell',
        'rank': 'Rank 6 - Bestseller',
        'tier': 'Tier 2 - Volume Accessory',
        'category_label': 'Cat Safety & Collars',
        'season': 'All Year Focus',
        'google_cat': 'Animals & Pet Supplies > Pet Supplies > Cat Supplies > Cat Collars & Harnesses',
        'prod_type': 'Cat Supplies > AirTag Collars & Safety Belts',
        'title_prefix': 'Pet Mode Reflective Cat Collar for Apple AirTag - Breakaway Safety Collar with Bell (Holder Only)'
    },
    {
        'handle': 'cat-dog-steam-grooming-brush',
        'rank': 'Rank 7 - Viral Grooming',
        'tier': 'Tier 2 - Volume Accessory',
        'category_label': 'Grooming & Deshedding',
        'season': 'Autumn Shedding Focus',
        'google_cat': 'Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Grooming Supplies > Dog Brushes & Combs',
        'prod_type': 'Pet Supplies > Grooming > Steam Brushes',
        'title_prefix': 'Pet Mode 3-in-1 Pet Steam Grooming Brush - Anti-Shedding & Massage Spray Comb for Dogs & Cats'
    },
    {
        'handle': 'pet-gps-tracker-with-adjustable-collar',
        'rank': 'Rank 8 - Smart Tech',
        'tier': 'Tier 2 - Smart Tech Accessory',
        'category_label': 'Pet Safety & GPS',
        'season': 'All Year Focus',
        'google_cat': 'Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Collars & Harnesses',
        'prod_type': 'Pet Supplies > GPS Trackers & Smart Collars',
        'title_prefix': 'Pet Mode Pet GPS Tracker with Adjustable Collar - Real-Time Location Anti-Lost Finder for Dogs & Cats'
    },
    {
        'handle': 'dog-necklace-metal',
        'rank': 'Rank 9 - Accessory',
        'tier': 'Tier 2 - Volume Accessory',
        'category_label': 'Dog Fashion & Collars',
        'season': 'All Year Focus',
        'google_cat': 'Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Collars & Harnesses',
        'prod_type': 'Dog Supplies > Metal Chain Collars',
        'title_prefix': 'Pet Mode Metal Chain Collar Necklace for Dogs & Cats - Heavy Duty Cuban Link Choker'
    },
    {
        'handle': 'pet-cat-dog-stainless-steel-automatic-circulation-water-dispenser',
        'rank': 'Rank 10 - Hydration',
        'tier': 'Tier 2 - Feeding & Hydration',
        'category_label': 'Feeding & Hydration',
        'season': 'All Year Focus',
        'google_cat': 'Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Bowls, Feeders & Waterers',
        'prod_type': 'Pet Supplies > Automatic Water Dispensers',
        'title_prefix': 'Pet Mode Stainless Steel Automatic Water Dispenser (2L) - Ultra Quiet Filtered Pet Drinking Fountain'
    },
    {
        'handle': 'cozy-soft-plush-hooded-cat-bed',
        'rank': 'Rank 11 - Winter Warmth',
        'tier': 'Tier 2 - Winter Comfort',
        'category_label': 'Cat Beds & Caves',
        'season': 'Winter Indoor Focus',
        'google_cat': 'Animals & Pet Supplies > Pet Supplies > Cat Supplies > Cat Beds',
        'prod_type': 'Cat Supplies > Hooded Plush Beds',
        'title_prefix': 'Pet Mode Cosy Soft Plush Hooded Cat Bed - Warm Winter Cave & Calming Nest for Cats & Kittens'
    },
    {
        'handle': 'summer-pet-cooling-mat',
        'rank': 'Rank 12 - Seasonal Off-Peak',
        'tier': 'Tier 3 - Seasonal Low Priority',
        'category_label': 'Cooling & Summer',
        'season': 'Summer Off-Season Deprioritize',
        'google_cat': 'Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Beds',
        'prod_type': 'Pet Supplies > Cooling Mats & Pads',
        'title_prefix': 'Pet Mode Self-Cooling Pet Mat - Breathable Ice Silk Waterproof Pad for Dogs & Cats'
    }
]

feed_items = []
for rule in feed_rules:
    handle = rule['handle']
    p = prod_by_handle.get(handle)
    if not p:
        continue
    
    prod_id = p['id']
    prod_title = p['title'].strip()
    clean_desc = clean_html_desc(p.get('body_html', ''))
    images = [img['src'] for img in p.get('images', [])]
    main_img = images[0] if images else ""
    additional_imgs = ",".join(images[1:6]) if len(images) > 1 else ""
    
    for v in p.get('variants', []):
        var_id = v['id']
        var_title = v['title'].strip()
        sku = v.get('sku') or f"PM-{prod_id}-{var_id}"
        price = float(v.get('price') or 0.0)
        compare_price = float(v.get('compare_at_price') or 0.0)
        is_avail = v.get('available', True)
        
        # GMC unique IDs
        gmc_id = f"shopify_GB_{prod_id}_{var_id}"
        item_group_id = f"shopify_GB_{prod_id}"
        
        # Optimized title: frontload converting keywords, variant at end
        base_title = rule['title_prefix']
        if var_title and var_title.lower() != 'default title':
            full_title = f"{base_title} - {var_title}"
        else:
            full_title = base_title
        full_title = full_title[:150]
        
        # Strict pricing
        if compare_price > price:
            price_str = f"{compare_price:.2f} GBP"
            sale_price_str = f"{price:.2f} GBP"
        else:
            price_str = f"{price:.2f} GBP"
            sale_price_str = ""
            
        link = f"https://petmode.co.uk/products/{handle}?variant={var_id}"
        
        feed_items.append({
            'id': gmc_id,
            'title': full_title,
            'description': clean_desc,
            'link': link,
            'image_link': main_img,
            'additional_image_link': additional_imgs,
            'availability': 'in_stock' if is_avail else 'out_of_stock',
            'price': price_str,
            'sale_price': sale_price_str,
            'brand': 'Pet Mode',
            'gtin': '',
            'mpn': sku,
            'identifier_exists': 'no',
            'condition': 'new',
            'item_group_id': item_group_id,
            'google_product_category': rule['google_cat'],
            'product_type': rule['prod_type'],
            'shipping': 'GB:::0.00 GBP',
            'included_destination': 'Shopping_ads,Free_listings',
            'excluded_destination': 'Local_inventory_ads,Free_local_listings',
            'custom_label_0': rule['tier'],
            'custom_label_1': rule['category_label'],
            'custom_label_2': rule['season'],
            'custom_label_3': 'Free UK Delivery',
            'custom_label_4': rule['rank']
        })

print(f"Generated {len(feed_items)} fully optimized feed items.")
feed_df = pd.DataFrame(feed_items)

out_dir = r'c:\Users\test\Videos\Office\data\Pet Mode\Google Ads'
os.makedirs(out_dir, exist_ok=True)

# 1. TSV
tsv_path = os.path.join(out_dir, 'Pet_Mode_Optimized_GMC_Feed.tsv')
feed_df.to_csv(tsv_path, sep='\t', index=False, encoding='utf-8')
print(f"TSV saved to: {tsv_path}")

# 2. CSV
csv_path = os.path.join(out_dir, 'Pet_Mode_Optimized_GMC_Feed.csv')
feed_df.to_csv(csv_path, index=False, encoding='utf-8')
print(f"CSV saved to: {csv_path}")

# 3. Excel
excel_path = os.path.join(out_dir, 'Pet_Mode_Optimized_GMC_Feed.xlsx')
feed_df.to_excel(excel_path, index=False)
print(f"Excel saved to: {excel_path}")
