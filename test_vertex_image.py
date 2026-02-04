import os
from google import genai
from google.genai import types
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()

PROJETC_ID = 'bot-redes-486401'
KEY_PATH = 'credentials.json'
LOCATION = 'us-central1'

def test_vertex_gen():
    print(f"Testing Vertex AI Image Generation for project {PROJETC_ID}...")
    try:
        # Load credentials explicitly
        creds = service_account.Credentials.from_service_account_file(
            KEY_PATH,
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
        
        # Init client in Vertex AI mode
        client = genai.Client(
            vertexai=True,
            project=PROJETC_ID,
            location=LOCATION,
            credentials=creds
        )
        
        print("Listing available Vertex AI models...")
        for m in client.models.list(config={'page_size': 100}):
             print(f" - {m.name}")

        print("Client initialized. Attempting generation...")
        # Try a model that is likely to exist in Vertex AI
        model_name = 'imagen-3.0-generate-001' 
        
        # List models to be sure what to call? 
        # But let's just try generate first.
        
        response = client.models.generate_images(
            model=model_name,
            prompt='A cyberpunk city with neon lights',
            config=types.GenerateImagesConfig(
                number_of_images=1,
            )
        )
        
        if response.generated_images:
            output_path = "test_vertex_result.png"
            response.generated_images[0].image.save(output_path)
            print(f"Success! Image saved to {output_path}")
        else:
            print("No images generated.")

    except Exception as e:
        print(f"Error generating image via Vertex: {e}")
        # If model doesn't exist, it usually errors with NOT_FOUND.

if __name__ == "__main__":
    test_vertex_gen()
