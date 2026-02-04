import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

load_dotenv()

GOOGLE_SHEETS_KEY_PATH = os.getenv('GOOGLE_SHEETS_KEY_PATH')
GOOGLE_SHEETS_ID = os.getenv('GOOGLE_SHEETS_ID')

def explore():
    try:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SHEETS_KEY_PATH, scope)
        client = gspread.authorize(creds)
        
        sh = client.open_by_key(GOOGLE_SHEETS_ID)
        print(f"Spreadsheet Title: {sh.title}")
        
        print("--- Worksheets ---")
        for ws in sh.worksheets():
            print(f"- {ws.title}")
            print(f"  Headers: {ws.row_values(1)}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    explore()
