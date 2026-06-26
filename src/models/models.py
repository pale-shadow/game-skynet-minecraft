from google import genai
import os

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set")
client = genai.Client(api_key=api_key)
for model in client.models.list():
    print(model.name)
