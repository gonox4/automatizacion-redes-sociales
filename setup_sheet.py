import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from dotenv import load_dotenv

load_dotenv()

print("Conectando a Google Sheets para escribir datos...")

json_path = os.getenv('GOOGLE_SHEETS_KEY_PATH', 'credentials.json')
sheet_id = os.getenv('GOOGLE_SHEETS_ID')

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
client = gspread.authorize(creds)

try:
    sheet = client.open_by_key(sheet_id).sheet1
    
    # 1. Limpiar hoja (opcional, pero mejor para asegurar estado limpio)
    sheet.clear()
    
    # 2. Escribir Cabeceras
    headers = ['ID', 'PROMPT_IMAGEN', 'TEXTO_POST', 'ESTADO']
    sheet.append_row(headers)
    
    # 3. Escribir Fila de Prueba
    test_row = [1, 'Un paisaje futurista cyberpunk con luces de neón rosa y azul', 'Mi primer post automático con IA. #Futuro #IA', 'PENDIENTE']
    sheet.append_row(test_row)
    
    print("[OK] Hecho! He escrito las cabeceras y una fila de prueba en tu hoja.")

except Exception as e:
    print(f"[ERROR] Error escribiendo en la hoja: {e}")
