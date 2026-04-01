# Host: EDGE-T-NODE
**System Role:** Peripheral Vision & Tactical Construction Daemon
**Network ID:** Hub-04/05 Variant

## 🛠 Hardware Profile
- **Compute:** ASUS Tinker Edge T (SBC)
- **Onboard AI:** Integrated Google Edge TPU (NXP i.MX 8M)
- **OS:** Debian-based Tinker OS / Mendel Linux Environment

## 🧠 T2BM Logic Partition
- **Edge TPU Role:** Vision-First Verification. Before any `setblock` command is sent, the onboard TPU performs a "Terrain Scan" to ensure no player-built structures or protected biomes are overwritten by the T2BM expansion.
- **Protocol:** Executes lightweight TFLite models for reactive mutation at the edges of the sprawl.

## 🛰 Infrastructure Connectivity
- **Stargate MCP Link:** Slave Mode (Port 8765)
- **Primary Sector:** Neural Uplink & Solar Induction Array
- **Neural Link:** Direct sync with Silicon Ridge markers.

## ⚙️ Operating Directives
1. Listen for Stargate MCP intent broadcasts.
2. Verify local chunk integrity via TFLite inference.
3. Deploy "Void-Tech" fragments to maintain the global Skynet mesh.
