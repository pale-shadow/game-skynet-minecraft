# Skynet Distributed Test Suite GEMINI Context

This document provides a Gemini-specific overview of the Skynet Distributed Test Suite, detailing the purpose and scope of each test module within the `/test` directory.

## 1. Purpose

The Skynet Distributed Test Suite is designed to validate the Stargate MCP and the hardware-accelerated "Void-Tech" infrastructure. Its primary goal is to ensure that AI-driven urbanization operations remain within the **20 TPS performance ceiling** and adhere to safety protocols.

## 2. Test Categories and Descriptions

### 2.1. AI & Logic (T2BM Pipeline)

*   **`test_gemini_link.py`**: Validates the **prompt refinement** phase using the Gemini 2.0 Flash API. Confirms connectivity and responsiveness of the AI's input processing.
*   **`test_hailo_npu_decoding_validity.py`**: Audits the Raspberry Pi 5 and Hailo-8L NPU's **spatial inference capabilities** to find optimal build vectors. This ensures the NPU accurately identifies suitable locations for new structures, rather than decoding raw architectural concepts (which is a Stargate responsibility).
*   **`test_builders.py`**: Exercises the **repairing and construction** logic for autonomous builders (e.g., Tower, Castle). Verifies that builder scripts function correctly and add blocks to schematics.
*   **`test_brain.py`**: Verifies the core `SkynetUnifiedDaemon` and its interactions with other components, focusing on the primary logic core at the Inference Nexus (Hub 01).

### 2.2. Hardware & Connectivity

*   **`test_rcon.py`**: Confirms the RCON signal path to the **Transmission Core (Hub 02)**. This is essential for the T2BM pipeline and maintaining the 20 TPS goal, ensuring commands can be sent and received.
*   **`test_tpu.py`**: Specifically targets connectivity for the **Edge TPU Vision node** at Hub 06. Verifies the Vision Overseer's readiness for tasks like classification.
*   **`test_hardware.py`**: Performs broad audits of physical Skynet hubs (Hailo-8L NPU and Edge TPU) using the `@pytest.mark.hardware` decorator, ensuring hardware presence and basic functionality.
*   **`test_neural_vault_logging_persistence.py`**: Ensures encrypted AI logs are successfully persisted to the **Neural-Data Vault (Hub 07)**, supporting grief recovery mechanisms.

### 2.3. Spatial Safety & Performance

*   **`test_schematic_boundary_safety.py`**: Uses the **NPUSpatialEngine** to prevent collisions with existing builds or designated hubs, ensuring that new constructions do not interfere with critical infrastructure.
*   **`test_schematic_tps_impact_threshold.py`**: Simulates the tick-time cost of new mutations to ensure they do not exceed the 20 TPS threshold, crucial for server stability.

## 3. Performance Monitoring

If tests indicate performance bottlenecks, the **Spark profiler** (bundled with Paper 1.21.1) is recommended for real-time diagnostics. The command `spark profiler start --timeout 600` can be used.

## 4. Go Tools (Schematics)

Information regarding Go tools for schematic generation can be found in the `schematics` directory, including setup commands like:
```sh
mkdir -p ~/src/schematic-go
cd ~/src/schematic-go
go mod init github.com/chonk/minecraft-station
go get github.com/Tnze/go-mc@master
```
