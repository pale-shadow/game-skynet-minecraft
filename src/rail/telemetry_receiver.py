import asyncio
import json
import logging

from src.rail.rail_manager import RailManager
from src.utils.config_utils import setup_logging

# Configure logging specifically for rail traffic
rail_traffic_logger = setup_logging("rail_traffic", log_file="logs/rail_traffic.log")
logger = setup_logging("telemetry_receiver") # General logger for this module

class RailTelemetryProcessor:
    def __init__(self):
        self.rail_manager = RailManager()
        logger.info("RailTelemetryProcessor initialized.")

    async def _orchestrate_with_llm(self, event_data):
        """
        Placeholder for LLM interaction to determine train priority and switch scheduling.
        In a real scenario, this would involve an RPC call to the Ollama LLM.
        """
        rail_traffic_logger.info(f"LLM Orchestration: Receiving event for analysis: {event_data}")
        # Simulate LLM decision
        # For now, let's assume the LLM always decides to toggle the switch based on the event.
        # In a real scenario, the LLM might return a specific action or a series of actions.
        
        # Example decision: If a CART_PASS event is for 'chonk_01_sensor',
        # the LLM decides to activate the corresponding switch.
        node = event_data.get("NODE")
        # Assuming node_mapping from cart_handler.py for consistency
        node_mapping = {
            "CHONK-01": "chonk_01_sensor",
            "CHONK-02": "chonk_02_sensor",
            "CHONK-03": "chonk_03_sensor"
        }
        switch_id = node_mapping.get(node)

        if switch_id:
            # Simulate LLM deciding to activate the switch
            llm_decision = {"action": "toggle_switch", "switch_id": switch_id, "state": True}
        else:
            llm_decision = {"action": "no_action"}

        rail_traffic_logger.info(f"LLM Orchestration: Decision for {node}: {llm_decision}")
        return llm_decision

    async def process_rail_event(self, event_data):
        """
        Ingests, parses, logs, and orchestrates rail telemetry events.
        """
        rail_traffic_logger.info(f"Received rail telemetry: {json.dumps(event_data)}")

        raw_decision = await self._orchestrate_with_llm(event_data)
        decisions = raw_decision if isinstance(raw_decision, list) else [raw_decision]
        for llm_decision in decisions:
            action = llm_decision.get("action")
            
            if action == "toggle_switch":
                switch_id = llm_decision.get("switch_id")
                state = llm_decision.get("state")
                logger.info(f"Orchestrator activating switch: {switch_id} to state {state}")
                
                # Execute via thread pool for non-async RailManager
                success = await asyncio.to_thread(self.rail_manager.toggle_switch, switch_id, state)
                if success:
                    logger.info(f"Successfully executed LLM decision for {switch_id}.")
                else:
                    logger.error(f"Failed to execute LLM decision for {switch_id}.")
                    
            elif action == "no_action":
                logger.info("LLM decided no action is needed for this event.")
            else:
                logger.warning(f"Unknown LLM decision: {action}. Taking no action.")

if __name__ == "__main__":
    # This block allows for standalone testing/simulation of the processor.
    async def simulate_event():
        processor = RailTelemetryProcessor()
        test_event = {
            "EVENT": "CART_PASS",
            "NODE": "CHONK-01",
            "coords": {"x": 100, "y": 64, "z": 200},
            "timestamp": "2026-05-06T12:00:00Z"
        }
        await processor.process_rail_event(test_event)

    try:
        asyncio.run(simulate_event())
    except KeyboardInterrupt:
        logger.info("Telemetry receiver simulation stopped.")
