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

# 1. Fetch all live products from Pet Mode Shopify store
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(
    'https://petmode.co.uk/products.json?limit=250',
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
)
with urllib.request.urlopen(req, context=ctx) as resp:
    catalog = json.loads(resp.read().decode('utf-8'))

products = catalog.get('products', [])
print(f"Loaded {len(products)} products from petmode.co.uk.")

# Clean description text
def clean_desc(raw_html, title):
    if not raw_html or len(raw_html.strip()) < 10:
        return f"High quality {title} from Pet Mode UK. Designed for pet comfort, safety, and durability with fast UK delivery."
    clean = re.sub(r'<[^>]+>', ' ', raw_html)
    clean = html.unescape(clean)
    clean = clean.replace('\ufffd', ' ').replace('\u2013', '-').replace('\u2014', '-')
    clean = re.sub(r'\s+', ' ', clean).strip()
    if len(clean) < 20:
        clean = f"{title}. {clean}. High quality pet essential from Pet Mode UK."
    return clean[:4900]

# Taxonomic classification engine
def classify_product(title, p_type, tags):
    text = (title + " " + (p_type or "") + " " + " ".join(tags or [])).lower()
    
    is_cat = any(w in text for w in ['cat', 'cats', 'kitten', 'feline'])
    is_dog = any(w in text for w in ['dog', 'dogs', 'puppy', 'pup', 'canine'])
    
    # 1. Treats & Food
    if any(w in text for w in ['treat', 'sausage', 'jerky', 'trachea', 'lung', 'tripe', 'paddywack', 'ear', 'meat', 'food', 'dently']):
        g_cat = "Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Treats" if is_dog or not is_cat else "Animals & Pet Supplies > Pet Supplies > Cat Supplies > Cat Treats"
        prod_t = "Dog Supplies > Natural Treats & Chews" if is_dog or not is_cat else "Cat Supplies > Cat Treats"
        cluster = "Treats & Chews"

    # 2. Cat Scratchers & Furniture
    elif any(w in text for w in ['scratch', 'scratching', 'cat tree', 'scratcher', 'climbing']):
        g_cat = "Animals & Pet Supplies > Pet Supplies > Cat Supplies > Cat Furniture > Cat Scratching Posts & Pads"
        prod_t = "Cat Supplies > Furniture Protectors & Scratchers"
        cluster = "Cat Furniture & Scratchers"

    # 3. Bark Control
    elif any(w in text for w in ['bark', 'anti-bark', 'anti bark']):
        g_cat = "Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Collars & Harnesses"
        prod_t = "Dog Supplies > Bark Collars & Training"
        cluster = "Bark Control & Training"

    # 4. Car Travel & Carriers
    elif any(w in text for w in ['car seat', 'booster', 'carrier', 'travel kennel', 'travel bag']):
        if any(w in text for w in ['car seat', 'booster']):
            g_cat = "Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Car Seats & Seat Covers"
            prod_t = "Dog Supplies > Car Booster Seats & Travel Beds"
            cluster = "Travel & Car Safety"
        else:
            g_cat = "Animals & Pet Supplies > Pet Supplies > Pet Carrier & Crate Accessories"
            prod_t = "Pet Supplies > Travel Carriers"
            cluster = "Travel & Car Safety"

    # 5. Beds, Cots, Blankets, Sofas, Mats
    elif any(w in text for w in ['bed', 'mat', 'blanket', 'sofa', 'cushion', 'cot', 'lounger', 'snuffle']):
        if any(w in text for w in ['feeding mat', 'bowl mat', 'spill-proof', 'spill proof', 'lick mat']):
            g_cat = "Animals & Pet Supplies > Pet Supplies > Cat Supplies > Cat Bowls & Feeders" if is_cat and not is_dog else "Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Bowls, Feeders & Waterers"
            prod_t = "Pet Supplies > Feeding Mats & Accessories"
            cluster = "Feeding & Hydration"
        elif is_cat and not is_dog:
            g_cat = "Animals & Pet Supplies > Pet Supplies > Cat Supplies > Cat Beds"
            prod_t = "Cat Supplies > Beds & Mats"
            cluster = "Beds & Comfort"
        else:
            g_cat = "Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Beds"
            prod_t = "Dog Supplies > Beds & Furniture"
            cluster = "Beds & Comfort"

    # 6. Dental & Toothbrushes
    elif any(w in text for w in ['toothbrush', 'dental', 'chew toy', 'molar stick', 'teeth']):
        g_cat = "Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Toys"
        prod_t = "Dog Supplies > Dental Chew Toys & Toothbrushes"
        cluster = "Dental Care"

    # 7. Feeding, Bowls & Fountains
    elif any(w in text for w in ['fountain', 'water dispenser', 'water bottle', 'bowl', 'feeder', 'water cup', 'drinking']):
        if is_cat and not is_dog:
            g_cat = "Animals & Pet Supplies > Pet Supplies > Cat Supplies > Cat Bowls & Feeders"
            prod_t = "Cat Supplies > Bowls & Fountains"
        else:
            g_cat = "Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Bowls, Feeders & Waterers"
            prod_t = "Dog Supplies > Bowls & Dispensers"
        cluster = "Feeding & Hydration"

    # 8. Grooming & Hygiene
    elif any(w in text for w in ['brush', 'grooming', 'nail grinder', 'clipper', 'comb', 'vacuum', 'hair remover', 'hair removal', 'bath']):
        if is_cat and not is_dog:
            g_cat = "Animals & Pet Supplies > Pet Supplies > Cat Supplies > Cat Grooming Supplies"
            prod_t = "Cat Supplies > Grooming Tools"
        else:
            g_cat = "Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Grooming Supplies"
            prod_t = "Dog Supplies > Grooming Supplies"
        cluster = "Grooming & Hygiene"

    # 9. Collars, Harnesses & Leashes
    elif any(w in text for w in ['collar', 'harness', 'leash', 'lead', 'choker', 'necklace', 'chest strap', 'traction rope']):
        if is_cat and not is_dog:
            g_cat = "Animals & Pet Supplies > Pet Supplies > Cat Supplies > Cat Collars & Harnesses"
            prod_t = "Cat Supplies > Collars & Harnesses"
        else:
            g_cat = "Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Collars & Harnesses"
            prod_t = "Dog Supplies > Collars, Harnesses & Leashes"
        cluster = "Collars, Harnesses & Leashes"

    # 10. Trackers & GPS
    elif any(w in text for w in ['tracker', 'gps', 'airtag', 'tag locator']):
        g_cat = "Animals & Pet Supplies > Pet Supplies > Pet Identification Tags"
        prod_t = "Pet Supplies > Trackers & GPS"
        cluster = "Pet Safety & GPS"

    # 11. Apparel, Coats & Shoes
    elif any(w in text for w in ['shoe', 'shoes', 'boot', 'coat', 'jacket', 'puffer', 'vest', 'sweater', 'apparel']):
        g_cat = "Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Apparel"
        prod_t = "Dog Supplies > Apparel & Shoes"
        cluster = "Apparel & Protection"

    # 12. Toys & Entertainment
    elif any(w in text for w in ['toy', 'laser', 'ball', 'catnip', 'dinosaur']):
        if is_cat and not is_dog:
            g_cat = "Animals & Pet Supplies > Pet Supplies > Cat Supplies > Cat Toys"
            prod_t = "Cat Supplies > Toys"
        else:
            g_cat = "Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Toys"
            prod_t = "Dog Supplies > Toys"
        cluster = "Toys & Play"

    # 13. Waste & Clean-up
    elif any(w in text for w in ['poop', 'waste', 'litter', 'poo bag']):
        if is_cat and not is_dog:
            g_cat = "Animals & Pet Supplies > Pet Supplies > Cat Supplies > Cat Litter & Waste Disposal"
            prod_t = "Cat Supplies > Litter & Clean-up"
        else:
            g_cat = "Animals & Pet Supplies > Pet Supplies > Dog Supplies > Dog Waste Disposal"
            prod_t = "Dog Supplies > Waste Disposal & Bags"
        cluster = "Waste & Clean-up"

    # 14. Bundles & Starter Packs
    elif any(w in text for w in ['starter pack', 'bundle', 'picks', 'essentials', 'collection']):
        g_cat = "Animals & Pet Supplies > Pet Supplies"
        prod_t = "Pet Supplies > Bundles & Starter Sets"
        cluster = "Bundles & Sets"

    else:
        g_cat = "Animals & Pet Supplies > Pet Supplies"
        prod_t = "Pet Supplies > General Essentials"
        cluster = "General Pet Care"
        
    return g_cat, prod_t, cluster

