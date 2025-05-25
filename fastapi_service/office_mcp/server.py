from mcp.server.fastmcp import FastMCP
from tools.property_tools import  register_property_tools

# Create MCP Server
mcp = FastMCP("Property_Information", stateless_http=True)

# Register tools dynamically
register_property_tools(mcp)

# Run the server using SSE
if __name__ == "__main__":
    mcp.run(transport="sse")
    # mcp.run(transport="streamable-http")
