# Ollama Integration: Local Architectural Inference

This document details the setup and integration of Ollama into the Bitsmasher Minecraft AI network. By migrating from Gemini to local inference, we ensure the **Stargate** node (Pi 5 + NVMe) can handle high-density architectural intents without cloud latency, supporting our **20 TPS** performance goal.

## 1. Recommended Model: Llama 3.1 8B

For the **T2BM (Text to Building in Minecraft)** pipeline, we recommend **Llama 3.1 8B**.

*   **Why:** It is the current state-of-the-art for local inference in the 8B class. It excels at following complex spatial instructions and generating the "Noodle Logic" required for our v5 industrial schematics.
*   **Hardware Fit:** On a **Raspberry Pi 5 (8GB)**, the 4-bit quantized version (approx 4.7GB) fits comfortably within memory, leaving room for the system and the MCP stack.
*   **Alternative (Lightweight):** If memory becomes a constraint during heavy Hailo-8L geometric expansion, use `phi3.5` (3.8B).

## 2. Installation

Run the following command on the **Stargate** host:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Pull the Model
```bash
ollama pull llama3.1:8b
```

## 3. Python Integration

Add the `ollama` library to the local environment:

```bash
pip install ollama
```

### Sample CLI Bridge (`ollama-cli`)
Create a simple bridge to match the `gemini-cli` workflow:

```python
#!/usr/bin/env python3
import sys
import ollama

user_input = " ".join(sys.argv[1:])
if not user_input and not sys.stdin.isatty():
    user_input = sys.stdin.read()

if not user_input:
    print("Usage: ./ollama-cli 'Build a Void-Tech spire'")
    sys.exit(0)

response = ollama.chat(model='llama3.1:8b', messages=[
  {
    'role': 'user',
    'content': user_input,
  },
])
print(response['message']['content'])
```

## 4. MCP Integration

To expose Ollama as an MCP tool, we are introducing `src/mcp_server/ollama_service.py`. This allows the **Skynet Unified Brain** to request architectural intent refinement locally.

### Configuration (`mcp-servers.json`)
Add the following entry to your MCP configuration:

```json
"ollama-stargate": {
  "command": "python3",
  "args": ["src/mcp_server/ollama_service.py"],
  "env": {
    "OLLAMA_HOST": "http://localhost:11434"
  }
}
```

## 5. Architectural Style Enforcement

When prompting Ollama for "Void-Tech" designs, ensure the system prompt includes our v5 standards:
- **Primary Block:** Polished Tuff (`minecraft:polished_tuff`)
- **Accent:** Obsidian/Crying Obsidian
- **Lighting:** Froglights (`minecraft:pearlescent_froglight`)
- **Depth:** Mandatory Rule of Three (Base, Pillar, Girder)

---
*Created for theDevilsVoice | Last Updated: April 29, 2026*
