import os
import sys
import time
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ClientError
from PIL import Image, ImageDraw, ImageFont

# Cargar variables de entorno
load_dotenv()

# Configuración
FB_PAGE_ACCESS_TOKEN = os.getenv('FB_PAGE_ACCESS_TOKEN')
FB_PAGE_ID = os.getenv('FB_PAGE_ID')
IG_ACCOUNT_ID = os.getenv('IG_ACCOUNT_ID')
GOOGLE_SHEETS_KEY_PATH = os.getenv('GOOGLE_SHEETS_KEY_PATH')
GOOGLE_SHEETS_ID = os.getenv('GOOGLE_SHEETS_ID')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Validar configuración básica
if not all([FB_PAGE_ACCESS_TOKEN, FB_PAGE_ID, IG_ACCOUNT_ID, GOOGLE_SHEETS_KEY_PATH, GOOGLE_SHEETS_ID, GEMINI_API_KEY]):
    print("Error: Faltan variables de entorno. Revisa tu archivo .env")
    sys.exit(1)

# Configurar Gemini
client = genai.Client(api_key=GEMINI_API_KEY)

def get_google_sheets_client():
    """Conecta a Google Sheets usando Service Account."""
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SHEETS_KEY_PATH, scope)
    client = gspread.authorize(creds)
    return client

def generate_image(prompt, output_path="static/generated/last_gen.png"):
    """Genera una imagen usando Gemini (Imagen 4) y la guarda."""
    print(f"Generando imagen para: {prompt}...")
    try:
        # Intento 1: Usar el modelo de Imagen 4 (si está disponible y facturado)
        try:
            response = client.models.generate_images(
                model='imagen-4.0-generate-001',
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                )
            )
            if response.generated_images:
                response.generated_images[0].image.save(output_path)
                print(" [OK] Imagen generada con Imagen 4.")
                return output_path
        except ClientError as e:
            if "billed users" in str(e) or "400" in str(e):
                print(" [INFO] La API de Imagen requiere facturación. Usando fallback.")
            else:
                print(f" [INFO] Error en API Imagen ({e}). Probando fallback...")
        except Exception as e_img:
            print(f" [INFO] No se pudo usar Imagen directo ({e_img}). Probando alternativa...")

        # Fallback
        print(" [AVISO] Usando imagen generada por PIL (Fallback/Simulación).")
        
        img = Image.new('RGB', (1024, 1024), color = (73, 109, 137))
        d = ImageDraw.Draw(img)
        
        # Intentar cargar fuente
        try:
            font_title = ImageFont.truetype("arial.ttf", 60)
            font_text = ImageFont.truetype("arial.ttf", 40)
        except IOError:
            font_title = ImageFont.load_default()
            font_text = ImageFont.load_default()

        # Dibujar texto centrado aproximado
        d.text((50, 400), "Imagen Generada Automaticamente", fill=(255, 255, 255), font=font_title)
        d.text((50, 500), prompt[:60] + "...", fill=(220, 220, 220), font=font_text)
             
        img.save(output_path)
        return output_path

    except Exception as e:
        print(f"Error generando imagen: {e}")
        return None

def publish_facebook_photo(image_path, caption):
    """Publica una foto en la página de Facebook."""
    url = f"https://graph.facebook.com/v21.0/me/photos?access_token={FB_PAGE_ACCESS_TOKEN}"
    payload = {
        'message': caption
    }
    files = {
        'file': open(image_path, 'rb')
    }
    response = requests.post(url, data=payload, files=files)
    if response.status_code == 200:
        return response.json().get('id')
    else:
        print(f"Error Facebook: {response.text}")
        return None

def get_fb_photo_url(photo_id):
    """Obtiene la URL pública de una foto subida a Facebook."""
    url = f"https://graph.facebook.com/v21.0/{photo_id}?fields=images&access_token={FB_PAGE_ACCESS_TOKEN}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # 'images' es una lista, la primera suele ser la original/más grande
        return data['images'][0]['source']
    return None

def publish_instagram_photo(image_url, caption):
    """Publica una foto en Instagram usando Container + Publish con URL."""
    # 1. Crear contenedor de medios
    url_container = f"https://graph.facebook.com/v21.0/{IG_ACCOUNT_ID}/media"
    payload_container = {
        'image_url': image_url,
        'caption': caption,
        'access_token': FB_PAGE_ACCESS_TOKEN 
    }
    r_cont = requests.post(url_container, data=payload_container)
    if r_cont.status_code != 200:
        print(f"Error IG Container: {r_cont.text}")
        return None
    
    creation_id = r_cont.json().get('id')
    
    # Esperar un momento para que se procese
    time.sleep(5) 
    
    # 2. Publicar contenedor
    url_publish = f"https://graph.facebook.com/v21.0/{IG_ACCOUNT_ID}/media_publish"
    payload_publish = {
        'creation_id': creation_id,
        'access_token': FB_PAGE_ACCESS_TOKEN
    }
    r_pub = requests.post(url_publish, data=payload_publish)
    if r_pub.status_code == 200:
        return r_pub.json().get('id')
    else:
        print(f"Error IG Publish: {r_pub.text}")
        return None

