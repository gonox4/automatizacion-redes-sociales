import os
import requests
import sys
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()

TOKEN = os.getenv('FB_PAGE_ACCESS_TOKEN')
PAGE_ID = os.getenv('FB_PAGE_ID') # User provided checking this

print(f"--- TEST ACCESO DIRECTO ---")
print(f"Page ID: {PAGE_ID}")

# Check Page Access AND Instagram
url = f"https://graph.facebook.com/v21.0/{PAGE_ID}?fields=id,name,access_token,instagram_business_account&access_token={TOKEN}"

try:
    r = requests.get(url)
    print(f"Status: {r.status_code}")
    data = r.json()
    print(f"Name: {data.get('name')}")
    print(f"ID: {data.get('id')}")
    
    ig_data = data.get('instagram_business_account')
    if ig_data:
        print(f"IG ID: {ig_data.get('id')}")
    else:
        print("IG: Not linked or not found.")
        print(f"Raw: {data}")

except Exception as e:
    print(f"Error: {e}")