# Verified Top Sellers handles (from actual order audit)
tier1_handles = {
    'smart-automatic-anti-barking-dog-collar': ('Tier 1 - Hero Profit Scaler', 'Winter Indoor Focus'),
    'teeth-cleaning-dog-toothbrush': ('Tier 1 - Hero Volume Scaler', 'All Year'),
    'self-adhesive-cat-scratching-carpet-trim-to-fit-scratch-pad-for-cat-trees-furniture': ('Tier 1 - Hero Profit Scaler', 'Winter Indoor Focus'),
    'large-orthopaedic-dog-bed-waterproof': ('Tier 1 - High AOV Scaler', 'Winter Indoor Focus'),
    'dog-car-seat-bed-for-small-dogs-washable-booster-seat-with-safety-straps-storage-pockets': ('Tier 1 - High AOV Scaler', 'All Year'),
}

tier2_handles = {
    'reflective-airtag-cat-collar-breakaway-safety-collar-with-bell': ('Tier 2 - Proven Bestseller', 'All Year'),
    'cat-dog-steam-grooming-brush': ('Tier 2 - Proven Bestseller', 'All Year'),
    'pet-gps-tracker-with-adjustable-collar': ('Tier 2 - Proven Bestseller', 'All Year'),
    'dog-necklace-metal': ('Tier 2 - Proven Bestseller', 'All Year'),
    'pet-cat-dog-stainless-steel-automatic-circulation-water-dispenser': ('Tier 2 - Proven Bestseller', 'All Year'),
    'cozy-soft-plush-hooded-cat-bed': ('Tier 2 - Proven Bestseller', 'Winter Indoor Focus'),
    'elevated-cooling-dog-bed-breathable-raised-mesh-pet-cot-for-indoor-outdoor-use': ('Tier 2 - Proven Bestseller', 'Summer Off-Season Deprioritize'),
    '2-in-1-pet-hair-removal-roller': ('Tier 2 - Proven Bestseller', 'All Year'),
    'dog-nail-grinder-electric': ('Tier 2 - Proven Bestseller', 'All Year'),
    'hands-free-dog-running-leash-with-waist-pocket': ('Tier 2 - Proven Bestseller', 'All Year'),
}

