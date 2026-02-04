import os
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import json

load_dotenv()

GOOGLE_SHEETS_KEY_PATH = os.getenv('GOOGLE_SHEETS_KEY_PATH')
GOOGLE_SHEETS_ID = os.getenv('GOOGLE_SHEETS_ID')

def debug_sheet():
    try:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SHEETS_KEY_PATH, scope)
        client = gspread.authorize(creds)
        
        sheet = client.open_by_key(GOOGLE_SHEETS_ID).sheet1
        
        print("--- Headers ---")
        headers = sheet.row_values(1)
        print(headers)
        
        print("\n--- First 5 Rows ---")
        records = sheet.get_all_records()
        for i, r in enumerate(records[:5]):
            print(f"Row {i+2}: {r}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_sheet()
