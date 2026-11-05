import argparse
import os
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pandas as pd
from google.oauth2 import service_account

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']

def get_service():
    creds = None
    print("Attempting to authenticate...")
    
    # 1. Try Service Account (Preferred for Automation)
    if os.path.exists('service_account.json'):
        try:
            print("Found service_account.json. Using Service Account...")
            creds = service_account.Credentials.from_service_account_file(
                'service_account.json', scopes=SCOPES)
            # Service account credentials are valid by default
            service = build('searchconsole', 'v1', credentials=creds)
            print("Authentication via Service Account successful.")
            return service
        except Exception as e:
            print(f"Service account authentication failed: {e}")

    # 2. Try existing Token
    if os.path.exists('token.json'):
        print("Found token.json. Using OAuth2 Token...")
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # 3. Handle Refresh or Fallback
    if creds and creds.expired and creds.refresh_token:
        try:
            print("Refreshing OAuth2 token...")
            creds.refresh(Request())
        except Exception as e:
            print(f"Token refresh failed: {e}")
            creds = None

    if not creds:
        print("Error: No valid credentials found.")
        print("If using a Service Account, ensure 'service_account.json' is in the root.")
        print("Note: Automated OAuth2 login is disabled to prevent hanging.")
        return None

    service = build('searchconsole', 'v1', credentials=creds)
    return service

def main():
    parser = argparse.ArgumentParser(description='Query Google Search Console Performance Data')
    parser.add_argument('--site-url', required=True, help='The URL of the property in GSC')
    parser.add_argument('--start-date', required=True, help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', required=True, help='End date (YYYY-MM-DD)')
    parser.add_argument('--dimensions', help='Comma-separated dimensions (date, query, page, country, device)', default='date')
    parser.add_argument('--limit', type=int, help='Max rows to return', default=1000)

    args = parser.parse_args()

    service = get_service()
    if not service:
        return

    request = {
        'startDate': args.start_date,
        'endDate': args.end_date,
        'dimensions': args.dimensions.split(','),
        'rowLimit': args.limit
    }

    try:
        response = service.searchanalytics().query(siteUrl=args.site_url, body=request).execute()
        rows = response.get('rows', [])

        if not rows:
            print("No data found for the given criteria.")
            return

        data = []
        for row in rows:
            item = {}
            # Dimensions can be a list if multiple dimensions requested, or just values
            # The API returns 'keys' which corresponds to dimensions values
            keys = row.get('keys', [])
            for i, dim in enumerate(args.dimensions.split(',')):
                if i < len(keys):
                    item[dim] = keys[i]
            
            item['clicks'] = row.get('clicks')
            item['impressions'] = row.get('impressions')
            item['ctr'] = row.get('ctr')
            item['position'] = row.get('position')
            data.append(item)

        df = pd.DataFrame(data)
        print(df.to_string(index=False))

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
