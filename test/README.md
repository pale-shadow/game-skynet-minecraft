# Skynet Distributed Test Suite

- [Minecraft stuff](https://github.com/pale-shadow/game-chonk-minecraft)

This directory contains the validation framework for the Stargate MCP and the hardware-accelerated "Void-Tech" infrastructure. These tests ensure that AI-driven urbanization remains within the **20 TPS performance ceiling** [1].

## Test Case Details

### AI & Logic (T2BM Pipeline)
  - **test_gemini_link.py**: Validates the **prompt refinement** phase using the Gemini 2.0 Flash API [4].
  - **test_hailo_npu_decoding_validity.py**: Audits **interlayer representation decoding** on the Raspberry Pi 5 and Hailo-8L NPU [4].
  - **test_builders.py**: Exercises the **repairing and construction** logic for autonomous builders (Tower, Castle) [4].
  - **test_brain.py**: Verifies the core `SkynetUnifiedDaemon` and primary logic core at the Inference Nexus (Hub 01) [5].

### Hardware & Connectivity
  - **test_rcon.py**: Confirms the RCON signal path to the **Transmission Core (Hub 02)** for schematic injection [5].
  - **test_tpu.py**: Specifically targets connectivity for the **Edge TPU Vision node** at Hub 06 [5].
  - **test_hardware.py**: Uses the `@pytest.mark.hardware` decorator for broad audits of physical Skynet hubs [5].
  - **test_neural_vault_logging_persistence.py**: Ensures encrypted AI logs are successfully persisted to the **Neural-Data Vault (Hub 07)** [5].

### Spatial Safety & Performance
  - **test_schematic_boundary_safety.py**: Uses the **NPUSpatialEngine** to prevent collisions with existing builds or designated hubs [5, 6].
  - **test_schematic_tps_impact_threshold.py**: Simulates the tick-time cost of new mutations to ensure they do not exceed the 20 TPS threshold [1, 2].

## Performance Monitoring

If these tests indicate performance bottlenecks, use the **Spark profiler** (bundled with Paper 1.21.1) for real-time diagnostics:

`/spark profiler start --timeout 600`

## Schematics

Go tools

```sh
mkdir -p ~/src/schematic-go
cd ~/src/schematic-go
go mod init github.com/chonk/minecraft-station
go get github.com/Tnze/go-mc@master
```
