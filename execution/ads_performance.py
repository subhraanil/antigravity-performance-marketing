import os
import sys
from datetime import datetime, timedelta
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
import pandas as pd

def fetch_weekly_performance(customer_id, end_date=None):
    """
    Fetches weekly performance data (Clicks, Impressions, CTR, Cost, Conversions)
    from Google Ads for the last 7 days ending on end_date (default: yesterday).
    """
    try:
        # Load credentials from environment variables
        credentials = {
            "developer_token": os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN"),
            "client_id": os.getenv("GOOGLE_ADS_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_ADS_CLIENT_SECRET"),
            "refresh_token": os.getenv("GOOGLE_ADS_REFRESH_TOKEN"),
            "login_customer_id": os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID"),
            "use_proto_plus": True
        }
        client = GoogleAdsClient.load_from_dict(credentials)
    except Exception as e:
        print(f"Error initializing Google Ads Client: {e}")
        return None

    ga_service = client.get_service("GoogleAdsService")

    if end_date is None:
        end_date = datetime.now() - timedelta(days=1)
    else:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    start_date = end_date - timedelta(days=6)

    str_end_date = end_date.strftime("%Y-%m-%d")
    str_start_date = start_date.strftime("%Y-%m-%d")

    print(f"Fetching data from {str_start_date} to {str_end_date}...")

    query = f"""
        SELECT 
            metrics.clicks, 
            metrics.impressions, 
            metrics.ctr, 
            metrics.cost_micros, 
            metrics.conversions 
        FROM customer 
        WHERE segments.date BETWEEN '{str_start_date}' AND '{str_end_date}'
    """

    # Issue a search request using streaming.
    try:
        stream = ga_service.search_stream(customer_id=customer_id, query=query)
        
        total_clicks = 0
        total_impressions = 0
        total_cost_micros = 0
        total_conversions = 0.0

        for batch in stream:
            for row in batch.results:
                metrics = row.metrics
                total_clicks += metrics.clicks
                total_impressions += metrics.impressions
                total_cost_micros += metrics.cost_micros
                total_conversions += metrics.conversions

        # Calculate aggregates
        total_cost = total_cost_micros / 1000000
        ctr = (total_clicks / total_impressions) * 100 if total_impressions > 0 else 0

        return {
            "start_date": str_start_date,
            "end_date": str_end_date,
            "clicks": total_clicks,
            "impressions": total_impressions,
            "ctr": ctr,
            "cost": total_cost,
            "conversions": total_conversions
        }

    except GoogleAdsException as ex:
        print(f"Request with ID '{ex.request_id}' failed with status "
              f"'{ex.error.code().name}' and includes the following errors:")
        for error in ex.failure.errors:
            print(f"\tError with message '{error.message}'.")
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        return None

if __name__ == "__main__":
    print("Ads Performance execution module loaded.")
