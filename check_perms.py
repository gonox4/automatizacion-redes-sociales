import os
import requests
from dotenv import load_dotenv
import sys

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()

TOKEN = os.getenv('FB_PAGE_ACCESS_TOKEN')
APP_ID = os.getenv('FB_APP_ID')
APP_SECRET = os.getenv('FB_APP_SECRET')

print(f"Token present: {'Yes' if TOKEN else 'No'}")
if TOKEN:
    print(f"Token length: {len(TOKEN)}")
    print(f"Token starts with: {TOKEN[:10]}...")

if not TOKEN:
    print("❌ No token found in .env variable FB_PAGE_ACCESS_TOKEN")
    sys.exit(1)

# Debug token
url = f"https://graph.facebook.com/v21.0/debug_token"
params = {
    'input_token': TOKEN,
    'access_token': f"{APP_ID}|{APP_SECRET}" # App access token needed for debug
}

print("\n--- Verificando Permisos ---")
try:
    # First try /me/permissions which is easier
    me_url = f"https://graph.facebook.com/v21.0/me/permissions?access_token={TOKEN}"
    r = requests.get(me_url)
    if r.status_code == 200:
        data = r.json()
        print("Permisos concedidos:")
        for perm in data.get('data', []):
            if perm.get('status') == 'granted':
                print(f" - {perm.get('permission')}")
            else:
                print(f" - {perm.get('permission')} ({perm.get('status')})")
    else:
        print(f"Error checking /me/permissions: {r.text}")

except Exception as e:
    print(f"Error: {e}")
