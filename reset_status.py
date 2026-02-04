import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from dotenv import load_dotenv

load_dotenv()

json_path = os.getenv('GOOGLE_SHEETS_KEY_PATH', 'credentials.json')
sheet_id = os.getenv('GOOGLE_SHEETS_ID')

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
client = gspread.authorize(creds)

sheet = client.open_by_key(sheet_id).sheet1

# Encontrar columna estado
header = sheet.row_values(1)
col_idx = header.index("ESTADO") + 1

# Leer todos
vals = sheet.col_values(col_idx)

# Resetear cualquiera que sea ERROR_FB a PENDIENTE
for i, val in enumerate(vals):
    if "ERROR" in val or "PUBLICADO" in val: # Reset general para pruebas
        # i es 0-based, row es i+1
        print(f"Reseteando fila {i+1} de '{val}' a 'PENDIENTE'")
        sheet.update_cell(i+1, col_idx, 'PENDIENTE')

print("Reset completado.")
