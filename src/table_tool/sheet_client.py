import gspread
import os
from google.oauth2.service_account import Credentials

# Define the scope
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_gspread_client(credentials_path='service_account.json'):
    """
    Authenticates with Google Sheets using a service account JSON file.
    """
    if not os.path.exists(credentials_path):
        raise FileNotFoundError(f"Credentials file not found at {credentials_path}. Please follow the README to set up credentials.")
    
    credentials = Credentials.from_service_account_file(
        credentials_path, scopes=SCOPES
    )
    client = gspread.authorize(credentials)
    return client

def open_worksheet(sheet_name, worksheet_name=None):
    """
    Opens a specific worksheet in a Google Sheet.
    If worksheet_name is None, opens the first worksheet.
    """
    client = get_gspread_client()
    try:
        sheet = client.open(sheet_name)
        if worksheet_name:
            worksheet = sheet.worksheet(worksheet_name)
        else:
            worksheet = sheet.sheet1
        return worksheet
    except gspread.SpreadsheetNotFound:
        print(f"Error: Spreadsheet '{sheet_name}' not found. Make sure you've shared it with the service account email.")
        raise
    except gspread.WorksheetNotFound:
        print(f"Error: Worksheet '{worksheet_name}' not found in spreadsheet '{sheet_name}'.")
        raise
