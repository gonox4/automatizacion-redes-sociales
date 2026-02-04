import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image, ImageDraw, ImageFont

# Load env
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    print("Error: No GEMINI_API_KEY found")
    sys.exit(1)

def test_gen():
    print("Testing Image Generation with Imagen 3 (new SDK)...")
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        # List models first to see what's available
        print("Listing available models...")
        for m in client.models.list(config={'page_size': 100}):
            print(f" - {m.name}")

        response = client.models.generate_images(
            model='imagen-4.0-generate-001',
            prompt='A futuristic city with flying cars, photorealistic, 8k',
            config=types.GenerateImagesConfig(
                number_of_images=1,
            )
        )
        if response.generated_images:
            image = response.generated_images[0]
            output_path = "test_gen_result.png"
            image.image.save(output_path)
            print(f"Success! Image saved to {output_path}")
        else:
            print("No images generated.")

    except Exception as e:
        print(f"Error generating image: {e}")
        import traceback
        traceback.print_exc()

def test_fallback():
    print("\nTesting Fallback (PIL)...")
    try:
        img = Image.new('RGB', (1024, 1024), color = (73, 109, 137))
        d = ImageDraw.Draw(img)
        
        # Try to load a standard font
        try:
            # Windows standard font
            font_title = ImageFont.truetype("arial.ttf", 60)
            font_text = ImageFont.truetype("arial.ttf", 40)
        except IOError:
            # Fallback to default
            print("Could not load arial.ttf, using default font")
            font_title = ImageFont.load_default()
            font_text = ImageFont.load_default()

        # Draw centered text
        text_title = "Imagen Generada Automaticamente"
        text_prompt = "Prompt: Test Prompt..."
        
        # Approximate positioning
        d.text((50, 400), text_title, fill=(255, 255, 255), font=font_title)
        d.text((50, 500), text_prompt, fill=(220, 220, 220), font=font_text)
        
        img.save("test_fallback.png")
        print("Fallback image saved to test_fallback.png")
    except Exception as e:
        print(f"Error in fallback: {e}")

if __name__ == "__main__":
    test_gen()
    test_fallback()
    
    print("\n--- Diagnostic: Text Generation Test ---")
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model='gemini-2.5-flash', contents='Say "API Key is working"'
        )
        print(f"Text Gen Result: {response.text}")
    except Exception as e:
        print(f"Text Gen Error: {e}")

