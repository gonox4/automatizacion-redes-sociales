import os
import requests
import sys
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()

PAGE_ID = os.getenv('FB_PAGE_ID')
TOKEN = os.getenv('FB_PAGE_ACCESS_TOKEN')

print("--- TEst de Publicación en Facebook ---")
print(f"Target Page ID: {PAGE_ID}")

# 1. Verificar identidad del Token
r_me = requests.get(f"https://graph.facebook.com/v21.0/me?access_token={TOKEN}")
me_data = r_me.json()
print(f"Token pertenece a: {me_data.get('name')} (ID: {me_data.get('id')})")

page_token = TOKEN

# Si el token es del usuario "Dorian", intentamos obtener el token de la LÁGINA
if me_data.get('id') != str(PAGE_ID):
    print("⚠️ Detectado Token de Usuario. Intentando obtener Token de Página...")
    url_page_token = f"https://graph.facebook.com/v21.0/{PAGE_ID}?fields=access_token&access_token={TOKEN}"
    r_pt = requests.get(url_page_token)
    if r_pt.status_code == 200:
        pt_data = r_pt.json()
        if 'access_token' in pt_data:
            page_token = pt_data['access_token']
            print("✅ Token de Página obtenido con éxito.")
        else:
             print(f"⚠️ No vino access_token en la respuesta: {pt_data}")
    else:
        print(f"❌ Error obteniendo Token de Página: {r_pt.text}")

print(f"Usando Token: {page_token[:15]}...")

url = f"https://graph.facebook.com/v21.0/{PAGE_ID}/feed"
payload = {
    'message': '🤖 Hello World! Esto es una prueba de automatización desde el script. (Puedes borrar esto).',
    'access_token': page_token
}

try:
    print("Enviando petición...")
    r = requests.post(url, data=payload)
    print(f"Status Code: {r.status_code}")
    
    if r.status_code == 200:
        print("✅ ÉXITO: Publicación realizada.")
        print(f"Post ID: {r.json().get('id')}")
        print("¡Ve a la página y comprueba que ha salido!")
    else:
        print("❌ ERROR:")
        print(r.text)
except Exception as e:
    print(f"Excepción: {e}")
