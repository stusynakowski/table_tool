import gspread
import os
import google.auth
from google.oauth2.service_account import Credentials

# Define the scope
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_gspread_client(credentials_path='service_account.json'):
    """
    Authenticates with Google Sheets.
    Tries to use a service account JSON file first.
    If not found, falls back to Application Default Credentials (ADC).
    """
    # 1. Try Service Account
    if os.path.exists(credentials_path):
        credentials = Credentials.from_service_account_file(
            credentials_path, scopes=SCOPES
        )
        return gspread.authorize(credentials)
    
    # 2. Try Application Default Credentials (ADC)
    try:
        credentials, project = google.auth.default(scopes=SCOPES)
        return gspread.authorize(credentials)
    except Exception as e:
        print(f"ADC Authentication failed: {e}")

    # 3. Fail
    raise FileNotFoundError(
        f"No credentials found. Please either:\n"
        f"1. Place 'service_account.json' in the project root.\n"
        f"2. Run 'gcloud auth application-default login' to use your personal account."
    )

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
