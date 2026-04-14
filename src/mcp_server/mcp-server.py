from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Stargate-Utility")

@mcp.tool()
async def get_system_load() -> str:
    """Returns the current system load average."""
    import os
    return str(os.getloadavg())

if __name__ == "__main__":
    mcp.run(transport='stdio')
