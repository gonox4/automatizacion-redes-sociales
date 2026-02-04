import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('FB_PAGE_ACCESS_TOKEN')

if not TOKEN or "tu_token" in TOKEN:
    print("Error: No parece haber un token válido en .env")
    exit()

print(f"Usando token: {TOKEN[:10]}...")

# 1. Obtener páginas del usuario
url = f"https://graph.facebook.com/v19.0/me/accounts?access_token={TOKEN}"
r = requests.get(url)
data = r.json()

if 'data' in data and len(data['data']) > 0:
    page = data['data'][0] # Tomamos la primera página
    print(f"\n--- INFORMACIÓN ENCONTRADA ---")
    print(f"NOMBRE PÁGINA: {page['name']}")
    print(f"FB_PAGE_ID: {page['id']}")
    print(f"FB_PAGE_ACCESS_TOKEN (Token de Página, mejor que el de usuario):")
    print(page['access_token'])
    
    # Intentar obtener IG ID
    page_id = page['id']
    page_token = page['access_token']
    
    url_ig = f"https://graph.facebook.com/v19.0/{page_id}?fields=instagram_business_account&access_token={page_token}"
    r_ig = requests.get(url_ig)
    data_ig = r_ig.json()
    
    if 'instagram_business_account' in data_ig:
        print(f"IG_ACCOUNT_ID: {data_ig['instagram_business_account']['id']}")
    else:
        print("IG_ACCOUNT_ID: No encontrado (¿Está vinculada la cuenta de IG a esta página?)")
        
else:
    # Quizás el token ya es de página o hay error
    print("No se encontraron páginas vinculadas a este token o error:")
    print(data)