seasonal_deprioritize = {
    'summer-pet-cooling-mat',
    'self-cooling-pet-mat-leak-proof-gel-cooling-pad-for-dogs-cats',
    'elevated-cooling-dog-bed-breathable-mesh-pet-cot-with-washable-bolsters'
}

feed_rows = []

for p in products:
    handle = p['handle']
    prod_id = p['id']
    title_raw = p['title'].strip()
    title_clean = title_raw.replace('\ufffd', ' ').replace('\u2013', '-').replace('\u2014', '-').strip()
    desc = clean_desc(p.get('body_html', ''), title_clean)
    p_type = p.get('product_type', '')
    tags = p.get('tags', [])
    images = [img['src'] for img in p.get('images', [])]
    main_img = images[0] if images else ""
    extra_imgs = ",".join(images[1:6]) if len(images) > 1 else ""
    
    g_cat, prod_t, cluster = classify_product(title_clean, p_type, tags)
    
    # Custom Label 0 (Tier) & Custom Label 2 (Season)
    if handle in tier1_handles:
        tier, season = tier1_handles[handle]
    elif handle in tier2_handles:
        tier, season = tier2_handles[handle]
    elif handle in seasonal_deprioritize or 'cooling' in title_clean.lower():
        tier = 'Tier 4 - Seasonal Deprioritize'
        season = 'Summer Off-Season Deprioritize'
    elif 'buffalo' in title_clean.lower() or 'treat' in title_clean.lower():
        tier = 'Tier 4 - Low Margin Treat'
        season = 'All Year'
    else:
        tier = 'Tier 3 - General Catalog'
        season = 'Winter Focus' if any(w in title_clean.lower() for w in ['warm', 'plush', 'winter', 'fleece', 'heat']) else 'All Year'
        
    for v in p.get('variants', []):
        var_id = v['id']
        var_title = v['title'].strip()
        sku = v.get('sku') or f"PM-{prod_id}-{var_id}"
        price = float(v.get('price') or 0.0)
        compare_price = float(v.get('compare_at_price') or 0.0)
        is_avail = v.get('available', True)
        
        # GMC Unique IDs
        gmc_id = f"shopify_GB_{prod_id}_{var_id}"
        item_group_id = f"shopify_GB_{prod_id}"
        
        # Optimized Title Formula: [Brand] + [Product Core] + [Variant/Size/Color] + UK
        if var_title and var_title.lower() != 'default title':
            full_title = f"Pet Mode {title_clean} - {var_title}"
        else:
            full_title = f"Pet Mode {title_clean}"
        full_title = re.sub(r'\s+', ' ', full_title).strip()[:150]
        
        # Strict GMC Price formatting
        if compare_price > price and compare_price > 0:
            price_str = f"{compare_price:.2f} GBP"
            sale_price_str = f"{price:.2f} GBP"
            active_price = price
        else:
            price_str = f"{price:.2f} GBP"
            sale_price_str = ""
            active_price = price
            
        # Price Bracket (Custom Label 3)
        if active_price < 20.0:
            price_bracket = "Under £20"
        elif active_price <= 40.0:
            price_bracket = "£20 - £40"
        else:
            price_bracket = "Over £40"
            
        link = f"https://petmode.co.uk/products/{handle}?variant={var_id}"
        
        feed_rows.append({
            'id': gmc_id,
            'title': full_title,
            'description': desc,
            'link': link,
            'image_link': main_img,
            'additional_image_link': extra_imgs,
            'availability': 'in_stock' if is_avail else 'out_of_stock',
            'price': price_str,
            'sale_price': sale_price_str,
            'brand': 'Pet Mode',
            'gtin': '',
            'mpn': sku,
            'identifier_exists': 'no',
            'condition': 'new',
            'item_group_id': item_group_id,
            'google_product_category': g_cat,
            'product_type': prod_t,
            'shipping': 'GB:::0.00 GBP',
            'included_destination': 'Shopping_ads,Free_listings',
            'excluded_destination': 'Local_inventory_ads,Free_local_listings',
            'custom_label_0': tier,
            'custom_label_1': cluster,
            'custom_label_2': season,
            'custom_label_3': price_bracket,
            'custom_label_4': 'In Stock' if is_avail else 'Out of Stock'
        })

