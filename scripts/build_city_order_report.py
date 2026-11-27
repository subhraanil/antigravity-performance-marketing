import pandas as pd
import re
import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Load orders export
csv_path = r'c:\Users\test\Videos\Office\data\Pet Mode\orders_export.csv'
df = pd.read_csv(csv_path, low_memory=False)

# Shopify order rows: first row of each order contains order header data
orders = df.groupby('Name', as_index=False).first()

# Map Postcode area to standard UK region and county/area
postcode_region_map = {
    'AB': ('Aberdeen & North East Scotland', 'Scotland'),
    'B': ('Birmingham & West Midlands', 'West Midlands'),
    'BA': ('Bath & Somerset', 'South West'),
    'BB': ('Blackburn & Lancashire', 'North West'),
    'BD': ('Bradford & West Yorkshire', 'Yorkshire and the Humber'),
    'BH': ('Bournemouth & Dorset', 'South West'),
    'BL': ('Bolton & Greater Manchester', 'North West'),
    'BN': ('Brighton & East Sussex', 'South East'),
    'BR': ('Bromley & Greater London', 'Greater London'),
    'BS': ('Bristol & North Somerset', 'South West'),
    'BT': ('Northern Ireland', 'Northern Ireland'),
    'CA': ('Cumbria', 'North West'),
    'CB': ('Cambridge & Cambridgeshire', 'East of England'),
    'CF': ('Cardiff & South Wales', 'Wales'),
    'CH': ('Chester & Cheshire', 'North West'),
    'CM': ('Chelmsford & Essex', 'East of England'),
    'CO': ('Colchester & Essex', 'East of England'),
    'CR': ('Croydon & Greater London', 'Greater London'),
    'CT': ('Canterbury & Kent', 'South East'),
    'CV': ('Coventry & Warwickshire', 'West Midlands'),
    'CW': ('Crewe & Cheshire', 'North West'),
    'DA': ('Dartford & Greater London/Kent', 'Greater London'),
    'DD': ('Dundee & Angus/Fife', 'Scotland'),
    'DE': ('Derby & Derbyshire', 'East Midlands'),
    'DG': ('Dumfries and Galloway', 'Scotland'),
    'DH': ('Durham & County Durham', 'North East'),
    'DL': ('Darlington & North Yorkshire', 'North East'),
    'DN': ('Doncaster & North Lincolnshire', 'Yorkshire and the Humber'),
    'DT': ('Dorchester & Dorset', 'South West'),
    'DY': ('Dudley & West Midlands', 'West Midlands'),
    'E': ('East London', 'Greater London'),
    'EC': ('East Central London', 'Greater London'),
    'EH': ('Edinburgh & Lothians', 'Scotland'),
    'EN': ('Enfield & Greater London', 'Greater London'),
    'EX': ('Exeter & Devon', 'South West'),
    'FK': ('Falkirk & Stirling', 'Scotland'),
    'FY': ('Blackpool & Lancashire', 'North West'),
    'G': ('Glasgow & Dunbartonshire', 'Scotland'),
    'GL': ('Gloucester & Gloucestershire', 'South West'),
    'GU': ('Guildford & Surrey', 'South East'),
    'HA': ('Harrow & Greater London', 'Greater London'),
    'HD': ('Huddersfield & West Yorkshire', 'Yorkshire and the Humber'),
    'HG': ('Harrogate & North Yorkshire', 'Yorkshire and the Humber'),
    'HP': ('Hemel Hempstead & Buckinghamshire', 'South East'),
    'HR': ('Hereford & Herefordshire', 'West Midlands'),
    'HS': ('Outer Hebrides', 'Scotland'),
    'HU': ('Hull & East Yorkshire', 'Yorkshire and the Humber'),
    'HX': ('Halifax & West Yorkshire', 'Yorkshire and the Humber'),
    'IG': ('Ilford & Greater London', 'Greater London'),
    'IP': ('Ipswich & Suffolk', 'East of England'),
    'IV': ('Inverness & Highlands', 'Scotland'),
    'KA': ('Kilmarnock & Ayrshire', 'Scotland'),
    'KT': ('Kingston upon Thames & Greater London', 'Greater London'),
    'KW': ('Kirkwall & Highlands', 'Scotland'),
    'KY': ('Kirkcaldy & Fife', 'Scotland'),
    'L': ('Liverpool & Merseyside', 'North West'),
    'LA': ('Lancaster & Cumbria/Lancashire', 'North West'),
    'LD': ('Llandrindod Wells & Powys', 'Wales'),
    'LE': ('Leicester & Leicestershire', 'East Midlands'),
    'LL': ('Llandudno & North Wales', 'Wales'),
    'LN': ('Lincoln & Lincolnshire', 'East Midlands'),
    'LS': ('Leeds & West Yorkshire', 'Yorkshire and the Humber'),
    'LU': ('Luton & Bedfordshire', 'East of England'),
    'M': ('Manchester & Greater Manchester', 'North West'),
    'ME': ('Medway & Kent', 'South East'),
    'MK': ('Milton Keynes & Buckinghamshire', 'South East'),
    'ML': ('Motherwell & Lanarkshire', 'Scotland'),
    'N': ('North London', 'Greater London'),
    'NE': ('Newcastle upon Tyne & Tyne and Wear', 'North East'),
    'NG': ('Nottingham & Nottinghamshire', 'East Midlands'),
    'NN': ('Northampton & Northamptonshire', 'East Midlands'),
    'NP': ('Newport & South Wales', 'Wales'),
    'NR': ('Norwich & Norfolk', 'East of England'),
    'NW': ('North West London', 'Greater London'),
    'OL': ('Oldham & Greater Manchester', 'North West'),
    'OX': ('Oxford & Oxfordshire', 'South East'),
    'PA': ('Paisley & Renfrewshire/Argyll', 'Scotland'),
    'PE': ('Peterborough & Cambridgeshire/Norfolk', 'East of England'),
    'PH': ('Perth & Highlands', 'Scotland'),
    'PL': ('Plymouth & Devon/Cornwall', 'South West'),
    'PO': ('Portsmouth & Hampshire/West Sussex', 'South East'),
    'PR': ('Preston & Lancashire', 'North West'),
    'RG': ('Reading & Berkshire', 'South East'),
    'RH': ('Redhill & Surrey/West Sussex', 'South East'),
    'RM': ('Romford & Greater London', 'Greater London'),
    'S': ('Sheffield & South Yorkshire', 'Yorkshire and the Humber'),
    'SA': ('Swansea & South Wales', 'Wales'),
    'SE': ('South East London', 'Greater London'),
    'SG': ('Stevenage & Hertfordshire', 'East of England'),
    'SK': ('Stockport & Cheshire/Greater Manchester', 'North West'),
    'SL': ('Slough & Berkshire/Buckinghamshire', 'South East'),
    'SM': ('Sutton & Greater London', 'Greater London'),
    'SN': ('Swindon & Wiltshire', 'South West'),
    'SO': ('Southampton & Hampshire', 'South East'),
    'SP': ('Salisbury & Wiltshire', 'South West'),
    'SR': ('Sunderland & Tyne and Wear', 'North East'),
    'SS': ('Southend-on-Sea & Essex', 'East of England'),
    'ST': ('Stoke-on-Trent & Staffordshire', 'West Midlands'),
    'SW': ('South West London', 'Greater London'),
    'SY': ('Shrewsbury & Shropshire/Mid Wales', 'West Midlands'),
    'TA': ('Taunton & Somerset', 'South West'),
    'TD': ('Galashiels & Scottish Borders', 'Scotland'),
    'TF': ('Telford & Shropshire', 'West Midlands'),
    'TN': ('Tunbridge Wells & Kent/East Sussex', 'South East'),
    'TQ': ('Torquay & Devon', 'South West'),
    'TR': ('Truro & Cornwall', 'South West'),
    'TS': ('Cleveland & Teesside', 'North East'),
    'TW': ('Twickenham & Greater London', 'Greater London'),
    'UB': ('Uxbridge & Greater London', 'Greater London'),
    'W': ('West London', 'Greater London'),
    'WA': ('Warrington & Cheshire/Merseyside', 'North West'),
    'WC': ('West Central London', 'Greater London'),
    'WD': ('Watford & Hertfordshire', 'East of England'),
    'WF': ('Wakefield & West Yorkshire', 'Yorkshire and the Humber'),
    'WN': ('Wigan & Greater Manchester', 'North West'),
    'WR': ('Worcester & Worcestershire', 'West Midlands'),
    'WS': ('Walsall & West Midlands', 'West Midlands'),
    'WV': ('Wolverhampton & West Midlands', 'West Midlands'),
    'YO': ('York & North Yorkshire', 'Yorkshire and the Humber'),
    'ZE': ('Shetland', 'Scotland')
}

