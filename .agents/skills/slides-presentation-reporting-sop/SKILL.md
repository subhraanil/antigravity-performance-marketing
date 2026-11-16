---
name: slides-presentation-reporting-sop
description: >-
  Extract weekly/monthly marketing KPI metrics from Google Sheets and automatically generate executive PowerPoint (PPTX) and Google Slides presentation decks with dynamic SVG charts, scorecards, and performance tables.
---

# Google Sheets to Executive Presentation Reporting SOP

## Overview
A standard operating procedure to extract weekly and monthly marketing KPI metrics from Google Sheets and automatically generate executive PowerPoint (PPTX) and Google Slides presentation decks with dynamic charts, KPI scorecards, and channel performance tables.

---

## Prerequisites
- Google Cloud Project with Google Sheets API and Google Slides API enabled.
- `service_account.json` or `credentials.json` placed in the project root.
- Python dependencies installed:
  ```powershell
  pip install google-api-python-client google-auth pandas matplotlib python-pptx
  ```

---

## Trigger Conditions
- Weekly client performance reporting meetings.
- Monthly executive business reviews (EBR).
- Quarterly strategic media and revenue rebalancing presentations.

---

## Execution Methods

### Method 1: Comprehensive Automated Deck Generator (`sheets_to_slides.py`)
Parses metrics, builds period-over-period comparison tables, and plots spend vs conversion velocity charts:
```powershell
python scripts/sheets_to_slides.py \
  --sheet-id "YOUR_GOOGLE_SHEET_ID" \
  --client-name "Client Brand Name" \
  --period "Current Month 2026" \
  --output "reports/Executive_Performance_Deck.pptx"
```

### Method 2: Rapid Single-Sheet Report Generator (`generate_pptx_report.py`)
Generates a quick graphical presentation deck directly from a target Google Sheet:
```powershell
python scripts/generate_pptx_report.py \
  --sheet_id "YOUR_GOOGLE_SHEET_ID" \
  --title "Weekly Performance Report"
```

---

## Executive Narrative & Slide Layout

Ensure every presentation follows the 5-slide executive narrative structure:
1. **Slide 1: Executive Scorecard**: Total media spend, Blended MER, Net Revenue, and Blended CPA vs agreed KPI benchmarks.
2. **Slide 2: Channel Performance Matrix**: Side-by-side comparison of Meta Ads vs Google Ads vs Organic efficiency.
3. **Slide 3: High-Impact Wins**: Top creative performers, wasted placement burn elimination, and negative keyword cost savings.
4. **Slide 4: Bottlenecks & Leakages**: Identified friction points (e.g. mobile vs desktop conversion disparity, high cart abandonment).
5. **Slide 5: 30-Day Forward Roadmap**: Budget reallocation recommendations and upcoming sprint test priorities.

---

## Export & Client Delivery
1. Review generated `.pptx` deck locally.
2. Upload to Google Drive to open natively in Google Slides for collaborative team commenting.
3. Export high-resolution PDF version for executive email delivery.
