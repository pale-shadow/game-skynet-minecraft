import os
import pytest
from google import genai

@pytest.mark.skipif("GOOGLE_API_KEY" not in os.environ, reason="GOOGLE_API_KEY not set")
def test_connection():
    print("--- Skynet Handshake Initializing ---")
    client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents="Confirm link established. System status: Raspberry Pi 5 / aarch64. Respond with a witty Skynet-themed confirmation.",
        )
        print(f"\n[RESPONSE FROM GEMINI]:\n{response.text}")
        print("\n--- Connection Successful ---")
    except Exception as e:
        pytest.fail(f"Connection failed: {e}")
