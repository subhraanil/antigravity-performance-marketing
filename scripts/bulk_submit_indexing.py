import json
import requests
import time
from google.oauth2 import service_account
from google.auth.transport.requests import Request

urls_to_submit = [
    "https://www.promotionalproductsnow.au/category/bags/bum-bags",
    "https://www.promotionalproductsnow.au/category/bags/laptops",
    "https://www.promotionalproductsnow.au/category/bags/paper-bags",
    "https://www.promotionalproductsnow.au/category/bags/toiletry-bags",
    "https://www.promotionalproductsnow.au/category/clothing/aprons",
    "https://www.promotionalproductsnow.au/category/clothing/footwear",
    "https://www.promotionalproductsnow.au/category/clothing/hoodies",
    "https://www.promotionalproductsnow.au/category/clothing/jackets",
    "https://www.promotionalproductsnow.au/category/clothing/misc-clothing",
    "https://www.promotionalproductsnow.au/category/clothing/pants",
    "https://www.promotionalproductsnow.au/category/clothing/polo-shirts",
    "https://www.promotionalproductsnow.au/category/clothing/pullovers",
    "https://www.promotionalproductsnow.au/category/clothing/scarves",
    "https://www.promotionalproductsnow.au/category/clothing/shirts",
    "https://www.promotionalproductsnow.au/category/clothing/shorts",
    "https://www.promotionalproductsnow.au/category/clothing/singlets",
    "https://www.promotionalproductsnow.au/category/clothing/skirts",
    "https://www.promotionalproductsnow.au/category/clothing/vests",
    "https://www.promotionalproductsnow.au/category/drinkware/beer-glasses",
    "https://www.promotionalproductsnow.au/category/drinkware/drink-bottles",
    "https://www.promotionalproductsnow.au/category/drinkware/drinking-straws",
    "https://www.promotionalproductsnow.au/category/drinkware/flasks",
    "https://www.promotionalproductsnow.au/category/drinkware/glassware",
    "https://www.promotionalproductsnow.au/category/drinkware/misc-drinkware",
    "https://www.promotionalproductsnow.au/category/drinkware/mugs",
    "https://www.promotionalproductsnow.au/category/drinkware/sports-shakers",
    "https://www.promotionalproductsnow.au/category/drinkware/stubby-holders",
    "https://www.promotionalproductsnow.au/category/drinkware/wine-glasses",
    "https://www.promotionalproductsnow.au/category/exhibitions-&-events/badge-holders",
    "https://www.promotionalproductsnow.au/category/exhibitions-&-events/lanyards",
    "https://www.promotionalproductsnow.au/category/food-&-drink/chocolates",
    "https://www.promotionalproductsnow.au/category/food-&-drink/lollies",
    "https://www.promotionalproductsnow.au/category/fun-&-games/games",
    "https://www.promotionalproductsnow.au/category/fun-&-games/novelty-items",
    "https://www.promotionalproductsnow.au/category/fun-&-games/puzzles",
    "https://www.promotionalproductsnow.au/category/fun-&-games/stress-shapes",
    "https://www.promotionalproductsnow.au/category/headwear/baseball-caps",
    "https://www.promotionalproductsnow.au/category/headwear/bucket-&-sun-hats",
    "https://www.promotionalproductsnow.au/category/headwear/headbands",
    "https://www.promotionalproductsnow.au/category/headwear/misc-headwear",
    "https://www.promotionalproductsnow.au/category/headwear/straw-hats",
    "https://www.promotionalproductsnow.au/category/headwear/trucker-caps",
    "https://www.promotionalproductsnow.au/category/headwear/visors",
    "https://www.promotionalproductsnow.au/category/health-&-personal/lip-balms",
    "https://www.promotionalproductsnow.au/category/health-&-personal/misc-health",
    "https://www.promotionalproductsnow.au/category/health-&-personal/sunscreens",
    "https://www.promotionalproductsnow.au/category/home-&-living/misc-homeware",
    "https://www.promotionalproductsnow.au/category/home-&-living/pet-accessories",
    "https://www.promotionalproductsnow.au/category/home-&-living/picture-frames",
    "https://www.promotionalproductsnow.au/category/home-&-living/watches",
    "https://www.promotionalproductsnow.au/category/keyrings-&-tools/misc-tools",
    "https://www.promotionalproductsnow.au/category/keyrings-&-tools/tape-measures",
    "https://www.promotionalproductsnow.au/category/keyrings-&-tools/tool-sets",
    "https://www.promotionalproductsnow.au/category/keyrings-&-tools/torches",
    "https://www.promotionalproductsnow.au/category/leisure-&-outdoors/bbq-sets",
    "https://www.promotionalproductsnow.au/category/leisure-&-outdoors/camp-&-hike",
    "https://www.promotionalproductsnow.au/category/leisure-&-outdoors/chairs",
    "https://www.promotionalproductsnow.au/category/leisure-&-outdoors/golf-accessories",
    "https://www.promotionalproductsnow.au/category/leisure-&-outdoors/golf-balls",
    "https://www.promotionalproductsnow.au/category/leisure-&-outdoors/picnic-rugs",
    "https://www.promotionalproductsnow.au/category/leisure-&-outdoors/sports-balls",
    "https://www.promotionalproductsnow.au/category/leisure-&-outdoors/sports-gear",
    "https://www.promotionalproductsnow.au/category/leisure-&-outdoors/tables",
    "https://www.promotionalproductsnow.au/category/leisure-&-outdoors/umbrellas",
    "https://www.promotionalproductsnow.au/category/office-stationery/business-card-holders",
    "https://www.promotionalproductsnow.au/category/office-stationery/desk-accessories",
    "https://www.promotionalproductsnow.au/category/office-stationery/erasers",
    "https://www.promotionalproductsnow.au/category/office-stationery/notepads",
    "https://www.promotionalproductsnow.au/category/office-stationery/pencil-cases",
    "https://www.promotionalproductsnow.au/category/office-stationery/rulers",
    "https://www.promotionalproductsnow.au/category/office-stationery/sticky-notes",
    "https://www.promotionalproductsnow.au/category/pens-&-pencils/novelty-pens",
    "https://www.promotionalproductsnow.au/category/pens-&-pencils/pen-packaging",
    "https://www.promotionalproductsnow.au/category/pens-&-pencils/pencil-sharpeners",
    "https://www.promotionalproductsnow.au/category/pens-&-pencils/plastic-pens",
    "https://www.promotionalproductsnow.au/category/print/combo-pads",
    "https://www.promotionalproductsnow.au/category/print/stuk-notes",
    "https://www.promotionalproductsnow.au/category/usb-&-tech/cleaning-cloths",
    "https://www.promotionalproductsnow.au/category/usb-&-tech/phone-stands",
    "https://www.promotionalproductsnow.au/category/usb-&-tech/powerbanks",
    "https://www.promotionalproductsnow.au/category/usb-&-tech/tablet-covers",
    "https://www.promotionalproductsnow.au/category/usb-&-tech/travel-adapters",
    "https://www.promotionalproductsnow.au/category/usb-&-tech/usb-hubs"
]

