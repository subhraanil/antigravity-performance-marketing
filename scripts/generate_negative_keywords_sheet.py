import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
import csv

# Negative keywords data with category, keyword, match type, and rationale
negatives_data = [
    # 1. Harmful / Shock / Electric Gear
    ("Harmful / Shock Gear", "shock", "Phrase", '"shock"', "Pet Mode sells 100% humane sound/vibration collars; shock searchers bounce immediately."),
    ("Harmful / Shock Gear", "electric shock", "Phrase", '"electric shock"', "Eliminates electric shock dog training queries."),
    ("Harmful / Shock Gear", "electric collar", "Phrase", '"electric collar"', "Prevents matching with high-voltage training collars."),
    ("Harmful / Shock Gear", "zap", "Phrase", '"zap"', "Excludes queries like 'dog collars that zap'."),
    ("Harmful / Shock Gear", "e-collar", "Phrase", '"e-collar"', "Industry term for electronic shock training gear."),
    ("Harmful / Shock Gear", "ecollar", "Phrase", '"ecollar"', "Prevents competitor brand and shock device matches."),
    ("Harmful / Shock Gear", "prong", "Phrase", '"prong"', "Excludes metal prong training collars."),
    ("Harmful / Shock Gear", "pinch collar", "Phrase", '"pinch collar"', "Excludes pinch training devices."),
    ("Harmful / Shock Gear", "choke chain", "Phrase", '"choke chain"', "Excludes metal choke chains."),
    ("Harmful / Shock Gear", "choke collar", "Phrase", '"choke collar"', "Excludes choking training collars."),
    ("Harmful / Shock Gear", "citronella", "Phrase", '"citronella"', "Pet Mode does not sell citronella spray collars."),
    ("Harmful / Shock Gear", "spray collar", "Phrase", '"spray collar"', "Excludes spray-based deterrent collars."),
    ("Harmful / Shock Gear", "remote shock", "Phrase", '"remote shock"', "Excludes remote-controlled shock devices."),

    # 2. Competitor Brands & Retailers
    ("Competitor Brands", "costco", "Phrase", '"costco"', "Prevents matching queries like 'costco poo bags'."),
    ("Competitor Brands", "gulpup", "Phrase", '"gulpup"', "Direct competitor brand."),
    ("Competitor Brands", "petsafe", "Phrase", '"petsafe"', "Major pet tech competitor (NanoBark, ScoopFree)."),
    ("Competitor Brands", "pet safe", "Phrase", '"pet safe"', "Alternative spacing for PetSafe."),
    ("Competitor Brands", "ruffwear", "Phrase", '"ruffwear"', "High-end outdoor dog gear brand."),
    ("Competitor Brands", "julius k9", "Phrase", '"julius k9"', "Competitor harness and leash brand."),
    ("Competitor Brands", "scruffs", "Phrase", '"scruffs"', "Competitor dog bed & cooling mat brand."),
    ("Competitor Brands", "trixie", "Phrase", '"trixie"', "Budget pet accessory brand."),
    ("Competitor Brands", "furminator", "Phrase", '"furminator"', "De-shedding tool competitor."),
    ("Competitor Brands", "halty", "Phrase", '"halty"', "Headcollar training brand."),
    ("Competitor Brands", "halti", "Phrase", '"halti"', "Alternative spelling for Halti."),
    ("Competitor Brands", "gentle leader", "Phrase", '"gentle leader"', "Headcollar competitor."),
    ("Competitor Brands", "earth rated", "Phrase", '"earth rated"', "Poo bag brand competitor."),
    ("Competitor Brands", "therapet", "Phrase", '"therapet"', "Anxiety collar competitor."),
    ("Competitor Brands", "argos", "Phrase", '"argos"', "High-street retail catalog store."),
    ("Competitor Brands", "dunelm", "Phrase", '"dunelm"', "Home furnishing store selling budget pet mats."),
    ("Competitor Brands", "b&m", "Phrase", '"b&m"', "Discount high-street chain."),
    ("Competitor Brands", "home bargains", "Phrase", '"home bargains"', "Discount retailer."),
    ("Competitor Brands", "asda", "Phrase", '"asda"', "Supermarket pet aisle queries."),
    ("Competitor Brands", "tesco", "Phrase", '"tesco"', "Supermarket pet aisle queries."),
    ("Competitor Brands", "tk maxx", "Phrase", '"tk maxx"', "Off-price department store."),
    ("Competitor Brands", "ebay", "Phrase", '"ebay"', "Second-hand / marketplace searchers."),
    ("Competitor Brands", "temu", "Phrase", '"temu"', "Ultra-cheap marketplace searchers."),
    ("Competitor Brands", "shein", "Phrase", '"shein"', "Ultra-cheap fashion/marketplace searchers."),
    ("Competitor Brands", "aliexpress", "Phrase", '"aliexpress"', "Direct-from-China wholesale searchers."),
    ("Competitor Brands", "zooplus", "Phrase", '"zooplus"', "Large online pet superstore."),
    ("Competitor Brands", "viovet", "Phrase", '"viovet"', "Online pharmacy/pet food retailer."),
    ("Competitor Brands", "vet uk", "Phrase", '"vet uk"', "Online pet medicine retailer."),

    # 3. Non-Pet & Irrelevant Species
    ("Irrelevant Species & Products", "child", "Phrase", '"child"', "PMax matching GPS pet trackers to child tracking."),
    ("Irrelevant Species & Products", "toddler", "Phrase", '"toddler"', "PMax matching trackers to toddlers."),
    ("Irrelevant Species & Products", "baby", "Phrase", '"baby"', "Excludes baby car seats, baby trackers."),
    ("Irrelevant Species & Products", "human", "Phrase", '"human"', "Excludes human beds, human toothpaste queries."),
    ("Irrelevant Species & Products", "rabbit", "Phrase", '"rabbit"', "Pet Mode does not sell small animal / rabbit products."),
    ("Irrelevant Species & Products", "guinea pig", "Phrase", '"guinea pig"', "Excludes guinea pig clippers / bottles."),
    ("Irrelevant Species & Products", "hamster", "Phrase", '"hamster"', "Excludes rodent queries."),
    ("Irrelevant Species & Products", "horse", "Phrase", '"horse"', "Excludes equine supplies."),
    ("Irrelevant Species & Products", "equine", "Phrase", '"equine"', "Excludes equestrian products."),
    ("Irrelevant Species & Products", "bird", "Phrase", '"bird"', "Excludes caged bird / parrot supplies."),
    ("Irrelevant Species & Products", "reptile", "Phrase", '"reptile"', "Excludes vivarium / lizard heat mats."),
    ("Irrelevant Species & Products", "fish", "Phrase", '"fish"', "Excludes aquarium filters / tanks."),

    # 4. Cleaning Machines & Hardware
    ("Machinery & Hardware", "vacuum", "Phrase", '"vacuum"', "PMax matching pet mats/brushes to household vacuum cleaners."),
    ("Machinery & Hardware", "rug doctor", "Phrase", '"rug doctor"', "Excludes carpet cleaning machine rentals."),
    ("Machinery & Hardware", "carpet cleaner machine", "Phrase", '"carpet cleaner machine"', "Excludes heavy carpet cleaning hardware."),
    ("Machinery & Hardware", "bissell", "Phrase", '"bissell"', "Excludes wet vacuum / spot cleaner brand."),
    ("Machinery & Hardware", "vax", "Phrase", '"vax"', "Excludes vacuum cleaner brand."),
    ("Machinery & Hardware", "washing machine", "Phrase", '"washing machine"', "Excludes appliance queries."),

    # 5. Low Intent / Informational / Bargain
    ("Low-Intent & Informational", "how to", "Phrase", '"how to"', "Over 800 informational blog searches (e.g. 'how to stop barking')."),
    ("Low-Intent & Informational", "diy", "Phrase", '"diy"', "Users seeking to build home-made items."),
    ("Low-Intent & Informational", "make your own", "Phrase", '"make your own"', "Do-it-yourself searchers."),
    ("Low-Intent & Informational", "homemade", "Phrase", '"homemade"', "DIY recipes and remedies."),
    ("Low-Intent & Informational", "recipe", "Phrase", '"recipe"', "Food/treat preparation recipes."),
    ("Low-Intent & Informational", "rspca", "Phrase", '"rspca"', "Informational charity searches."),
    ("Low-Intent & Informational", "jobs", "Phrase", '"jobs"', "Employment seekers."),
    ("Low-Intent & Informational", "careers", "Phrase", '"careers"', "Job seekers."),
    ("Low-Intent & Informational", "wholesale", "Phrase", '"wholesale"', "B2B bulk buyers."),
    ("Low-Intent & Informational", "second hand", "Phrase", '"second hand"', "Used product bargain hunters."),
    ("Low-Intent & Informational", "used", "Phrase", '"used"', "Prevents matching with pre-owned items."),
    ("Low-Intent & Informational", "cheap", "Phrase", '"cheap"', "Ultra-budget shoppers with high cart abandonment."),
    ("Low-Intent & Informational", "free voucher", "Phrase", '"free voucher"', "Prevents coupon seekers without blocking hands-free leads."),
    ("Low-Intent & Informational", "free discount", "Phrase", '"free discount"', "Prevents coupon scarpers."),

    # 6. Specific High-Spend Non-Converting Exact Queries
    ("High-Spend Zero-Converters", "dog water bottle", "Exact", '[dog water bottle]', "Spent £10.01 with 16 clicks and 0 conversions."),
    ("High-Spend Zero-Converters", "best anti bark collar uk reviews", "Exact", '[best anti bark collar uk reviews]', "Spent £8.58 with 2 clicks and 0 conversions."),
    ("High-Spend Zero-Converters", "cat tracker collar", "Exact", '[cat tracker collar]', "Spent £5.05 with 10 clicks and 0 conversions."),
    ("High-Spend Zero-Converters", "best anti bark collar rspca uk", "Exact", '[best anti bark collar rspca uk]', "Spent £4.82 with 2 clicks and 0 conversions."),
    ("High-Spend Zero-Converters", "cooling mats for cats", "Exact", '[cooling mats for cats]', "Spent £4.12 with 3 clicks and 0 conversions."),
    ("High-Spend Zero-Converters", "air tag cat collar", "Exact", '[air tag cat collar]', "Spent £3.94 with 4 clicks and 0 conversions."),
    ("High-Spend Zero-Converters", "poop bag dispenser", "Exact", '[poop bag dispenser]', "Spent £3.80 with 2 clicks and 0 conversions."),
    ("High-Spend Zero-Converters", "biodegradable dog poo bags uk", "Exact", '[biodegradable dog poo bags uk]', "Spent £3.66 with 1 click and 0 conversions."),
    ("High-Spend Zero-Converters", "dog running lead", "Exact", '[dog running lead]', "Spent £2.73 with 6 clicks and 0 conversions."),
    ("High-Spend Zero-Converters", "double dog lead", "Exact", '[double dog lead]', "Spent £2.88 with 2 clicks and 0 conversions.")
]

