import os
import requests
import sys
from dotenv import load_dotenv

# Reconfigurar stdout para mostrar caracteres especiales
sys.stdout.reconfigure(encoding='utf-8')

# Cargar .env actual
load_dotenv()

def get_long_lived_user_token(app_id, app_secret, short_token):
    """Intercambia un token de usuario corto por uno de larga duración (60 días)."""
    url = "https://graph.facebook.com/v21.0/oauth/access_token"
    params = {
        'grant_type': 'fb_exchange_token',
        'client_id': app_id,
        'client_secret': app_secret,
        'fb_exchange_token': short_token
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if response.status_code == 200:
        return data.get('access_token')
    else:
        print(f"❌ Error obteniendo Token de Usuario Largo: {data}")
        return None

def get_permanent_page_token(user_access_token, page_id):
    """Obtiene el token de página usando el token de usuario de larga duración.
    El token de página obtenido de esta manera es PERMANENTE."""
    
    url = f"https://graph.facebook.com/v21.0/{page_id}"
    params = {
        'fields': 'access_token',
        'access_token': user_access_token
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if response.status_code == 200:
        return data.get('access_token')
    else:
        print(f"❌ Error obteniendo Token de Página Permanente: {data}")
        return None

def main():
    print("--- GENERADOR DE TOKEN PERMANENTE ---")
    
    app_id = os.getenv('FB_APP_ID')
    app_secret = os.getenv('FB_APP_SECRET')
    short_token = os.getenv('FB_SHORT_TOKEN')
    page_id = os.getenv('FB_PAGE_ID')
    
    # Validaciones
    if not all([app_id, app_secret, short_token, page_id]):
        print("⚠️ FALTAN DATOS EN .ENV")
        print("Asegúrate de haber seguido la GUIA_TOKEN_PERMANENTE.md y tener:")
        print(f" - FB_APP_ID: {'✅' if app_id else '❌'}")
        print(f" - FB_APP_SECRET: {'✅' if app_secret else '❌'}")
        print(f" - FB_SHORT_TOKEN: {'✅' if short_token else '❌'}")
        print(f" - FB_PAGE_ID: {'✅' if page_id else '❌'}")
        return

    print("1. Generando Token de Usuario de Larga Duración...")
    long_user_token = get_long_lived_user_token(app_id, app_secret, short_token)
    
    if long_user_token:
        print("✅ Token de Usuario extendido con éxito.")
        
        print(f"2. Obteniendo Token Permanente para la Página ID {page_id}...")
        permanent_page_token = get_permanent_page_token(long_user_token, page_id)
        
        if permanent_page_token:
            print("\n" + "="*50)
            print("🚀 ¡TOKEN PERMANENTE GENERADO!")
            print("="*50)
            print(permanent_page_token)
            print("="*50 + "\n")
            
            print("👉 Copia este token y reemplaza el valor de FB_PAGE_ACCESS_TOKEN en tu archivo .env")
        else:
            print("❌ Falló el paso 2.")
    else:
        print("❌ Falló el paso 1.")

if __name__ == "__main__":
    main()
