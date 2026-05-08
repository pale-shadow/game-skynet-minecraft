
import os
import requests

api_key = os.getenv("VERTEX_AI_KEY")
if not api_key:
    print("[-] Error: VERTEX_AI_KEY is not set!")
    exit(1)

# Endpoint for Vertex AI Gemini model
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

headers = {'Content-Type': 'application/json'}

# The high-temperature "Visionary" test prompt
payload = {
    "contents": [{
        "parts": [{
            "text": "You are the Visionary Greebler. We have a simple 5x5x5 cobblestone cube. Suggest a highly creative, chaotic sci-fi mechanical mutation to transform this cube into an industrial generator. Describe the pipes, copper coils, and venting layout."
        }]
    }],
    "generationConfig": {
        "temperature": 1.2  # Cranking the heat for maximum creativity!
    }
}

print("[*] Initiating Emerald Mirror handshake via Skynet...")
response = requests.post(url, json=payload, headers=headers)

if response.status_code == 200:
    print("[+] Handshake successful! The Visionary says:\n")
    print(response.json()['candidates'][0]['content']['parts'][0]['text'])
else:
    print(f"[-] Handshake failed. Status Code: {response.status_code}")
    print(response.text)
