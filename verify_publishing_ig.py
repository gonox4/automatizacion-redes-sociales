import os
import requests
import sys
import time
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()

IG_ID = os.getenv('IG_ACCOUNT_ID')
TOKEN = os.getenv('FB_PAGE_ACCESS_TOKEN')

print("--- Test de Publicación en Instagram ---")
print(f"Target IG ID: {IG_ID}")

# Imagen de prueba (Debe ser una URL pública real para que IG la pueda descargar)
# Usaremos una imagen de Wikimedia Commons que es estable y directa .png
IMAGE_URL = "https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png"
CAPTION = "🤖 Hello World Instagram! Prueba de automatización. #bot #test"

# 1. Crear Contenedor
print("1. Creando contenedor de medios...")
url_container = f"https://graph.facebook.com/v21.0/{IG_ID}/media"
payload_container = {
    'image_url': IMAGE_URL,
    'caption': CAPTION,
    'access_token': TOKEN
}

try:
    r_cont = requests.post(url_container, data=payload_container)
    print(f"Status Crear: {r_cont.status_code}")
    
    if r_cont.status_code == 200:
        container_id = r_cont.json().get('id')
        print(f"✅ Contenedor Creado ID: {container_id}")
        
        print("⏳ Esperando 10 segundos para procesamiento...")
        time.sleep(10)
        
        # 2. Publicar
        print("2. Publicando contenedor...")
        url_publish = f"https://graph.facebook.com/v21.0/{IG_ID}/media_publish"
        payload_publish = {
            'creation_id': container_id,
            'access_token': TOKEN
        }
        
        r_pub = requests.post(url_publish, data=payload_publish)
        print(f"Status Publicar: {r_pub.status_code}")
        
        if r_pub.status_code == 200:
            print("✅ ÉXITO: Publicación realizada en Instagram.")
            print(f"IG Media ID: {r_pub.json().get('id')}")
            print("¡Comprueba tu Instagram Business!")
        else:
            print("❌ Error Publicando:")
            print(r_pub.text)
            
    else:
        print("❌ Error Creando Contenedor:")
        print(r_cont.text)

except Exception as e:
    print(f"Excepción: {e}")
