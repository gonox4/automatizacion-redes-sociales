import os
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

load_dotenv()

GOOGLE_SHEETS_KEY_PATH = os.getenv('GOOGLE_SHEETS_KEY_PATH')
GOOGLE_SHEETS_ID = os.getenv('GOOGLE_SHEETS_ID')

def set_time_column():
    try:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SHEETS_KEY_PATH, scope)
        client = gspread.authorize(creds)
        
        sheet = client.open_by_key(GOOGLE_SHEETS_ID).sheet1
        
        headers = sheet.row_values(1)
        
        if "HORA_PUBLICACION" not in headers:
            print("Adding 'HORA_PUBLICACION' column...")
            # Nueva columna en la primera fila vacía a la derecha
            col_index = len(headers) + 1
            sheet.update_cell(1, col_index, "HORA_PUBLICACION")
            time_col_idx = col_index
        else:
            print("'HORA_PUBLICACION' column already exists.")
            time_col_idx = headers.index("HORA_PUBLICACION") + 1
            
        # Get all records to know how many rows to update
        records = sheet.get_all_records()
        num_rows = len(records)
        
        if num_rows == 0:
            print("No data rows found.")
            return

        print(f"Updating {num_rows} rows with '10:00 AM'...")
        
        # Batch update is better, but cell_list with individual updates is safer for simple scripts or use update_cells
        # Let's simple iterate for now or use range update if possible.
        # Construct range string e.g. E2:E100
        
        # Taking a safer approach: update row by row or small batches if API allows easily.
        # gspread has update(range_name, values)
        
        # Column letter calculation is annoying, let's just iterate for safety and avoiding letter math bugs
        # Or better, construct a list of cell objects to update in batch.
        
        cell_list = []
        for i in range(num_rows):
            # Row index is i + 2 (1 for header, 1 for 0-index offset)
            row_idx = i + 2
            cell_list.append(gspread.Cell(row_idx, time_col_idx, "10:00 AM"))
            
        sheet.update_cells(cell_list)

        print("Update complete.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    set_time_column()