SCOPES = ["https://www.googleapis.com/auth/indexing"]
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"

print(f"Total URLs to bulk submit for indexing: {len(urls_to_submit)}", flush=True)

creds = service_account.Credentials.from_service_account_file("service_account.json", scopes=SCOPES)
creds.refresh(Request())

session = requests.Session()
session.headers.update({"Authorization": f"Bearer {creds.token}"})

success_count = 0
error_count = 0

for idx, url in enumerate(urls_to_submit, 1):
    payload = {"url": url, "type": "URL_UPDATED"}
    try:
        res = session.post(ENDPOINT, json=payload, timeout=10)
        if res.status_code == 200:
            success_count += 1
            print(f"[{idx}/{len(urls_to_submit)}] SUCCESS | {url}", flush=True)
        else:
            error_count += 1
            print(f"[{idx}/{len(urls_to_submit)}] ERROR {res.status_code} | {url} | {res.text}", flush=True)
    except Exception as e:
        error_count += 1
        print(f"[{idx}/{len(urls_to_submit)}] EXCEPTION | {url} | {e}", flush=True)
        
print(f"\n================ BULK SUBMISSION SUMMARY ================", flush=True)
print(f"Total Submitted: {len(urls_to_submit)}", flush=True)
print(f"Successful (200 OK): {success_count}", flush=True)
print(f"Failed: {error_count}", flush=True)
print("========================================================\n", flush=True)
