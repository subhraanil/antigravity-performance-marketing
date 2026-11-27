import urllib.request
import json
import ssl
import re
import html
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
print(f"Loaded {len(all_products)} live products from store.")

# 2. Load order history to rank products by proven sales
df_orders = pd.read_csv(r'c:\Users\test\Videos\Office\data\Pet Mode\orders_export.csv', low_memory=False)
order_items = df_orders.groupby('Lineitem name').agg(
    orders=('Lineitem quantity', 'count'),
    units=('Lineitem quantity', lambda x: pd.to_numeric(x, errors='coerce').fillna(1).sum()),
    revenue=('Total', lambda x: pd.to_numeric(x, errors='coerce').fillna(0).sum())
).reset_index().sort_values(by='units', ascending=False)

# Clean HTML helper
def clean_html_desc(raw_html):
    if not raw_html:
        return "High quality pet accessories and essentials from Pet Mode UK."
    # Remove HTML tags
    clean = re.sub(r'<[^>]+>', ' ', raw_html)
    # Unescape HTML entities
    clean = html.unescape(clean)
    # Normalize whitespaces
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean[:4900]

# List of top selling product handles and custom configurations
# These match the proven top revenue and unit drivers from Shopify orders
top_product_rules = [
    {
        'handle': 'teeth-cleaning-dog-toothbrush',
        'rank': 'Rank 1 - #1 Best Seller',
        'label_0': 'Top Seller - Hero SKU',
        'label_1': 'Dental Care',
        'google_cat': 'Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Toys',
        'prod_type': 'Dog Supplies > Dental Chew Toys & Toothbrushes',
        'priority': 1
    },
    {
        'handle': '5-in-1-interactive-dog-dental-chew-toy-toothbrush-treat-dispenser-chew-stick',
        'rank': 'Rank 2 - Hero SKU',
        'label_0': 'Top Seller - Hero SKU',
        'label_1': 'Dental Care',
        'google_cat': 'Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Toys',
        'prod_type': 'Dog Supplies > Dental Chew Toys & Treat Dispensers',
        'priority': 2
    },
    {
        'handle': '3-in-1-dog-dental-chew-toy-teeth-cleaning-gum-massage-stick',
        'rank': 'Rank 3 - Hero SKU',
        'label_0': 'Top Seller - Hero SKU',
        'label_1': 'Dental Care',
        'google_cat': 'Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Toys',
        'prod_type': 'Dog Supplies > Squeaky Dental Chew Toys',
        'priority': 3
    },
    {
        'handle': 'smart-automatic-anti-barking-dog-collar',
        'rank': 'Rank 4 - Bestseller',
        'label_0': 'Top Seller - High Margin',
        'label_1': 'Training & Bark Control',
        'google_cat': 'Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Collars & Harnesses',
        'prod_type': 'Dog Supplies > Bark Collars & Training',
        'priority': 4
    },
    {
        'handle': 'dog-car-seat-bed-for-small-dogs-washable-booster-seat-with-safety-straps-storage-pockets',
        'rank': 'Rank 5 - High AOV Bestseller',
        'label_0': 'Top Seller - High AOV',
        'label_1': 'Car Travel & Safety',
        'google_cat': 'Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Car Seats & Seat Covers',
        'prod_type': 'Dog Supplies > Car Booster Seats & Travel Beds',
        'priority': 5
    },
    {
        'handle': 'cat-dog-steam-grooming-brush',
        'rank': 'Rank 6 - Viral Bestseller',
        'label_0': 'Top Seller - High Volume',
        'label_1': 'Grooming & Shedding',
        'google_cat': 'Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Grooming Supplies > Dog Brushes & Combs',
        'prod_type': 'Pet Supplies > Grooming > Steam Brushes',
        'priority': 6
    },
    {
        'handle': 'self-adhesive-cat-scratching-carpet-trim-to-fit-scratch-pad-for-cat-trees-furniture',
        'rank': 'Rank 7 - Bestseller',
        'label_0': 'Top Seller - High Volume',
        'label_1': 'Cat Furniture & Scratchers',
        'google_cat': 'Animals & Pet Supplies > Pet Supplies > Cat Supplies > Cat Furniture > Cat Scratching Posts & Pads',
        'prod_type': 'Cat Supplies > Furniture Protectors & Scratchers',
        'priority': 7
    },
    {
        'handle': 'elevated-cooling-dog-bed-breathable-raised-mesh-pet-cot-for-indoor-outdoor-use',
        'rank': 'Rank 8 - Bestseller',
        'label_0': 'Top Seller - High Margin',
        'label_1': 'Beds & Furniture',
        'google_cat': 'Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Beds',
        'prod_type': 'Dog Supplies > Elevated Cooling Beds',
        'priority': 8
    },
    {
        'handle': 'elevated-cooling-dog-bed-breathable-mesh-pet-cot-with-washable-bolsters',
        'rank': 'Rank 9 - Bestseller',
        'label_0': 'Top Seller - High Margin',
        'label_1': 'Beds & Furniture',
        'google_cat': 'Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Beds',
        'prod_type': 'Dog Supplies > Elevated Cooling Beds with Bolsters',
        'priority': 9
    },
    {
        'handle': '2-in-1-pet-hair-removal-roller',
        'rank': 'Rank 10 - Bestseller',
        'label_0': 'Top Seller - High Volume',
        'label_1': 'Grooming & Cleaning',
        'google_cat': 'Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Grooming Supplies',
        'prod_type': 'Pet Cleaning > Hair Removal Rollers',
        'priority': 10
    },
    {
        'handle': 'nteractivei-cat-toys-ball-auto-electric-rolling',
        'rank': 'Rank 11 - Bestseller',
        'label_0': 'Top Seller - Volume Driver',
        'label_1': 'Cat Toys',
        'google_cat': 'Animals & Pet Supplies > Pet Supplies > Cat Supplies > Cat Toys',
        'prod_type': 'Cat Supplies > Interactive Electronic Toys',
        'priority': 11
    },
    {
        'handle': 'calming-washable-soft-dog-bed-for-anxiety-comfort',
        'rank': 'Rank 12 - High AOV Bestseller',
        'label_0': 'Top Seller - High AOV',
        'label_1': 'Beds & Furniture',
        'google_cat': 'Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Beds',
        'prod_type': 'Dog Supplies > Calming Anti-Anxiety Beds',
        'priority': 12
    },
    {
        'handle': 'summer-pet-cooling-mat',
        'rank': 'Rank 13 - Bestseller',
        'label_0': 'Top Seller - Volume Driver',
        'label_1': 'Cooling & Comfort',
        'google_cat': 'Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Beds',
        'prod_type': 'Pet Supplies > Cooling Mats & Pads',
        'priority': 13
    },
    {
        'handle': 'dog-necklace-metal',
        'rank': 'Rank 14 - Proven Seller',
        'label_0': 'Top Seller - Accessories',
        'label_1': 'Collars & Accessories',
        'google_cat': 'Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Collars & Harnesses',
        'prod_type': 'Dog Supplies > Metal Chain Collars & Necklaces',
        'priority': 14
    },
    {
        'handle': 'large-orthopaedic-dog-bed-waterproof',
        'rank': 'Rank 15 - High AOV',
        'label_0': 'Top Seller - High AOV',
        'label_1': 'Beds & Furniture',
        'google_cat': 'Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Beds',
        'prod_type': 'Dog Supplies > Orthopedic Waterproof Beds',
        'priority': 15
    },
    {
        'handle': 'automatic-cordless-pet-water-fountain-3000ml-smart-water-dispenser',
        'rank': 'Rank 16 - High AOV',
        'label_0': 'Top Seller - High AOV',
        'label_1': 'Feeding & Hydration',
        'google_cat': 'Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Bowls, Feeders & Waterers',
        'prod_type': 'Pet Supplies > Automatic Water Fountains',
        'priority': 16
    },
    {
        'handle': 'dog-harness-no-pull-breathable-reflective',
        'rank': 'Rank 17 - Proven Seller',
        'label_0': 'Top Seller - Walking & Travel',
        'label_1': 'Collars & Harnesses',
        'google_cat': 'Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Collars & Harnesses',
        'prod_type': 'Dog Supplies > No-Pull Reflective Harnesses',
        'priority': 17
    },
    {
        'handle': 'dog-leash-retractable',
        'rank': 'Rank 18 - Proven Seller',
        'label_0': 'Top Seller - Walking & Travel',
        'label_1': 'Collars & Leashes',
        'google_cat': 'Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Leashes',
        'prod_type': 'Dog Supplies > LED Retractable Leashes',
        'priority': 18
    },
    {
        'handle': 'hands-free-dog-leash',
        'rank': 'Rank 19 - Proven Seller',
        'label_0': 'Top Seller - Walking & Travel',
        'label_1': 'Collars & Leashes',
        'google_cat': 'Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Leashes',
        'prod_type': 'Dog Supplies > Hands-Free Bungee Leashes',
        'priority': 19
    },
    {
        'handle': 'professional-pet-nail-clipper',
        'rank': 'Rank 20 - Proven Seller',
        'label_0': 'Top Seller - Grooming',
        'label_1': 'Grooming & Care',
        'google_cat': 'Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Grooming Supplies > Dog Nail Clippers',
        'prod_type': 'Pet Grooming > LED Nail Clippers',
        'priority': 20
    }
]

