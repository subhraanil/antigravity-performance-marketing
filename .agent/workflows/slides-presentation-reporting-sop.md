# Workflow: Google Sheets to Executive Presentation Reporting SOP

## Overview
A standard operating procedure to extract weekly/monthly marketing KPI metrics from Google Sheets and automatically generate executive PowerPoint (PPTX) and Google Slides presentation decks with dynamic SVG charts, scorecards, and performance tables.

---

## Trigger Conditions
- Weekly client performance reporting calls.
- Monthly executive business reviews (EBR).
- Quarterly strategic media and revenue rebalancing presentations.

---

## Step-by-Step SOP

### Step 1: Data Preparation in Google Sheets
1. Verify Google Sheet contains standardized reporting tabs:
   - `Weekly_Metrics`: Spend, Impressions, Clicks, CPC, Leads, CPA, ROAS, Revenue.
   - `Channel_Breakdown`: Meta Ads, Google Search, Google Shopping/PMax, Email, Organic.
   - `Action_Items`: Completed optimizations and upcoming sprint initiatives.
2. Confirm Google Sheet permissions allow service account read access.

### Step 2: Automated Deck Generation
1. Execute the presentation generator script:
   ```powershell
   python scripts/sheets_to_slides.py \
     --sheet-id "YOUR_GOOGLE_SHEET_ID" \
     --client-name "Client Brand Name" \
     --period "October 2026" \
     --output "reports/Executive_Performance_Deck.pptx"
   ```
2. The generator parses metrics, builds comparison tables (Current vs Previous Period), and plots spend vs conversion velocity charts.

### Step 3: Executive Narrative & Slide Layout
Ensure the resulting deck follows the 5-slide executive narrative:
1. **Slide 1: Executive Scorecard**: Total media spend, Blended MER, Net Revenue, and Blended CPA vs agreed KPI benchmarks.
2. **Slide 2: Channel Performance Matrix**: Side-by-side comparison of Meta vs Google Ads efficiency.
3. **Slide 3: High-Impact Wins**: Top creative performers, placement burn elimination, and negative keyword cost savings.
4. **Slide 4: Bottlenecks & Remediation**: Specific leakages identified (e.g. mobile vs desktop conversion disparity).
5. **Slide 5: 30-Day Forward Roadmap**: Budget reallocation recommendations and testing sprint priorities.

### Step 4: Deliverable Export & Client Delivery
1. Review generated `.pptx` deck.
2. Upload to Google Drive to open natively in Google Slides for collaborative commenting.
3. Export PDF version for executive email delivery.
