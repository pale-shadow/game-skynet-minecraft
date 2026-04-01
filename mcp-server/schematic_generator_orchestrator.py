
import argparse
import json
import os
import sys

import requests

# --- Configuration Loading ---
# Assumes mcp-servers.json is located in the same directory as this script
# or accessible via a known path.
MCP_CONFIG_PATH = "mcp-server/mcp-servers.json"

# Placeholder for default ports if not specified in config
DEFAULT_PORTS = {
    "filesystem-stargate": 8081,
    "rcon-chonk": 8082,
    "git-ledger": 8083,
    "vision-edge-t": 8084,
    "npu-skynet": 8085,
}

def load_mcp_configuration(config_path):
    """Loads MCP server configurations from a JSON file."""
    if not os.path.exists(config_path):
        print(f"Error: MCP configuration file not found at {config_path}", file=sys.stderr)
        sys.exit(1)
    try:
        with open(config_path, 'r') as f:
            config_data = json.load(f)
            return config_data.get("mcpServers", {})
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {config_path}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error loading configuration from {config_path}: {e}", file=sys.stderr)
        sys.exit(1)

# Load configuration globally when the script is imported or run
MCP_SERVER_CONFIG = load_mcp_configuration(MCP_CONFIG_PATH)

# --- MCP Client ---
class MCPServiceError(Exception):
    """Custom exception for MCP service errors."""
    pass

class MCPClient:
    def __init__(self, service_name, base_url):
        self.service_name = service_name
        self.base_url = base_url

    def _request(self, method, endpoint, payload=None):
        """Helper to make HTTP requests to an MCP service."""
        url = f"{self.base_url}/{endpoint}"
        try:
            # print(f"DEBUG: Requesting {method} {url} with payload: {json.dumps(payload)}") # Uncomment for debugging
            response = requests.request(method, url, json=payload, timeout=30) # Added timeout
            response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
            return response.json()
        except requests.exceptions.Timeout:
            raise MCPServiceError(f"Request timed out calling MCP service {self.service_name} at {url}")
        except requests.exceptions.RequestException as e:
            # Attempt to get error details from response if available
            error_detail = ""
            if e.response is not None:
                try:
                    error_detail = e.response.json()
                except json.JSONDecodeError:
                    error_detail = e.response.text
            raise MCPServiceError(f"Error calling MCP service {self.service_name} at {url}: {e}. Details: {error_detail}")

    def call(self, method, params=None):
        """
        Calls an MCP service method.
        The endpoint is derived from the method name by replacing underscores with hyphens.
        """
        # Convert method name (snake_case) to endpoint name (kebab-case)
        endpoint = method.replace('_', '-')
        
        # Construct the payload. MCP services might expect specific structures.
        # This generic structure assumes a 'params' key. Adjust if services expect otherwise.
        payload = {"params": params} 
        
        return self._request(method='POST', endpoint=endpoint, payload=payload)

def get_mcp_client(service_name):
    """
    Returns an MCPClient instance configured for the given service name.
    Dynamically constructs the base URL from loaded configuration.
    """
    config = MCP_SERVER_CONFIG.get(service_name)
    if not config:
        raise ValueError(f"Service configuration not found for '{service_name}' in {MCP_CONFIG_PATH}")

    base_url = None
    if config.get("remote"):
        # For remote services, use the specified host and infer port or use default
        host = config["remote"].get("host")
        port = config["remote"].get("port", DEFAULT_PORTS.get(service_name))
        if not host or not port:
            raise ValueError(f"Missing host or port for remote service '{service_name}' configuration.")
        base_url = f"http://{host}:{port}"
    else:
        # For local services, assume localhost and infer port or use default
        host = "localhost"
        port = config.get("port", DEFAULT_PORTS.get(service_name)) # Allow explicit port in config
        if not port:
             raise ValueError(f"Missing port for local service '{service_name}' configuration.")
        base_url = f"http://{host}:{port}"
        
    return MCPClient(service_name, base_url)