records = []
for idx, r in orders.iterrows():
    name = str(r['Name']).strip()
    raw_city = str(r['Shipping City']).strip() if pd.notna(r['Shipping City']) else ''
    zip_code = str(r['Shipping Zip']).strip().upper() if pd.notna(r['Shipping Zip']) else ''
    country = str(r['Shipping Country']).strip().upper() if pd.notna(r['Shipping Country']) else ''
    province = str(r['Shipping Province Name']).strip() if pd.notna(r['Shipping Province Name']) else ''
    total = float(r['Total']) if pd.notna(r['Total']) else 0.0
    status = str(r['Financial Status']).strip() if pd.notna(r['Financial Status']) else ''
    created_at = str(r['Created at']).strip() if pd.notna(r['Created at']) else ''
    
    # Extract postcode area & outcode
    if country == 'GB':
        m_area = re.match(r'^([A-Z]{1,2})', zip_code)
        pc_area = m_area.group(1) if m_area else 'Other'
        outcode = zip_code.split(' ')[0] if ' ' in zip_code else zip_code
        area_info = postcode_region_map.get(pc_area, ('Other UK', 'Other UK'))
        county_desc = area_info[0]
        region = area_info[1]
    elif country == 'PL':
        pc_area = 'PL'
        outcode = zip_code
        county_desc = 'West Pomerania (Poland)'
        region = 'International (Poland)'
    elif country == 'US':
        pc_area = 'NJ'
        outcode = zip_code
        county_desc = 'Ocean County, New Jersey (USA)'
        region = 'International (USA)'
    else:
        pc_area = 'Other'
        outcode = zip_code
        county_desc = 'Other'
        region = 'Other'
        
    # Standardize city display
    c_lower = raw_city.lower()
    if country == 'PL':
        clean_city = 'Świnoujście (Poland)'
        metro = 'International'
    elif country == 'US':
        clean_city = 'Lacey Township, NJ (USA)'
        metro = 'International'
    else:
        # UK clean city
        if c_lower in ['london', 'greater london']:
            clean_city = 'London'
            metro = 'Greater London'
        elif 'hackney' in c_lower:
            clean_city = 'London (Hackney)'
            metro = 'Greater London'
        elif 'islington' in c_lower:
            clean_city = 'London (Islington)'
            metro = 'Greater London'
        elif 'leytonstone' in c_lower:
            clean_city = 'London (Leytonstone)'
            metro = 'Greater London'
        elif 'cheam' in c_lower:
            clean_city = 'Cheam (Sutton)'
            metro = 'Greater London'
        elif 'purley' in c_lower:
            clean_city = 'Purley (Croydon)'
            metro = 'Greater London'
        elif 'beckenham' in c_lower:
            clean_city = 'Beckenham (Bromley)'
            metro = 'Greater London'
        elif 'pinner' in c_lower:
            clean_city = 'Pinner (Harrow)'
            metro = 'Greater London'
        elif 'teddington' in c_lower:
            clean_city = 'Teddington (Richmond)'
            metro = 'Greater London'
        elif 'uxbridge' in c_lower:
            clean_city = 'Uxbridge (Hillingdon)'
            metro = 'Greater London'
        elif 'worcester park' in c_lower:
            clean_city = 'Worcester Park (Sutton/Surrey)'
            metro = 'Greater London'
        elif 'bognor regis' in c_lower:
            clean_city = 'Bognor Regis'
            metro = 'West Sussex Coastal'
        elif 'chorleywood' in c_lower:
            clean_city = 'Chorleywood'
            metro = 'Hertfordshire'
        elif 'edenbridge' in c_lower:
            clean_city = 'Edenbridge'
            metro = 'Sevenoaks / Kent'
        elif 'hatfield' in c_lower:
            clean_city = 'Hatfield (Doncaster)'
            metro = 'Greater Doncaster'
        elif 'mirfield' in c_lower:
            clean_city = 'Mirfield'
            metro = 'West Yorkshire'
        elif 'newcastle upon tyne' in c_lower or c_lower == 'newcastle':
            clean_city = 'Newcastle upon Tyne'
            metro = 'Tyne and Wear'
        elif 'old kilpatrick' in c_lower:
            clean_city = 'Clydebank / Old Kilpatrick'
            metro = 'Greater Glasgow'
        elif 'penylan' in c_lower:
            clean_city = 'Cardiff (Penylan)'
            metro = 'Cardiff & South Wales'
        elif 'pollokshields' in c_lower:
            clean_city = 'Glasgow (Pollokshields)'
            metro = 'Greater Glasgow'
        elif 'stone' in c_lower:
            clean_city = 'Stone'
            metro = 'Staffordshire'
        elif 'stratford-upon-avon' in c_lower:
            clean_city = 'Stratford-upon-Avon'
            metro = 'Warwickshire'
        elif 'winsham' in c_lower:
            clean_city = 'Winsham'
            metro = 'Somerset'
        elif 'wokingham' in c_lower:
            clean_city = 'Wokingham'
            metro = 'Berkshire'
        elif 'yelverton' in c_lower:
            clean_city = 'Yelverton'
            metro = 'Plymouth & Dartmoor'
        elif 'essex' in c_lower:
            clean_city = 'Epping (Essex)'
            metro = 'Essex'
        elif 'warmley' in c_lower:
            clean_city = 'Warmley (Bristol)'
            metro = 'Greater Bristol'
        elif 'cheddar' in c_lower:
            clean_city = 'Cheddar'
            metro = 'Somerset / Mendip'
        elif 'sutton coldfield' in c_lower:
            clean_city = 'Sutton Coldfield'
            metro = 'Greater Birmingham'
        elif 'tamworth' in c_lower:
            clean_city = 'Tamworth'
            metro = 'Greater Birmingham'
        elif 'walsall' in c_lower:
            clean_city = 'Walsall'
            metro = 'Greater Birmingham / Black Country'
        elif 'bristol' in c_lower:
            clean_city = 'Bristol'
            metro = 'Greater Bristol'
        elif 'glasgow' in c_lower:
            clean_city = 'Glasgow'
            metro = 'Greater Glasgow'
        elif 'edinburgh' in c_lower:
            clean_city = 'Edinburgh'
            metro = 'Edinburgh & Lothians'
        elif 'cardiff' in c_lower:
            clean_city = 'Cardiff'
            metro = 'Cardiff & South Wales'
        elif 'leeds' in c_lower:
            clean_city = 'Leeds'
            metro = 'West Yorkshire'
        elif 'manchester' in c_lower:
            clean_city = 'Manchester'
            metro = 'Greater Manchester'
        else:
            clean_city = raw_city.title()
            metro = area_info[0]

    records.append({
        'Order_ID': name,
        'Created_At': created_at,
        'Financial_Status': status,
        'Raw_City': raw_city,
        'Clean_City': clean_city,
        'Metro_Area': metro,
        'County_Desc': county_desc,
        'Region': region,
        'Country': country,
        'Postcode': zip_code,
        'Outcode': outcode,
        'Postcode_Area': pc_area,
        'Order_Total': total
    })

order_df = pd.DataFrame(records)
print(f"Total processed records: {len(order_df)}")
print(f"Total Revenue: £{order_df['Order_Total'].sum():.2f}")
print("\nTop 15 Cleaned Cities by Order Count:")
city_summary = order_df.groupby('Clean_City').agg(
    orders=('Order_ID', 'count'),
    revenue=('Order_Total', 'sum'),
    aov=('Order_Total', 'mean')
).sort_values(by=['orders', 'revenue'], ascending=[False, False])
print(city_summary.head(15))
