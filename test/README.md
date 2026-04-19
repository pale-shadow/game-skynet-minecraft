# Skynet Distributed Test Suite

- [Minecraft stuff](https://github.com/pale-shadow/game-skynet-minecraft)

This directory contains the validation framework for the Stargate MCP and the hardware-accelerated "Void-Tech" infrastructure. These tests ensure that AI-driven urbanization remains within the **20 TPS performance ceiling** [1].

## Recent Updates (April 17, 2026)
- **Database Vault Expansion**: Implemented multi-database connectivity testing for `luckperms`, `bluemap`, `coreprotect`, and `skynet_vault` on Hub 07 (`blowfish`).
- **Schema Validation**: Added integrity checks for the `skynet_vault.build_history` table to ensure spatial query compatibility.
- **Chunk Integrity Audit**: Introduced a new scanner for Minecraft `.mca` region files to detect header corruption and truncated data, mitigating the risk of "Ghost" chunk stalls.
- **Credential Review**: Conducted a security audit of database usernames and connection strings; verified placeholder usage in test environments.

## Test Case Details

### AI & Logic (T2BM Pipeline)
  - **test_gemini_link.py**: Validates the **prompt refinement** phase using the Gemini 2.0 Flash API [4].
  - **test_hailo_npu_decoding_validity.py**: Audits the Raspberry Pi 5 and Hailo-8L NPU's **spatial inference capabilities** to find optimal build vectors.
  - **test_builders.py**: Exercises the **repairing and construction** logic for autonomous builders (Tower, Castle) [4].
  - **test_brain.py**: Verifies the core `SkynetUnifiedDaemon` and primary logic core at the Inference Nexus (Hub 01) [5].

### Hardware & Connectivity
  - **test_rcon.py**: Confirms the RCON signal path to the **Transmission Core (Hub 02)** for schematic injection [5].
  - **test_tpu.py**: Specifically targets connectivity for the **Edge TPU Vision node** at Hub 06 [5].
  - **test_hardware.py**: Uses the `@pytest.mark.hardware` decorator for broad audits of physical Skynet hubs [5].
  - **test_neural_vault_logging_persistence.py**: Ensures encrypted AI logs are successfully persisted to the **Neural-Data Vault (Hub 07)** [5].
  - **test_vault_multi_db_connectivity.py**: **(New)** Validates cross-schema access and permissions for all MariaDB instances on Hub 07.

### Spatial Safety & World Integrity
  - **test_schematic_metadata_integrity.py**: Verifies that every schematic file has a corresponding, valid JSON metadata file.
  - **test_schematic_boundary_safety.py**: Uses the **NPUSpatialEngine** to prevent collisions with existing builds [5, 6].
  - **test_schematic_tps_impact_threshold.py**: Simulates the tick-time cost of new mutations.
  - **test_chunk_integrity.py**: **(New)** Scans the world region files (`.mca`) for structural integrity and corruption.

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