# --- Orchestration Logic ---
def orchestrate_schematic_generation(prompt: str, design_id: str, location_criteria: dict):
    """
    Orchestrates the schematic generation process by calling various MCP services.
    """
    print(f"Starting schematic generation for ID: '{design_id}'")

    # 1. Analyze terrain using Vision MCP on Edge-T
    print("Step 1: Analyzing terrain using Vision MCP (vision-edge-t)...")
    try:
        vision_client = get_mcp_client("vision-edge-t")
        terrain_analysis = vision_client.call(
            "analyze_terrain",
            {"criteria": location_criteria, "context": "schematic_generation"}
        )
        if not terrain_analysis or terrain_analysis.get("error"):
            raise MCPServiceError(f"Vision MCP error: {terrain_analysis.get('error', 'Unknown error')}")
        print(f"Terrain analysis complete. Data: '{terrain_analysis.get('terrain_data')}', Score: {terrain_analysis.get('analysis_score')}")

        # Simple check: If terrain is not suitable, abort.
        # This threshold is an example and might need tuning.
        if terrain_analysis.get("analysis_score", 0) < 0.8:
            print(f"Terrain analysis score ({terrain_analysis.get('analysis_score')}) is below threshold. Aborting generation.")
            return None
    except (MCPServiceError, ValueError) as e:
        print(f"Error in Step 1 (Vision MCP): {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"An unexpected error occurred in Step 1: {e}", file=sys.stderr)
        return None


    # 2. Generate schematic using NPU Skynet MCP (on Stargate)
    print("Step 2: Generating schematic using NPU Skynet MCP (npu-skynet)...")
    try:
        npu_client = get_mcp_client("npu-skynet")
        generation_params = {
            "prompt": prompt,
            "id": design_id,
            "terrain_data": terrain_analysis.get("terrain_data"), # Pass analysis results to generator if needed
            "terrain_score": terrain_analysis.get("analysis_score")
        }
        schematic_info = npu_client.call(
            "generate_schematic",
            generation_params
        )
        if not schematic_info or schematic_info.get("error"):
            raise MCPServiceError(f"NPU Skynet MCP error: {schematic_info.get('error', 'Unknown error')}")

        schematic_path = schematic_info.get("schematic_path")
        metadata_path = schematic_info.get("metadata_path")
        if not schematic_path or not metadata_path:
            raise MCPServiceError("NPU Skynet MCP did not return valid schematic or metadata paths.")
        print(f"Schematic generated at: '{schematic_path}'. Metadata at: '{metadata_path}'")
    except (MCPServiceError, ValueError) as e:
        print(f"Error in Step 2 (NPU Skynet MCP): {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"An unexpected error occurred in Step 2: {e}", file=sys.stderr)
        return None

    # 3. Save schematic and metadata using Filesystem MCP
    print("Step 3: Saving schematic and metadata using Filesystem MCP (filesystem-stargate)...")
    try:
        # In a real application, you'd read the actual file content from a temporary location
        # or directly from the NPU service's output. For now, mocking content.
        # NOTE: In a real scenario, the NPU service might return file contents directly or write to a shared volume.
        # Here, we simulate writing some placeholder content.
        generated_schematic_content = f"--- Mock schematic content for {design_id} ---
# Generated by AI
# Prompt: {prompt}
"
        generated_metadata_content = json.dumps({
            "generated_by": "schematic-orchestrator",
            "prompt": prompt,
            "design_id": design_id,
            "terrain_analysis": terrain_analysis,
            "generation_time_ms": schematic_info.get("generation_time_ms")
        }, indent=2)

        fs_client = get_mcp_client("filesystem-stargate")
        write_schematic_result = fs_client.call(
            "write_file",
            {"path": schematic_path, "content": generated_schematic_content}
        )
        if not write_schematic_result or write_schematic_result.get("error"):
            raise MCPServiceError(f"Filesystem MCP error writing schematic: {write_schematic_result.get('error', 'Unknown error')}")
        print(f"Schematic saved to: {write_schematic_result.get('path')}")

        write_metadata_result = fs_client.call(
            "write_file",
            {"path": metadata_path, "content": generated_metadata_content}
        )
        if not write_metadata_result or write_metadata_result.get("error"):
            raise MCPServiceError(f"Filesystem MCP error writing metadata: {write_metadata_result.get('error', 'Unknown error')}")
        print(f"Metadata saved to: {write_metadata_result.get('path')}")
    except (MCPServiceError, ValueError) as e:
        print(f"Error in Step 3 (Filesystem MCP): {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"An unexpected error occurred in Step 3: {e}", file=sys.stderr)
        return None

    # 4. Commit the design using Git Ledger MCP
    print("Step 4: Committing design to Git ledger (git-ledger)...")
    try:
        git_client = get_mcp_client("git-ledger")
        commit_result = git_client.call(
            "commit_design",
            {
                "design_id": design_id,
                "schematic_path": schematic_path,
                "metadata_path": metadata_path,
                "commit_message": f"AI-generated design: {design_id} for prompt: '{prompt[:50]}...'"
            }
        )
        if not commit_result or commit_result.get("error"):
            raise MCPServiceError(f"Git Ledger MCP error: {commit_result.get('error', 'Unknown error')}")
        print(f"Design committed with hash: {commit_result.get('commit_hash')}")
    except (MCPServiceError, ValueError) as e:
        print(f"Error in Step 4 (Git Ledger MCP): {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"An unexpected error occurred in Step 4: {e}", file=sys.stderr)
        return None

    print(f"Schematic generation for '{design_id}' complete.")
    return {
        "status": "success",
        "design_id": design_id,
        "schematic_path": schematic_path,
        "commit_hash": commit_result.get("commit_hash")
    }

def main():
    parser = argparse.ArgumentParser(
        description="MCP Schematic Generation Orchestrator.",
        formatter_class=argparse.RawTextHelpFormatter # To preserve newlines in help text
    )
    parser.add_argument("--prompt", required=True, help="The prompt for schematic generation.")
    parser.add_argument("--id", required=True, help="Unique ID for the design (e.g., 'city_hub_v1').")
    parser.add_argument("--criteria", required=True, 
                        help="JSON string of location criteria, e.g., '{"terrain_type": "flat", "near_water": true}'.")

    args = parser.parse_args()

    try:
        location_criteria = json.loads(args.criteria)
    except json.JSONDecodeError:
        print("Error: --criteria must be a valid JSON string.", file=sys.stderr)
        sys.exit(1)

    # Ensure the MCP config file exists before proceeding
    if not os.path.exists(MCP_CONFIG_PATH):
        print(f"Error: MCP configuration file '{MCP_CONFIG_PATH}' not found. Please ensure it exists.", file=sys.stderr)
        sys.exit(1)

    try:
        result = orchestrate_schematic_generation(
            prompt=args.prompt,
            design_id=args.id,
            location_criteria=location_criteria
        )
        if result:
            print("
--- Orchestration Summary ---")
            print(json.dumps(result, indent=2))
        else:
            print("
Schematic generation process did not complete successfully.", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        # Catch any unhandled exceptions during orchestration
        print(f"
An unhandled error occurred during orchestration: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    # Example of how to run this script from the command line:
    # python mcp-server/schematic_generator_orchestrator.py --prompt "A futuristic city hub with vertical farms." --id "city_hub_v1" --criteria '{"terrain_type": "flat", "min_size": 100}'
    main()
