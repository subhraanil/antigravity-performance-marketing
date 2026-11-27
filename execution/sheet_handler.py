import os
import pickle
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Scopes
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

def get_creds():
    creds = None
    if os.path.exists('token.json'):
        with open('token.json', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if os.path.exists('credentials.json'):
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            else:
                print("credentials.json not found.")
                return None
        with open('token.json', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def create_sheet(title, data):
    """
    Creates a Google Sheet and populates it with data.
    data format: list of lists (rows)
    """
    creds = get_creds()
    if not creds:
        return None

    service = build('sheets', 'v4', credentials=creds)

    # Create Sheet
    spreadsheet_body = {
        'properties': {
            'title': title
        }
    }
    spreadsheet = service.spreadsheets().create(body=spreadsheet_body, fields='spreadsheetId,spreadsheetUrl').execute()
    spreadsheet_id = spreadsheet.get('spreadsheetId')
    spreadsheet_url = spreadsheet.get('spreadsheetUrl')

    # Prepare Data
    value_range_body = {
        'values': data
    }

    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range='A1',
        valueInputOption='RAW',
        body=value_range_body
    ).execute()
    
    print(f"Sheet created: {spreadsheet_url}")
    print(f"Sheet created: {spreadsheet_url}")
    return spreadsheet_id, spreadsheet_url

def append_data(spreadsheet_id, values, range_name='A1'):
    """
    Appends data to an existing Google Sheet.
    values: list of lists (rows)
    """
    creds = get_creds()
    if not creds:
        return None

    service = build('sheets', 'v4', credentials=creds)

    value_range_body = {
        'values': values
    }

    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption='USER_ENTERED',
        insertDataOption='INSERT_ROWS',
        body=value_range_body
    ).execute()

    print(f"{result.get('updates').get('updatedCells')} cells appended.")
    return result

def move_to_folder(file_id, folder_id):
    """
    Moves a file to a specific drive folder.
    """
    creds = get_creds()
    if not creds:
        return
    
    service = build('drive', 'v3', credentials=creds)
    
    # Retrieve the existing parents to remove
    file = service.files().get(fileId=file_id, fields='parents').execute()
    previous_parents = ",".join(file.get('parents'))
    
    # Move the file to the new folder
    service.files().update(fileId=file_id,
                           addParents=folder_id,
                           removeParents=previous_parents,
                           fields='id, parents').execute()
    print(f"File {file_id} moved to folder {folder_id}")

if __name__ == "__main__":
    print("Sheet Handler execution module loaded.")