# Write to Excel
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Negative Keywords List"
ws.views.sheetView[0].showGridLines = True

# Styling
hdr_font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
hdr_fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
zebra_fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
white_fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
reg_font = Font(name="Calibri", size=9.5)
bold_font = Font(name="Calibri", size=9.5, bold=True)
thin_side = Side(border_style="thin", color="CBD5E1")
cell_border = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)

headers = ["Category", "Keyword", "Match Type", "Google Ads Import Format", "Rationale & Spend Protection"]
for c_idx, h in enumerate(headers, start=1):
    c = ws.cell(row=1, column=c_idx, value=h)
    c.font = hdr_font
    c.fill = hdr_fill
    c.alignment = Alignment(horizontal="center", vertical="center")
    c.border = cell_border
ws.row_dimensions[1].height = 25

for r_idx, row_val in enumerate(negatives_data, start=2):
    fill_to_use = zebra_fill if (r_idx % 2 == 1) else white_fill
    for c_idx, val in enumerate(row_val, start=1):
        cell = ws.cell(row=r_idx, column=c_idx, value=val)
        cell.font = bold_font if c_idx in [1, 2, 4] else reg_font
        cell.fill = fill_to_use
        cell.border = cell_border
        if c_idx in [1, 3]:
            cell.alignment = Alignment(horizontal="center", vertical="center")
        else:
            cell.alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[r_idx].height = 20

col_widths = {1: 28, 2: 26, 3: 15, 4: 34, 5: 65}
for col, w in col_widths.items():
    ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = w

xlsx_path = "data/Pet Mode/Google Ads/Pet_Mode_Negative_Keywords_List.xlsx"
wb.save(xlsx_path)
print(f"Saved Excel negative keywords list to: {xlsx_path}")

# Write to CSV (Google Ads bulk upload compatible)
csv_path = "data/Pet Mode/Google Ads/Pet_Mode_Negative_Keywords_Import.csv"
with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Criterion", "Match Type", "Category", "Rationale"])
    for cat, kw, mtype, g_fmt, rat in negatives_data:
        writer.writerow([g_fmt, mtype, cat, rat])

print(f"Saved CSV negative keywords import file to: {csv_path}")
