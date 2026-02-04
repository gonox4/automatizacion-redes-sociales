import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai.errors import ClientError

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    print("Error: No GEMINI_API_KEY in .env")
    sys.exit(1)

client = genai.Client(api_key=api_key)

models_to_test = [
    'gemini-1.5-flash',
    'gemini-2.0-flash',
    'gemini-2.5-flash',
    'gemini-2.5-flash-8b',
    'gemini-2.5-pro',
]

print(f"--- Diagnostic: Testing Models with API Key ending in ...{api_key[-4:]} ---\n")

for model in models_to_test:
    print(f"Testing {model}...", end=" ", flush=True)
    try:
        response = client.models.generate_content(
            model=model,
            contents="Say 'Hello'"
        )
        print(f"SUCCESS: {response.text.strip()}")
    except ClientError as e:
        print(f"FAILED (ClientError): {str(e)[:200]}")
    except Exception as e:
        print(f"FAILED (General): {str(e)[:200]}")

print("\n--- Diagnostic Complete ---")
