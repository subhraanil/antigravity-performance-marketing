import os
import pandas as pd
import matplotlib.pyplot as plt
from googleapiclient.discovery import build
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import argparse
import io
import time

# Scopes required for Sheets, Slides, and Drive
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/presentations',
    'https://www.googleapis.com/auth/drive.file'
]

def get_credentials():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
            
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        elif os.path.exists('service_account.json'):
            creds = service_account.Credentials.from_service_account_file(
                'service_account.json', scopes=SCOPES)
        elif os.path.exists('credentials.json'):
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        else:
            raise FileNotFoundError("Could not find service_account.json or credentials.json")
            
        # Save the credentials for the next run (if not a service account)
        if not isinstance(creds, service_account.Credentials):
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
                
    return creds

def read_sheet_data(sheet_id, range_name):
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id, range=range_name).execute()
    values = result.get('values', [])
    
    if not values:
        print('No data found.')
        return None
    
    df = pd.DataFrame(values[1:], columns=values[0])
    return df

def create_presentation(title):
    creds = get_credentials()
    service = build('slides', 'v1', credentials=creds)
    body = {'title': title}
    presentation = service.presentations().create(body=body).execute()
    print(f"Created presentation with ID: {presentation.get('presentationId')}")
    return presentation.get('presentationId')

def add_slide(presentation_id, layout='TITLE_AND_BODY'):
    creds = get_credentials()
    service = build('slides', 'v1', credentials=creds)
    requests = [
        {
            'createSlide': {
                'slideLayoutReference': {
                    'predefinedLayout': layout
                }
            }
        }
    ]
    body = {'requests': requests}
    response = service.presentations().batchUpdate(presentationId=presentation_id, body=body).execute()
    return response.get('replies')[0].get('createSlide').get('objectId')

def update_text(presentation_id, object_id, text, placeholder_index=0):
    creds = get_credentials()
    service = build('slides', 'v1', credentials=creds)
    
    # First, get the presentation to find the placeholder objectId if needed
    # (Simplified for now: assuming object_id is passed or handled differently)
    
    requests = [
        {
            'insertText': {
                'objectId': object_id,
                'insertionIndex': 0,
                'text': text
            }
        }
    ]
    body = {'requests': requests}
    service.presentations().batchUpdate(presentationId=presentation_id, body=body).execute()

def upload_image_to_drive(file_path):
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)
    
    file_metadata = {'name': os.path.basename(file_path)}
    from googleapiclient.http import MediaFileUpload
    media = MediaFileUpload(file_path, mimetype='image/png')
    
    file = service.files().create(body=file_metadata, media_body=media, fields='id, webContentLink').execute()
    file_id = file.get('id')
    
    # Make the file readable by anyone with the link
    service.permissions().create(
        fileId=file_id,
        body={'type': 'anyone', 'role': 'reader'}
    ).execute()
    
    # Get the webContentLink which is a direct download link
    file_info = service.files().get(fileId=file_id, fields='webContentLink').execute()
    return file_info.get('webContentLink')

def generate_performance_charts(df):
    # Clean data: convert strings to numeric
    for col in df.columns:
        if col != 'Week':
            # Handle currency, percentage, and commas
            df[col] = df[col].astype(str).str.replace(r'[£$€€%,]', '', regex=True).replace('', '0')
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    charts = []
    
    # 1. Traffic Trends
    plt.figure(figsize=(10, 6))
    plt.plot(df['Week'], df['Impressions'], label='Impressions', marker='o')
    plt.plot(df['Week'], df['Clicks'], label='Clicks', marker='s')
    plt.title('Traffic Trends')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig('traffic_trends.png')
    charts.append('traffic_trends.png')
    
    # 2. Conversion Trends
    plt.figure(figsize=(10, 6))
    plt.bar(df['Week'], df['Items Sale'], label='Sales', color='green')
    plt.title('Sales Trends')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig('sales_trends.png')
    charts.append('sales_trends.png')
    
    # 3. ROAS Trend
    plt.figure(figsize=(10, 6))
    plt.plot(df['Week'], df['ROAS'], label='ROAS', marker='^', color='orange')
    plt.axhline(y=df['ROAS'].mean(), color='r', linestyle='--', label='Avg ROAS')
    plt.title('ROAS performance')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig('roas_trend.png')
    charts.append('roas_trend.png')
    
    return charts

