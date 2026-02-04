import os
import sys
import google.generativeai as genai
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

# Cargar .env
load_dotenv()
print("--- INICIANDO DIAGNOSTICO ---\n")

# 1. TEST GEMINI
print("1. PROBANDO GEMINI (Inteligencia Artificial)...")
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("[X] ERROR: No se encontro GEMINI_API_KEY en .env")
else:
    try:
        genai.configure(api_key=api_key)
        # Usamos gemini-1.5-flash que es mas actual
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content("Di 'Hola Mundo'")
        print(f"[OK] EXITO: Gemini respondio: {response.text}")
    except Exception as e:
        print(f"[X] ERROR GEMINI: {e}")

print("\n" + "-"*30 + "\n")

# 2. TEST GOOGLE SHEETS
print("2. PROBANDO GOOGLE SHEETS...")
json_path = os.getenv('GOOGLE_SHEETS_KEY_PATH', 'credentials.json')
sheet_id = os.getenv('GOOGLE_SHEETS_ID')

if not os.path.exists(json_path):
    print(f"[X] ERROR: No encuentro el archivo '{json_path}'. Asegurate de haberlo descargado y renombrado.")
elif not sheet_id or "tu_id" in sheet_id:
    print("[X] ERROR: El GOOGLE_SHEETS_ID en .env parece ser el de ejemplo.")
else:
    try:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(sheet_id)
        print(f"[OK] EXITO: Hoja conectada. Titulo: '{spreadsheet.title}'")
        
        # Verificar columnas
        worksheet = spreadsheet.sheet1
        headers = worksheet.row_values(1)
        print(f"   Columnas encontradas: {headers}")
        
        required = ['ID', 'PROMPT_IMAGEN', 'TEXTO_POST', 'ESTADO']
        missing = [h for h in required if h not in headers]
        if missing:
             print(f"[!] ADVERTENCIA: Faltan columnas requeridas: {missing}")
        else:
             print("[OK] Todas las columnas estan correctas.")
             
    except Exception as e:
        print(f"[X] ERROR SHEETS: {e}")
        print("   (Verifica que hayas compartido la hoja con el email del JSON)")

print("\n--- FIN DEL DIAGNOSTICO ---")
