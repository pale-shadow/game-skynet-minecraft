from diagrams import Cluster, Diagram, Edge
from diagrams.generic.device import Tablet
from diagrams.onprem.compute import Server

# Changed SQL to Mysql to fix the ImportError
from diagrams.onprem.database import Mysql
from diagrams.onprem.network import Internet
from diagrams.onprem.vcs import Github
from diagrams.programming.language import Go, Python

# Added filename parameter to ensure the output is easy to locate
with Diagram(
    "Skynet Unified Brain Architecture",
    filename="skynet_unified_brain",
    show=False,
    direction="LR",
):

    github = Github("Technical Ledger\n(GitHub Repository)")

    with Cluster("Stargate Command Hub (10.10.16.x)"):
        stargate = Server("Stargate MCP\n(System Orchestrator)")
        # Using Mysql icon for the Hub 07 Vault
        vault = Mysql("Neural-Data Vault\n(Hub 07 Archive)")
        stargate >> vault

    with Cluster("Skynet AI Testing Field (Edge Compute)"):
        skynet_node = Server("Skynet Pi 5\n(Hailo-8L NPU)")
        logic_core = Python("reactive_mutation2.1.py\n(Hub 01)")
        schem_gen = Go("schem-gen\n(Go/Python Pipeline)")

        mono_eye = Server("Mono-Eye Sensor (Hub 06)\n(Edge TPU Vision)")

        # Internal Logic Flow
        skynet_node >> logic_core >> schem_gen
        mono_eye >> Edge(label="Sense/Net Feed") >> logic_core

    with Cluster("Chonk Simulation Engine (10.10.8.60)"):
        chonk = Server("Chonk Server\n(Paper 1.21.1)")
        bluemap = Internet("BlueMap Telemetry\n(Web-App)")
        rcon = Server("Transmission Core\n(Hub 02 RCON)")

        chonk >> rcon
        chonk >> Edge(label="20 TPS Mapping") >> bluemap

    # Distributed Workflow Connections
    logic_core >> Edge(label="Commit World State") >> github
    logic_core >> Edge(label="RCON / FS MCP") >> rcon
    logic_core >> Edge(label="Hailo-8L NPU Decoding") >> skynet_node

    schem_gen >> Edge(label="Sync .schem Files", color="red") >> chonk

    user = Tablet("Admin Controller")
    user >> Edge(label="Minecraft Client") >> chonk
    user >> Edge(label="Spark Profiler Audit") >> bluemap