def process_row(row, sheet):
    """Procesa una fila individual."""
    row_num = row['ROW_INDEX']
    row_id = row['ID']
    prompt = row['PROMPT_IMAGEN']
    caption = row['TEXTO_POST']
    print(f"Procesando ID: {row_id} (Fila {row_num})")

    # 1. Generar Imagen
    image_path = generate_image(prompt)
    if not image_path:
        sheet.update_cell(row_num, sheet.find("ESTADO").col, 'ERROR_IMAGEN')
        return

    # 2. Publicar en Facebook
    fb_id = publish_facebook_photo(image_path, caption)
    
    if fb_id:
        print(f"Publicado en FB ID: {fb_id}")
        
        # 3. Publicar en Instagram usando la URL de FB
        fb_url = get_fb_photo_url(fb_id)
        if fb_url:
            ig_id = publish_instagram_photo(fb_url, caption)
            if ig_id:
                print(f"Publicado en IG ID: {ig_id}")
                sheet.update_cell(row_num, sheet.find("ESTADO").col, 'PUBLICADO')
            else:
                sheet.update_cell(row_num, sheet.find("ESTADO").col, 'ERROR_IG')
        else:
             print("No se pudo obtener URL de FB para IG")
             sheet.update_cell(row_num, sheet.find("ESTADO").col, 'PUBLICADO_SOLO_FB')
             
    else:
        sheet.update_cell(row_num, sheet.find("ESTADO").col, 'ERROR_FB')

def main():
    try:
        client = get_google_sheets_client()
        sheet = client.open_by_key(GOOGLE_SHEETS_ID).sheet1
        
        # Obtener todos los registros
        records = sheet.get_all_records()
        
        # Añadir índice de fila para actualizaciones (1-based, +1 por header)
        for i, r in enumerate(records):
            r['ROW_INDEX'] = i + 2
            
        # Filtrar PENDIENTES
        pendientes = [r for r in records if r.get('ESTADO') == 'PENDIENTE']
        
        # Ordenar por ID
        pendientes.sort(key=lambda x: int(x['ID']))
        
        if not pendientes:
            print("No hay publicaciones pendientes.")
            return

        print(f"Encontrados {len(pendientes)} posts pendientes.")

        # MODO PROGRAMADO: Procesar solo el primero pendiente
        target = pendientes[0]
        
        # Verificar HORA_PUBLICACION
        import datetime
        hora_str = target.get('HORA_PUBLICACION', '10:00 AM') # Por defecto 10 AM se no existe
        
        try:
            # Parsear hora (asumiendo formato "10:00 AM" or "10:00")
            now = datetime.datetime.now()
            
            # Limpiar string
            hora_str = str(hora_str).strip().upper()
            
            # Formatos posibles
            if "AM" in hora_str or "PM" in hora_str:
                fmt = "%I:%M %p"
            else:
                fmt = "%H:%M"
                
            scheduled_time = datetime.datetime.strptime(hora_str, fmt).time()
            current_time = now.time()
            
            print(f"Hora programada: {scheduled_time} | Hora actual: {current_time.strftime('%H:%M:%S')}")
            
            # Margen de 5 minutos antes? No, mejor estricto.
            # Check if running in GitHub Actions (skip time check)
            is_github_actions = os.getenv('GITHUB_ACTIONS') == 'true'

            if not is_github_actions and current_time < scheduled_time:
                print(f" [ESPERA] Aún no es la hora de publicación ({hora_str}).")
                print("El script terminará sin publicar.")
                return

        except ValueError as e:
            print(f" [WARN] Error parseando hora ({hora_str}): {e}. Se intentará publicar de todos modos.")

        print(f"Modo Programado: Procesando solo el siguiente post (ID {target['ID']})...")

        print(f"\n--- Procesando Post ID {target['ID']} ---")
        process_row(target, sheet)
        print("Proceso completado. Cerrando script.")
        
    except Exception as e:
        print(f"Error crítico: {e}")

if __name__ == "__main__":
    main()
