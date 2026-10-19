# Google Shopping & Google Merchant Center (GMC) Feed Playbook
# Proven Architecture Derived from Live Multi-Country E-Commerce Audits

## 1. Google Merchant Center Feed Architecture

Google Shopping and Performance Max campaigns live and die by feed quality. Google's auction algorithm extracts search query relevance directly from feed attributes rather than keywords.

### Primary Feed File Formats:
- **TSV (Tab-Separated Values - Recommended)**: Immune to comma parsing bugs in descriptions and titles. Highest upload reliability in GMC.
- **CSV (Comma-Separated Values)**: Standard export format from Shopify/WooCommerce; requires strict quotation of multi-line descriptions.
- **Content API / Supplement Feeds**: Used for real-time price and inventory updates.

---

## 2. Mandatory Product Attributes Specification

| Attribute | Format / Constraint | Performance Optimization Best Practice |
| :--- | :--- | :--- |
| `id` | Alphanumeric (Max 50 chars) | Must remain persistent forever. Format: `SKU_VARIANT_ID` |
| `title` | Max 150 chars (70 visible) | `[Brand] + [Product Name] + [Key Spec/Material] + [Color] + [Size]` |
| `description` | Max 5,000 chars | Lead with primary use-case, materials, dimensions, and benefits in first 500 chars |
| `link` | Absolute URL (`https://`) | Include primary variant URL with clean query parameters |
| `image_link` | Minimum 800x800 px | Clean white background, no promotional watermarks, badges, or text |
| `additional_image_link`| Comma-separated URLs | Lifestyle images, dimension charts, package contents |
| `price` | E.g. `29.99 GBP` | Must match live on-page checkout price down to the penny |
| `availability` | `in_stock` \| `out_of_stock` | Real-time sync; GMC suspends accounts with availability discrepancies |
| `brand` | Text | Official brand name |
| `gtin` | EAN / UPC / ISBN (12-14 digits) | **Critical**: Products with valid GTINs achieve 40%+ higher impression share |
| `mpn` | Manufacturer Part Number | Required if GTIN is unavailable alongside `identifier_exists: false` |
| `google_product_category` | Numeric ID or Taxonomy string | Map to deepest possible level (e.g., `Animals & Pet Supplies > Pet Supplies`) |

---

## 3. Product Variant & Apparel Structuring

When selling products with multiple sizes, colors, or materials, you **must** use `item_group_id`:

```tsv
id	title	item_group_id	color	size	gender	age_group
PET-BED-RED-S	Orthopedic Dog Bed - Washable Memory Foam - Red (Small)	PET-BED-01	Red	Small	unisex	all
PET-BED-RED-M	Orthopedic Dog Bed - Washable Memory Foam - Red (Medium)	PET-BED-01	Red	Medium	unisex	all
PET-BED-BLU-S	Orthopedic Dog Bed - Washable Memory Foam - Blue (Small)	PET-BED-01	Blue	Small	unisex	all
```

---

## 4. Custom Labels Strategy (`custom_label_0` to `custom_label_4`)

Segment your PMax and Standard Shopping campaigns using strategic custom labels:

- **`custom_label_0` (Margin Tier)**: `high_margin` (>60%), `medium_margin` (40-60%), `low_margin` (<40%).
- **`custom_label_1` (Sales Velocity)**: `bestseller` (Top 20% revenue drivers), `steady`, `slow_mover`, `dead_stock`.
- **`custom_label_2` (Seasonality)**: `q4_holiday`, `summer_core`, `evergreen`.
- **`custom_label_3` (Price Tier)**: `under_25`, `25_to_50`, `50_to_100`, `over_100`.

---

## 5. Resolving Common GMC Disapproval Flags

1. **"Limited Performance Due to Missing GTIN"**:
   - If products are custom or white-label without an official UPC/EAN, add `identifier_exists` = `no`.
2. **"Mismatched Value (Price / Currency)"**:
   - Ensure landing page displays the exact currency of the target country feed. Never send USD prices to a UK feed (`GBP`).
3. **"Promotional Overlay on Image"**:
   - Replace primary `image_link` with clean product-only photography; move images with badges/text to `additional_image_link`.
4. **"Insufficient Contact Information / Policy Missing"**:
   - Merchant Center requires physical business address, working support telephone number, and transparent 30-day refund policy links in the website footer.
