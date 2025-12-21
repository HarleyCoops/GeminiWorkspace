import os
from google import genai
from src.config import settings

def list_models():
    try:
        client = genai.Client(api_key=settings.GOOGLE_API_KEY)
        print("Listing available Gemini models:")
        for model in client.models.list():
            print(f" - {model.name}")
    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    list_models()