feed_df = pd.DataFrame(feed_rows)
print(f"Successfully generated {len(feed_df)} Primary Feed items across all {len(products)} products!")

out_dir = r'c:\Users\test\Videos\Office\data\Pet Mode\Google Ads'
os.makedirs(out_dir, exist_ok=True)

# 1. Primary Feed TSV (Tab-Separated — Google's Recommended Primary Format)
tsv_path = os.path.join(out_dir, 'Pet_Mode_Primary_Product_Feed.tsv')
feed_df.to_csv(tsv_path, sep='\t', index=False, encoding='utf-8')
print(f"Primary TSV Feed: {tsv_path}")

# 2. Primary Feed CSV
csv_path = os.path.join(out_dir, 'Pet_Mode_Primary_Product_Feed.csv')
feed_df.to_csv(csv_path, index=False, encoding='utf-8')
print(f"Primary CSV Feed: {csv_path}")

# 3. Primary Feed XML (Google Shopping RSS 2.0 Standard)
xml_path = os.path.join(out_dir, 'Pet_Mode_Primary_Product_Feed.xml')
with open(xml_path, 'w', encoding='utf-8') as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">\n')
    f.write('  <channel>\n')
    f.write('    <title>Pet Mode UK Official Product Feed</title>\n')
    f.write('    <link>https://petmode.co.uk</link>\n')
    f.write('    <description>Official Google Merchant Center Primary Product Feed for Pet Mode UK</description>\n')
    for row in feed_df.to_dict(orient='records'):
        f.write('    <item>\n')
        f.write(f'      <g:id>{html.escape(str(row["id"]))}</g:id>\n')
        f.write(f'      <g:title>{html.escape(str(row["title"]))}</g:title>\n')
        f.write(f'      <g:description>{html.escape(str(row["description"]))}</g:description>\n')
        f.write(f'      <g:link>{html.escape(str(row["link"]))}</g:link>\n')
        f.write(f'      <g:image_link>{html.escape(str(row["image_link"]))}</g:image_link>\n')
        if row["additional_image_link"]:
            for add_img in row["additional_image_link"].split(','):
                f.write(f'      <g:additional_image_link>{html.escape(add_img)}</g:additional_image_link>\n')
        f.write(f'      <g:availability>{row["availability"]}</g:availability>\n')
        f.write(f'      <g:price>{row["price"]}</g:price>\n')
        if row["sale_price"]:
            f.write(f'      <g:sale_price>{row["sale_price"]}</g:sale_price>\n')
        f.write(f'      <g:brand>{html.escape(str(row["brand"]))}</g:brand>\n')
        f.write(f'      <g:mpn>{html.escape(str(row["mpn"]))}</g:mpn>\n')
        f.write(f'      <g:identifier_exists>{row["identifier_exists"]}</g:identifier_exists>\n')
        f.write(f'      <g:condition>{row["condition"]}</g:condition>\n')
        f.write(f'      <g:item_group_id>{html.escape(str(row["item_group_id"]))}</g:item_group_id>\n')
        f.write(f'      <g:google_product_category>{html.escape(str(row["google_product_category"]))}</g:google_product_category>\n')
        f.write(f'      <g:product_type>{html.escape(str(row["product_type"]))}</g:product_type>\n')
        f.write('      <g:shipping>\n')
        f.write('        <g:country>GB</g:country>\n')
        f.write('        <g:price>0.00 GBP</g:price>\n')
        f.write('      </g:shipping>\n')
        f.write(f'      <g:custom_label_0>{html.escape(str(row["custom_label_0"]))}</g:custom_label_0>\n')
        f.write(f'      <g:custom_label_1>{html.escape(str(row["custom_label_1"]))}</g:custom_label_1>\n')
        f.write(f'      <g:custom_label_2>{html.escape(str(row["custom_label_2"]))}</g:custom_label_2>\n')
        f.write(f'      <g:custom_label_3>{html.escape(str(row["custom_label_3"]))}</g:custom_label_3>\n')
        f.write(f'      <g:custom_label_4>{html.escape(str(row["custom_label_4"]))}</g:custom_label_4>\n')
        f.write('    </item>\n')
    f.write('  </channel>\n')
    f.write('</rss>\n')
