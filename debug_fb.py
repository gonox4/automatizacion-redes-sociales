import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('FB_PAGE_ACCESS_TOKEN')
PAGE_ID = os.getenv('FB_PAGE_ID')

# 1. Debug Token
print(f"Verificando token para página: {PAGE_ID}")
debug_url = f"https://graph.facebook.com/debug_token?input_token={TOKEN}&access_token={TOKEN}"
# Nota: debug_token requiere un app access token o user access token, usar el mismo suele funcionar si es user, si es page a veces no.
# Probemos consulta directa a 'me' y 'me/permissions'

url_me = f"https://graph.facebook.com/v19.0/me?access_token={TOKEN}"
r_me = requests.get(url_me)
print(f"Identify Me: {r_me.text}")

url_perms = f"https://graph.facebook.com/v19.0/me/permissions?access_token={TOKEN}"
r_perms = requests.get(url_perms)
print(f"Permisos: {r_perms.json()}")

# Verificar si el ID apunta a un usuario o pagina
url_obj = f"https://graph.facebook.com/v19.0/{PAGE_ID}?metadata=1&access_token={TOKEN}"
r_obj = requests.get(url_obj)
print(f"Objeto ID info: {r_obj.text}")
