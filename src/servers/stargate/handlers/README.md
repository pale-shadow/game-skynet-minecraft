# Stargate Event Handlers

This directory contains modular handlers for telemetry events received from the Chonk host.

## Adding a New Handler

1. Create a new python file in this directory (e.g., `my_event_handler.py`).
2. Define an asynchronous function that takes a `payload` (dict) as an argument.
3. Register the new handler in `src/servers/stargate/telemetry_listener.py` by adding it to the `EVENT_HANDLERS` dictionary.

### Example

```python
async def handle_my_event(payload):
    print(f"Received my event with data: {payload}")
```