def main():
    parser = argparse.ArgumentParser(description='Google Sheets to Slides Report')
    parser.add_argument('--sheet_id', required=True, help='Google Sheet ID')
    parser.add_argument('--title', default='Marketing Performance Report', help='Presentation Title')
    args = parser.parse_args()
    
    print("Reading data from Google Sheet...")
    df = read_sheet_data(args.sheet_id, 'A1:K20')
    if df is None: return
    
    print("Generating charts...")
    chart_files = generate_performance_charts(df)
    
    print("Creating Google Slides presentation...")
    pres_id = create_presentation(args.title)
    
    # Get the slides service to find placeholders
    creds = get_credentials()
    slides_service = build('slides', 'v1', credentials=creds)
    
    # Title Slide (created by default)
    pres = slides_service.presentations().get(presentationId=pres_id).execute()
    title_slide = pres.get('slides')[0]
    title_id = title_slide.get('pageElements')[0].get('objectId')
    update_text(pres_id, title_id, args.title)
    
    # Add Slides for each chart
    for chart_file in chart_files:
        print(f"Uploading {chart_file} to Drive and adding to Slide...")
        try:
            image_url = upload_image_to_drive(chart_file)
            slide_id = add_slide(pres_id, layout='TITLE_ONLY')
            
            # Find the title placeholder on the new slide
            temp_pres = slides_service.presentations().get(presentationId=pres_id).execute()
            new_slide = next(s for s in temp_pres.get('slides') if s['objectId'] == slide_id)
            title_place_id = new_slide.get('pageElements')[0].get('objectId')
            update_text(pres_id, title_place_id, chart_file.replace('.png', '').replace('_', ' ').title())
            
            # Insert Image
            requests = [
                {
                    'createImage': {
                        'url': image_url,
                        'elementProperties': {
                            'pageObjectId': slide_id,
                            'size': {
                                'width': {'magnitude': 600, 'unit': 'PT'},
                                'height': {'magnitude': 400, 'unit': 'PT'}
                            },
                            'transform': {
                                'scaleX': 1, 'scaleY': 1,
                                'translateX': 50, 'translateY': 100,
                                'unit': 'PT'
                            }
                        }
                    }
                }
            ]
            slides_service.presentations().batchUpdate(presentationId=pres_id, body={'requests': requests}).execute()
        except Exception as e:
            print(f"Error adding {chart_file}: {e}")
            
    # Add Table Slide
    print("Adding summary table slide...")
    slide_id = add_slide(pres_id, layout='TITLE_ONLY')
    rows = len(df) + 1
    cols = len(df.columns)
    
    requests = [
        {
            'createTable': {
                'rows': rows,
                'columns': cols,
                'elementProperties': {
                    'pageObjectId': slide_id
                }
            }
        }
    ]
    resp = slides_service.presentations().batchUpdate(presentationId=pres_id, body={'requests': requests}).execute()
    table_id = resp.get('replies')[0].get('createTable').get('objectId')
    
    # Fill Table
    table_requests = []
    # Header
    for j, col_name in enumerate(df.columns):
        table_requests.append({
            'insertText': {
                'objectId': table_id,
                'cellLocation': {'rowIndex': 0, 'columnIndex': j},
                'text': col_name
            }
        })
    # Rows
    for i, row in df.iterrows():
        for j, val in enumerate(row):
            table_requests.append({
                'insertText': {
                    'objectId': table_id,
                    'cellLocation': {'rowIndex': i+1, 'columnIndex': j},
                    'text': str(val)
                }
            })
    
    slides_service.presentations().batchUpdate(presentationId=pres_id, body={'requests': table_requests}).execute()
    
    print(f"\nSuccess! View your report here: https://docs.google.com/presentation/d/{pres_id}/edit")

if __name__ == '__main__':
    main()