print(f"Primary XML Feed: {xml_path}")

# 4. Formatted Excel Workbook
excel_path = os.path.join(out_dir, 'Pet_Mode_Primary_Product_Feed.xlsx')
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "GMC Primary Feed"
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
        if h in ['price', 'sale_price']:
            c.alignment = Alignment(horizontal="right", vertical="center")
        elif h in ['id', 'item_group_id', 'availability', 'brand', 'identifier_exists', 'condition', 'shipping', 'included_destination', 'excluded_destination', 'custom_label_0', 'custom_label_1', 'custom_label_2', 'custom_label_3', 'custom_label_4']:
            c.alignment = Alignment(horizontal="center", vertical="center")
        else:
            c.alignment = Alignment(horizontal="left", vertical="center")

for col in range(1, len(headers) + 1):
    col_letter = get_column_letter(col)
    h_name = headers[col - 1]
    if h_name in ['description']:
        ws.column_dimensions[col_letter].width = 35
    elif h_name in ['link', 'image_link', 'additional_image_link']:
        ws.column_dimensions[col_letter].width = 28
    elif h_name in ['title', 'google_product_category', 'product_type']:
        ws.column_dimensions[col_letter].width = 32
    else:
        ws.column_dimensions[col_letter].width = 16

wb.save(excel_path)
print(f"Primary Excel Feed: {excel_path}")
