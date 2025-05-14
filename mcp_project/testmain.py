import logging
from mcp.server.fastmcp import FastMCP

# Enable logging
logging.basicConfig(level=logging.DEBUG)

# Initialize MCP server
mcp = FastMCP("Test Server", stateless_http=True)

@mcp.tool()
def hello(name: str) -> str:
    return f"Hello, {name}!"

# Expose ASGI app
app = mcp.streamable_http_app()
