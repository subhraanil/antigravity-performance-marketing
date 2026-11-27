import os
import sys
import dotenv
from datetime import datetime

# Add project root to path for imports if needed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from execution import ads_performance
from execution import sheet_handler

def main():
    # Load environment variables
    dotenv.load_dotenv()
    
    customer_id = os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID") # Or specific client customer ID
    spreadsheet_id = os.getenv("SPREADSHEET_ID")
    
    if not customer_id:
        print("Error: GOOGLE_ADS_LOGIN_CUSTOMER_ID is missing in .env")
        return
    if not spreadsheet_id:
        print("Error: SPREADSHEET_ID is missing in .env")
        return

    print("Fetching weekly performance data from Google Ads...")
    data = ads_performance.fetch_weekly_performance(customer_id)
    
    if not data:
        print("No data fetched or error occurred.")
        return

    print("Data fetched successfully:")
    print(data)

    # Format data for Google Sheets
    # Columns: Date Range, Clicks, Impressions, CTR, Cost, Conversions, timestamp
    row = [
        f"{data['start_date']} to {data['end_date']}",
        data['clicks'],
        data['impressions'],
        f"{data['ctr']:.2f}%",
        data['cost'],
        data['conversions'],
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ]

    print("Appending data to Google Sheet...")
    result = sheet_handler.append_data(spreadsheet_id, [row])
    
    if result:
        print("Successfully appended weekly report data.")
    else:
        print("Failed to append data.")

if __name__ == "__main__":
    main()
