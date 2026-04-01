import os

from google import genai

# Setup client - Replace 'YOUR_API_KEY' with your actual key
# Or set it in your shell: export GOOGLE_API_KEY='your_key_here'
client = genai.Client(api_key="YOUR_API_KEY")


def test_connection():
    print("--- Skynet Handshake Initializing ---")
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents="Confirm link established. System status: Raspberry Pi 5 / aarch64. Respond with a witty Skynet-themed confirmation.",
        )

        print(f"\n[RESPONSE FROM GEMINI]:\n{response.text}")
        print("\n--- Connection Successful ---")
    except Exception as e:
        print(f"\n[ERROR]: Connection failed. Details: {e}")


if __name__ == "__main__":
    test_connection()