rule_map = {r['handle']: r for r in top_product_rules}

feed_items = []
prod_by_handle = {p['handle']: p for p in all_products}

for rule in top_product_rules:
    handle = rule['handle']
    p = prod_by_handle.get(handle)
    if not p:
        print(f"Warning: Handle {handle} not found in live catalog!")
        continue
    
    prod_id = p['id']
    prod_title = p['title'].strip()
    raw_desc = p.get('body_html', '')
    clean_desc = clean_html_desc(raw_desc)
    images = [img['src'] for img in p.get('images', [])]
    main_img = images[0] if images else ""
    additional_imgs = ",".join(images[1:6]) if len(images) > 1 else ""
    
    variants = p.get('variants', [])
    for v in variants:
        var_id = v['id']
        var_title = v['title'].strip()
        sku = v.get('sku') or f"PM-{prod_id}-{var_id}"
        price = float(v.get('price') or 0.0)
        compare_price = float(v.get('compare_at_price') or 0.0)
        is_avail = v.get('available', True)
        
        # GMC unique id
        gmc_id = f"shopify_GB_{prod_id}_{var_id}"
        
        # Build Title: If variant title is not 'Default Title', append color/size
        if var_title and var_title.lower() != 'default title':
            full_title = f"{prod_title} - {var_title} | Pet Mode UK"
        else:
            full_title = f"{prod_title} | Pet Mode UK"
        full_title = full_title[:150]
        
        # Format pricing
        price_str = f"{price:.2f} GBP"
        sale_price_str = ""
        if compare_price > price:
            # If compare at price is higher, current price is sale price!
            price_str = f"{compare_price:.2f} GBP"
            sale_price_str = f"{price:.2f} GBP"
            
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
            'google_product_category': rule['google_cat'],
            'product_type': rule['prod_type'],
            'shipping': 'GB:::0.00 GBP',
            'custom_label_0': rule['label_0'],
            'custom_label_1': rule['label_1'],
            'custom_label_2': rule['rank'],
            'custom_label_3': 'Free UK Delivery',
            'custom_label_4': 'Bestseller Feed'
        })

