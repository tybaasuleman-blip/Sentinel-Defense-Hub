from fastmcp import FastMCP
from .services.detector import analyze_frame

# Create the MCP Server
mcp = FastMCP("Sentinel_Agent")

@mcp.tool()
def monitor_location(location_name: str, image_file: str):
    """Checks a specific location in Palestine for anomalies or movement."""
    result = analyze_frame(image_file)
    return f"Report for {location_name}: {result}"

if __name__ == "__main__":
    mcp.run()