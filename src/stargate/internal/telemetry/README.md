# Stargate Telemetry Internal Logic

This directory contains internal logic for the telemetry listener, including:

- **Packet Validation**: Ensuring incoming data matches expected schemas (`validator.py`).
- **Socket Utilities**: (Future) specialized socket handling or protocol-specific logic.

This code should be decoupled from the high-level event handling logic found in the `handlers/` directory.
