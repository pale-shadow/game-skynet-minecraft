import base64

import requests


def generate_skynet_vault_png():
    # Model configuration for high-fidelity raster generation
    model_id = "imagen-4.0-generate-001"
    api_key = ""  # Key provided at runtime
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_id}:predict?key={api_key}"

    # Prompt optimized for industrial technical aesthetic
    prompt = (
        "Internal view of the Skynet neural data vault. A massive subterranean cylinder "
        "filled with glowing blue hexagonal data nodes. Central core features a "
        "vertical plasma-conduit connecting to a Hailo NPU array. Walls are dark "
        "carbon-fiber with gold-plated circuitry traces. Floating holographic "
        "UIs display real-time voxel stream telemetry. Cinematic lighting, "
        "industrial sci-fi, 8k resolution, technical accuracy."
    )

    payload = {"instances": {"prompt": prompt}, "parameters": {"sampleCount": 1}}

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()

        image_data = result["predictions"][0]["bytesBase64Encoded"]
        image_url = f"data:image/png;base64,{image_data}"

        # Output result for Canvas display
        print(f"Generated PNG available at: {image_url[:50]}...")
        return image_url
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    generate_skynet_vault_png()
