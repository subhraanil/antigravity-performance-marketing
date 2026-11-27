import os
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build

SPREADSHEET_ID = '1crkBH4x06SUx1GXE72ErKsVPq36U5kfJu9MczHE_NGg'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

def get_sheets_service():
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("GOOGLE_API_KEY not found in .env")
        return None
        
    service = build('sheets', 'v4', developerKey=api_key)
    return service

def analyze_campaigns():
    service = get_sheets_service()
    if not service:
        return
        
    try:
        # Get spreadsheet metadata to find all sheets (tabs)
        sheet_metadata = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
        sheets = sheet_metadata.get('sheets', '')
        
        all_campaign_data = {}

        for sheet in sheets:
            title = sheet.get("properties", {}).get("title", "")
            
            # Skip specified tabs
            if "remarketing" in title.lower() or "demand gen" in title.lower() or "demandgen" in title.lower():
                print(f"Skipping tab: {title}")
                continue
                
            print(f"Reading tab: {title}")
            
            # Fetch data for the current tab
            range_name = f"'{title}'"
            result = service.spreadsheets().values().get(
                spreadsheetId=SPREADSHEET_ID, range=range_name).execute()
            rows = result.get('values', [])
            
            if not rows:
                print(f"No data found in tab: {title}")
                continue
                
            # Process data
            # Assuming headers are in the first row
            # Date | Impressions | Clicks | Leads | Cost
            # We'll normalize headers to match expected keys
            headers = [h.lower().strip() for h in rows[0]]
            
            # Find indices for required columns
            try:
                date_idx = next(i for i, h in enumerate(headers) if 'date' in h or 'data' in h)
                imp_idx = next(i for i, h in enumerate(headers) if 'impression' in h)
                clk_idx = next(i for i, h in enumerate(headers) if 'click' in h)
                lead_idx = next(i for i, h in enumerate(headers) if 'lead' in h or 'conversion' in h)
                cost_idx = next(i for i, h in enumerate(headers) if 'cost' in h)
            except StopIteration:
                print(f"Could not find required columns (Date, Impression, Clicks, Leads, Cost) in tab: {title}")
                print(f"Found headers: {headers}")
                continue
            
            tab_data = []
            for row in rows[1:]:
                if not row or len(row) <= max(date_idx, imp_idx, clk_idx, lead_idx, cost_idx):
                    continue
                    
                try:
                    date_val = row[date_idx]
                    if not date_val: continue
                    
                    # Clean numeric strings (remove commas, currency symbols)
                    def clean_num(val):
                        if not val: return 0.0
                        return float(str(val).replace(',', '').replace('$', '').replace('£', '').replace('€', '').replace('₹', '').strip())
                    
                    impressions = clean_num(row[imp_idx])
                    clicks = clean_num(row[clk_idx])
                    leads = clean_num(row[lead_idx])
                    cost = clean_num(row[cost_idx])
                    
                    if impressions == 0 and clicks == 0 and cost == 0:
                        continue # Skip empty/zero rows
                        
                    # Calculate derived KPIs
                    cpc = cost / clicks if clicks > 0 else 0
                    ctr = (clicks / impressions) * 100 if impressions > 0 else 0
                    cpl = cost / leads if leads > 0 else 0
                    conv_rate = (leads / clicks) * 100 if clicks > 0 else 0
                    
                    tab_data.append({
                        'Date': date_val,
                        'Impressions': impressions,
                        'Clicks': clicks,
                        'Leads': leads,
                        'Cost': cost,
                        'Avg CPC': round(cpc, 2),
                        'CTR (%)': round(ctr, 2),
                        'Cost per Conv': round(cpl, 2),
                        'Conv Rate (%)': round(conv_rate, 2)
                    })
                except ValueError as e:
                    # Skip rows with invalid numeric data (like totals row)
                    continue
            
            if tab_data:
                df = pd.DataFrame(tab_data)
                all_campaign_data[title] = df
                
                print(f"\n--- Analysis for {title} ---")
                
                # Calculate totals for the tab
                total_imp = df['Impressions'].sum()
                total_clk = df['Clicks'].sum()
                total_leads = df['Leads'].sum()
                total_cost = df['Cost'].sum()
                
                avg_cpc = total_cost / total_clk if total_clk > 0 else 0
                avg_ctr = (total_clk / total_imp) * 100 if total_imp > 0 else 0
                avg_cpl = total_cost / total_leads if total_leads > 0 else 0
                avg_conv_rate = (total_leads / total_clk) * 100 if total_clk > 0 else 0
                
                print(f"Total Impressions: {total_imp:,.0f}")
                print(f"Total Clicks: {total_clk:,.0f}")
                print(f"Total Leads: {total_leads:,.0f}")
                print(f"Total Cost: ${total_cost:,.2f}")
                print(f"Overall Avg CPC: ${avg_cpc:.2f}")
                print(f"Overall CTR: {avg_ctr:.2f}%")
                print(f"Overall Cost per Conv: ${avg_cpl:.2f}")
                print(f"Overall Conv Rate: {avg_conv_rate:.2f}%")
                
                # Save to CSV
                reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')
                os.makedirs(reports_dir, exist_ok=True)
                report_path = os.path.join(reports_dir, f'KPI_Analysis_{title}.csv')
                df.to_csv(report_path, index=False)
                
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    analyze_campaigns()
