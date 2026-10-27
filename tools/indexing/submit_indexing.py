import argparse
import os
import json
from urllib.parse import urlparse
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import requests
from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/indexing"]
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"

def get_authenticated_session(service_account_file):
    if not os.path.exists(service_account_file):
        print(f"Error: Service account file '{service_account_file}' not found.")
        print("Please ensure you have created a service account and downloaded the JSON key file.")
        return None

    creds = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=SCOPES
    )
    
    return creds

def submit_url(service_account_file, url, action="URL_UPDATED"):
    creds = get_authenticated_session(service_account_file)
    if not creds:
        return

    # Create a fresh session and authorize it
    session = requests.Session()
    creds.refresh(Request())
    session.headers.update({'Authorization': f'Bearer {creds.token}'})

    content = {
        "url": url,
        "type": action
    }

    try:
        response = session.post(ENDPOINT, json=content)
        response.raise_for_status()
        print(f"Successfully submitted {url} with action {action} to Google Search Console.")
        print("Response:", json.dumps(response.json(), indent=2))
    except requests.exceptions.HTTPError as err:
        print(f"Google API HTTP Error occurred: {err}")
        print("Response content:", response.content.decode('utf-8'))
    except Exception as err:
        print(f"Google API Error occurred: {err}")

    # IndexNow Submission for Bing/Yandex
    indexnow_key = os.getenv("INDEXNOW_KEY")
    if indexnow_key and action == "URL_UPDATED":
        try:
            parsed = urlparse(url)
            host = parsed.netloc
            indexnow_url = "https://api.indexnow.org/indexnow"
            payload = {
                "host": host,
                "key": indexnow_key,
                "keyLocation": f"https://{host}/{indexnow_key}.txt",
                "urlList": [url]
            }
            res = requests.post(indexnow_url, json=payload, headers={"Content-Type": "application/json; charset=utf-8"})
            if res.status_code in (200, 202):
                print(f"Successfully submitted {url} to IndexNow (Bing/Yandex).")
            else:
                print(f"IndexNow submission for {url} returned status: {res.status_code} - {res.text}")
        except Exception as e:
            print(f"Failed to submit to IndexNow: {e}")

def main():
    parser = argparse.ArgumentParser(description="Submit URLs to Google Indexing API.")
    parser.add_argument("--url", required=True, help="The URL to submit for indexing.")
    parser.add_argument("--action", choices=["URL_UPDATED", "URL_DELETED"], default="URL_UPDATED", help="The type of notification (URL_UPDATED or URL_DELETED). Default is URL_UPDATED.")
    parser.add_argument("--key-file", default="service_account.json", help="Path to the service account JSON key file. Default is 'service_account.json' in the current directory.")

    args = parser.parse_args()

    submit_url(args.key_file, args.url, args.action)

if __name__ == "__main__":
    main()
