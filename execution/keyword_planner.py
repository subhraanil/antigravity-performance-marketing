import os
import sys
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Load environment variables (assumes .env is loaded by main runner or directives)

def fetch_keywords(customer_id, seed_keyword, location_id, competitor_url=None):
    """
    Generates keyword ideas using Google Keyword Planner.
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
        return []

    keyword_plan_idea_service = client.get_service("KeywordPlanIdeaService")
    request = client.get_type("GenerateKeywordIdeasRequest")
    request.customer_id = customer_id
    # Language: English (1000)
    request.language = client.get_service("GoogleAdsService").language_constant_path("1000")
    
    # Location mapping logic would go here. For now, assuming raw ID or mimicking global.
    # request.geo_target_constants = [location_resource_name] 

    request.include_adult_keywords = False
    
    # To generate keyword ideas based on a keyword_seed
    if not competitor_url:
        request.keyword_seed.keywords.extend([seed_keyword])
    
    # To generate keyword ideas based on a url_seed (if provided and preferred)
    if competitor_url:
         request.url_seed.url = competitor_url
         if seed_keyword:
             # Depending on API version/mode, might mix both or stick to one. 
             # Usually UrlSeed OR KeywordSeed. We'll prioritize Seed + Site refinement if possible,
             # but standard is one or the other for 'GenerateKeywordIdeas'.
             # Let's stick to KeywordSeed and optionally add site refinement if supported,
             # Or just use UrlSeed if seed_keyword is empty.
             pass

    # Note: This is an implementation skeleton. 
    # Real implementation requires handling specific API details for location resource names.

    try:
        response = keyword_plan_idea_service.generate_keyword_ideas(request=request)
        results = []
        for row in response:
            metrics = row.keyword_idea_metrics
            results.append({
                "keyword": row.text,
                "avg_monthly_searches": metrics.avg_monthly_searches,
                "competition": metrics.competition.name,
                "cpc_low": metrics.low_top_of_page_bid_micros / 1000000 if metrics.low_top_of_page_bid_micros else 0,
                "cpc_high": metrics.high_top_of_page_bid_micros / 1000000 if metrics.high_top_of_page_bid_micros else 0
            })
        
        # Sort by search volume
        results.sort(key=lambda x: x["avg_monthly_searches"], reverse=True)
        return results

    except GoogleAdsException as ex:
        print(f"Request with ID '{ex.request_id}' failed with status "
              f"'{ex.error.code().name}' and includes the following errors:")
        for error in ex.failure.errors:
            print(f"\tError with message '{error.message}'.")
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        return []

if __name__ == "__main__":
    # Example CLI usage
    # python keyword_planner.py [customer_id] [seed_keyword] [location_id] [competitor_url]
    # For now ensuring it runs without error if called empty
    print("Keyword Planner execution module loaded.")
