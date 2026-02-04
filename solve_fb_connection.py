import os
import requests
import sys
from dotenv import load_dotenv

# Force UTF-8 for Windows consoles
sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

TOKEN = os.getenv('FB_PAGE_ACCESS_TOKEN')
TARGET_PAGE_NAME = "cueva del eco" 

print(f"--- ANALIZANDO CONEXIÓN A FACEBOOK ---")
print(f"Token (inicio): {TOKEN[:15]}...")

if not TOKEN:
    print("ERROR: No hay token en .env")
    exit()

# 1. Verificar Usuario y Permisos
url_perms = f"https://graph.facebook.com/v21.0/me/permissions?access_token={TOKEN}"

try:
    r_perms = requests.get(url_perms)
    perms_data = r_perms.json()
    if 'data' in perms_data:
        print("\nPERMISOS ACTIVOS:")
        for p in perms_data['data']:
            if p['status'] == 'granted':
                print(f" + {p['permission']}")
            else:
                print(f" - {p['permission']} ({p['status']})")
    else:
        print(f"No se pudieron leer permisos: {perms_data}")
except Exception as e:
    print(f"Error comprobando permisos: {e}")


# 2. Verificar Usuario
url_me = f"https://graph.facebook.com/v21.0/me?access_token={TOKEN}"
r_me = requests.get(url_me)
if r_me.status_code == 200:
    user_data = r_me.json()
    print(f"\nUsuario: {user_data.get('name')} (ID: {user_data.get('id')})")
else:
    print(f"Error autenticando token: {r_me.text}")
    exit()

# 3. Buscar Páginas
print("\n--- BUSCANDO PÁGINAS ---")
url_accounts = f"https://graph.facebook.com/v21.0/me/accounts?access_token={TOKEN}"
r_accounts = requests.get(url_accounts)
pages_data = r_accounts.json()

found_pages = pages_data.get('data', [])

if not found_pages:
    print("[X] NO SE ENCONTRARON PÁGINAS.")
    print("Raw response:", pages_data)
else:
    print(f"[OK] Se encontraron {len(found_pages)} páginas:")
    for p in found_pages:
        name = p.get('name')
        pid = p.get('id')
        print(f" - NOMBRE: '{name}' | ID: {pid}")
        
        # Check IG
        url_ig = f"https://graph.facebook.com/v21.0/{pid}?fields=instagram_business_account&access_token={TOKEN}"
        r_ig = requests.get(url_ig)
        ig_data = r_ig.json()
        ig_id = ig_data.get('instagram_business_account', {}).get('id')
        
        if ig_id:
            print(f"   -> IG ACCOUNT ID: {ig_id}")
        else:
            print(f"   -> IG: No vinculada a esta página.")
