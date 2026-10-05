#!/usr/bin/env python3
"""
GA4 Standard UTM Tag Builder for Performance Campaigns.
"""
import argparse
import urllib.parse

def build_utm(url, source, medium, campaign, content=None, term=None):
    parsed = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qs(parsed.query)
    
    params["utm_source"] = [source]
    params["utm_medium"] = [medium]
    params["utm_campaign"] = [campaign]
    if content:
        params["utm_content"] = [content]
    if term:
        params["utm_term"] = [term]
        
    flat_params = {k: v[0] for k, v in params.items()}
    new_query = urllib.parse.urlencode(flat_params)
    result = urllib.parse.urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))
    
    print("-" * 60)
    print("Generated Tagged Destination URL:")
    print(result)
    print("-" * 60)
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build UTM tagged URL")
    parser.add_argument("--url", required=True, help="Base destination URL")
    parser.add_argument("--source", required=True, help="utm_source (e.g. meta, google, linkedin)")
    parser.add_argument("--medium", required=True, help="utm_medium (e.g. paid_social, paid_search, pmax)")
    parser.add_argument("--campaign", required=True, help="utm_campaign name")
    parser.add_argument("--content", help="utm_content (ad name / creative angle)")
    parser.add_argument("--term", help="utm_term (adset name or keyword)")
    args = parser.parse_args()

    build_utm(args.url, args.source, args.medium, args.campaign, args.content, args.term)