print(f"Total feed items (variants across top 20 products): {len(feed_items)}")
feed_df = pd.DataFrame(feed_items)

# Save TSV (Google Merchant Center primary recommended tab-delimited format)
import os
out_dir = r'c:\Users\test\Videos\Office\data\Pet Mode\Google Ads'
os.makedirs(out_dir, exist_ok=True)

tsv_path = os.path.join(out_dir, 'Pet_Mode_Top_Selling_Products_Feed.tsv')
feed_df.to_csv(tsv_path, sep='\t', index=False, encoding='utf-8')
print(f"Saved Google Merchant Center TSV feed to: {tsv_path}")

# Save CSV
csv_path = os.path.join(out_dir, 'Pet_Mode_Top_Selling_Products_Feed.csv')
feed_df.to_csv(csv_path, index=False, encoding='utf-8')
print(f"Saved Google Merchant Center CSV feed to: {csv_path}")

# Build formatted Excel workbook for client review
excel_path = os.path.join(out_dir, 'Pet_Mode_Top_Selling_Products_Feed.xlsx')
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Google Merchant Feed"
ws.views.sheetView[0].showGridLines = True

navy_fill = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
navy_font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
zebra_fill = PatternFill(start_color="F9FBFC", end_color="F9FBFC", fill_type="solid")
thin_border = Border(
    left=Side(style='thin', color='E0E0E0'),
    right=Side(style='thin', color='E0E0E0'),
    top=Side(style='thin', color='E0E0E0'),
    bottom=Side(style='thin', color='E0E0E0')
)
reg_font = Font(name="Calibri", size=9, color="000000")

headers = list(feed_df.columns)
for col_idx, h in enumerate(headers, start=1):
    c = ws.cell(1, col_idx, h)
    c.fill = navy_fill
    c.font = navy_font
    c.alignment = Alignment(horizontal="center", vertical="center")
    c.border = thin_border

for r_idx, r_data in enumerate(feed_df.to_dict(orient='records'), start=2):
    is_even = (r_idx % 2 == 0)
    for c_idx, h in enumerate(headers, start=1):
        c = ws.cell(r_idx, c_idx, r_data[h])
        c.font = reg_font
        c.border = thin_border
        if is_even:
            c.fill = zebra_fill
        if h in ['price', 'sale_price', 'shipping']:
            c.alignment = Alignment(horizontal="right", vertical="center")
        elif h in ['id', 'availability', 'brand', 'identifier_exists', 'condition', 'custom_label_0', 'custom_label_1', 'custom_label_2', 'custom_label_3', 'custom_label_4']:
            c.alignment = Alignment(horizontal="center", vertical="center")
        else:
            c.alignment = Alignment(horizontal="left", vertical="center")

# Auto-adjust column widths
for col in range(1, len(headers) + 1):
    col_letter = get_column_letter(col)
    h_name = headers[col - 1]
    if h_name in ['description']:
        ws.column_dimensions[col_letter].width = 40
    elif h_name in ['link', 'image_link', 'additional_image_link']:
        ws.column_dimensions[col_letter].width = 30
    elif h_name in ['title', 'google_product_category', 'product_type']:
        ws.column_dimensions[col_letter].width = 35
    else:
        ws.column_dimensions[col_letter].width = 18

wb.save(excel_path)
print(f"Saved formatted Excel feed to: {excel_path}")
