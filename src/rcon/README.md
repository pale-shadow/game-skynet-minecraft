# RCON Bridge (Skynet Execution Layer)

This directory contains the execution scripts for the **Skynet Architect** system, interfacing with the Minecraft server via RCON.

## Execution Tools
- **`rcon.sh`**: A shell script for manual RCON interaction and testing.
- **`npu_architect.py`**: A low-level Python RCON bridge optimized for high-throughput voxel data delivery.

## Delivery Protocol
The system uses **High-Speed RCON** with a 0.005s sleep per command, ensuring that NPU-generated "Void-Tech" structures are deployed in real-time with minimal server lag.
