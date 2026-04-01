from diagrams import Cluster, Diagram, Edge
from diagrams.generic.device import Tablet
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Internet
from diagrams.onprem.vcs import Github
from diagrams.programming.language import Go, Python

with Diagram("Skynet Unified Brain Architecture", show=False, direction="LR"):
    github = Github("GitHub Repo\n(Technical Ledger)")

    with Cluster("Orchestration Layer (10.10.16.x)"):
        stargate = Server("Stargate MCP\n(NVMe Orchestrator)")
        orchestrator = Python("skynet_unified.py")
        stargate >> orchestrator

    with Cluster("Inference Nexus (Edge Compute)"):
        skynet_node = Server("Skynet Pi 5\n(Hailo-8L NPU)")
        schem_gen = Go("schem-gen")

        edge_t = Server("edge-t (10.10.16.4)\n(Google Edge TPU)")
        vision_mcp = Python("Vision MCP Service")

        skynet_node >> schem_gen
        edge_t >> vision_mcp

    with Cluster("Simulation Engine (10.10.8.60)"):
        chonk = Server("Chonk Server\n(Paper 1.21.1)")
        bluemap = Internet("BlueMap WebApp")
        rcon = Server("RCON Transceiver")

        chonk >> rcon
        chonk >> bluemap

    # Workflow Connections
    orchestrator >> Edge(label="Git MCP") >> github
    orchestrator >> Edge(label="RCON / FS MCP") >> rcon
    orchestrator >> Edge(label="NPU Task") >> skynet_node
    orchestrator >> Edge(label="Vision Audit") >> edge_t

    schem_gen >> Edge(label="Sync Schematics", color="red") >> chonk

    user = Tablet("User / Admin")
    user >> Edge(label="Minecraft Client") >> chonk
    user >> Edge(label="Telemetry Audit") >> bluemap
