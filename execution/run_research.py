import argparse
import os
import sys
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime

# Add current directory to path to allow imports if run from root
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from execution import keyword_planner
from execution import sheet_handler

def main():
    parser = argparse.ArgumentParser(description="Run SEO Keyword Research")
    parser.add_argument("--seed", required=True, help="Seed keyword")
    parser.add_argument("--location", default="2840", help="Location ID (default US: 2840)") # 2840 is US
    parser.add_argument("--competitor", help="Competitor URL (optional)")
    parser.add_argument("--folder", help="Google Drive Folder ID (optional)")
    parser.add_argument("--customer_id", help="Google Ads Customer ID")
    
    args = parser.parse_args()
    
    # Load env
    load_dotenv()
    customer_id = args.customer_id or os.getenv("GOOGLE_ADS_CUSTOMER_ID")
    
    if not customer_id:
        print("Error: Google Ads Customer ID is required (via --customer_id or GOOGLE_ADS_CUSTOMER_ID env var).")
        return

    print(f"Starting research for '{args.seed}'...")
    
    # 1. Fetch Keywords
    print("Fetching keywords from Google Ads...")
    keywords = keyword_planner.fetch_keywords(
        customer_id=customer_id,
        seed_keyword=args.seed,
        location_id=args.location,
        competitor_url=args.competitor
    )
    
    if not keywords:
        print("No keywords found or error occurred.")
        return

    print(f"Found {len(keywords)} keywords.")

    # 2. Prepare Data for Sheet
    # Header
    sheet_data = [['Keyword', 'Avg. Monthly Searches', 'Competition', 'CPC Low', 'CPC High']]
    # Rows
    for k in keywords:
        sheet_data.append([
            k['keyword'],
            k['avg_monthly_searches'],
            k['competition'],
            k['cpc_low'],
            k['cpc_high']
        ])

    # 3. Create Sheet
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    title = f"Keyword Research - {args.seed} - {timestamp}"
    
    print("Creating Google Sheet...")
    sheet_id, sheet_url = sheet_handler.create_sheet(title, sheet_data)
    
    if sheet_url:
        print(f"Success! Sheet created: {sheet_url}")
        
        # 4. Move to Folder if requested
        if args.folder:
            print(f"Moving to folder {args.folder}...")
            sheet_handler.move_to_folder(sheet_id, args.folder)
            print("Moved.")
    else:
        print("Failed to create sheet.")

if __name__ == "__main__":
    main()
