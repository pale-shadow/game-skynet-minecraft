import os
import pytest
from google import genai
from src.utils.config_utils import setup_logging

logger = setup_logging("test_gemini_link")

@pytest.mark.skipif("GOOGLE_API_KEY" not in os.environ, reason="GOOGLE_API_KEY not set")
def test_connection():
    logger.info("--- Skynet Handshake Initializing ---")
    client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents="Confirm link established. System status: Raspberry Pi 5 / aarch64. Respond with a witty Skynet-themed confirmation.",
        )
        logger.info(f"[RESPONSE FROM GEMINI]:\n{response.text}")
        logger.info("--- Connection Successful ---")
    except Exception as e:
        pytest.fail(f"Connection failed: {e}")
