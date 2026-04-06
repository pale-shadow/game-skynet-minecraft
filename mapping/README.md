# Mapping and Telemetry Module
This directory contains the essential scripts and documentation for managing the BlueMap interface and spatial data validation across the Bitsmasher network. It ensures that the "Void-Tech" urbanization of the northern frontier and the Skynet AI Testing Field are accurately tracked and visualized
.
Directory Structure
bluemap_api.py: A Python-based interface designed to interact with the BlueMap API
. It is used for the dynamic injection of markers and landmarks, such as the Skynet Inference Nexus (Hub 01) and the Neural-Data Vault (Hub 07), into the live web-app
.
verify_ai_field_coords.py: A critical validation script used to audit and verify the coordinates of the Skynet AI Testing Field hubs. This script is crucial for ensuring "Reactive Mutations" are correctly positioned and for preventing overlap or chunk corruption within existing zones. For pre-deployment 3D AABB overlap detection of *new* builds, `schematics/validate_no_overlaps.py` is utilized.
push.sh: A deployment utility script for pushing local mapping configurations and HTML assets to the live Stargate node and webserver. It complements the broader bin/backup_to_git.sh workflow for maintaining the server's technical ledger
.
mapping.html / mapping.md: Core documentation and front-end assets for the BlueMap Telemetry interface, providing the historical context for landmarks like Glass City and the Severed Legacy Rail
.
notes.txt: Internal developer logs regarding the "Great Chunk Loss" and historical coordinate offsets required for legacy rail line alignment
.
Operational Context
Visualization and Telemetry
The mapping module is configured to render the Dreamland (Overworld) and Nether dimensions using the BlueMap plugin
. It utilizes SQL storage rather than standard file-based storage to improve the query performance of the "Neural-Data Vault"
.
Performance Monitoring
In line with our 20 TPS goal, the mapping scripts are designed to work alongside the Spark profiler
. By monitoring "tick time" and chunk loading lag through the BlueMap interface, admins can identify if specific AI-driven building tasks are impacting server stability
.
Security and Protection
All spatial data managed by these scripts is protected by the WorldGuard and CoreProtect frameworks
. This ensures that while the Skynet Unified Brain urbanizes the frontier, all changes are logged for immediate rollback if a "Void-Tech" anomaly occurs
.
Deployment
After modifying markers or coordinate data:
Run verify_ai_field_coords.py to ensure hub alignment.
Execute push.sh to update the Stargate node assets.
Execute /bluemap reload via RCON to push the changes to the live web interface.
After terrain resets, use `bluemap fix-edges` for visual continuity.

```sh
detail: """
    <h3>Skynet NPU Node: PI-5</h3>
    <p>Status: <b style='color:#31d1a3'>ACTIVE</b></p>
    <p>NPU Temp: <b>42°C</b></p>
    <p>Inference Latency: <b>4.2ms</b></p>
    <hr>
    <p><i>Processing real-time voxel mapping for the Abyssal Reef...</i></p>
"""
```
