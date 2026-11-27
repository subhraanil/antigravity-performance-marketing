import os
import argparse
from dotenv import load_dotenv
import pandas as pd
from google.ads.googleads.client import GoogleAdsClient
from google.oauth2 import service_account

# Load environment variables
load_dotenv()

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

def get_google_ads_client():
    # Setup OAuth2 Flow using credentials.json
    base_dir = os.path.dirname(os.path.dirname(__file__))
    credentials_path = os.path.join(base_dir, 'credentials.json')
    token_path = os.path.join(base_dir, 'token_ads.json')
    
    if not os.path.exists(credentials_path):
        raise FileNotFoundError(f"credentials.json not found at {credentials_path}")

    scopes = ['https://www.googleapis.com/auth/adwords']
    creds = None

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, scopes)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, scopes)
            creds = flow.run_local_server(port=0)
            
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    # Initialize the Google Ads client
    client = GoogleAdsClient(
        credentials=creds,
        developer_token=os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN"),
        login_customer_id=os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID")
    )
    return client

def run_campaign_report(client, customer_id):
    ga_service = client.get_service("GoogleAdsService")

    # A simple query to get campaign performance
    query = """
        SELECT
          campaign.id,
          campaign.name,
          campaign.status,
          metrics.impressions,
          metrics.clicks,
          metrics.cost_micros,
          metrics.conversions
        FROM campaign
        WHERE segments.date DURING LAST_30_DAYS
        ORDER BY metrics.impressions DESC
    """

    print(f"Fetching report for customer_id: {customer_id}")
    
    # Issues a search request using streaming.
    stream = ga_service.search_stream(customer_id=str(customer_id), query=query)

    data = []
    for batch in stream:
        for row in batch.results:
            data.append({
                'Campaign ID': row.campaign.id,
                'Campaign Name': row.campaign.name,
                'Status': row.campaign.status.name,
                'Impressions': row.metrics.impressions,
                'Clicks': row.metrics.clicks,
                'Cost': row.metrics.cost_micros / 1000000.0,
                'Conversions': row.metrics.conversions,
            })

    if not data:
        print("No campaigns found or no data for the last 30 days.")
        return

    df = pd.DataFrame(data)
    print("Report generated successfully.")
    
    # Save the report
    reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    report_path = os.path.join(reports_dir, 'google_ads_campaign_report.csv')
    df.to_csv(report_path, index=False)
    
    print(f"Report saved to: {report_path}")
    print("\nSummary:")
    print(df.head())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Google Ads Campaign Report")
    parser.add_argument("--customer-id", help="The Google Ads Customer ID (without hyphens)", default=os.getenv("GOOGLE_ADS_CUSTOMER_ID").replace("-", "") if os.getenv("GOOGLE_ADS_CUSTOMER_ID") else None)
    args = parser.parse_args()

    if not args.customer_id:
        print("Error: Customer ID is required. Either pass --customer-id or set GOOGLE_ADS_CUSTOMER_ID in .env")
        exit(1)

    client = get_google_ads_client()
    run_campaign_report(client, args.customer_id)
