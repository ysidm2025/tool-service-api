import logging
import random
import requests
from mcp.server.fastmcp import FastMCP
from sqlalchemy import text
from loaders.tool_loader import load_static_tools
from loaders.dynamic_loader import create_tool_function
from db import get_db
import anyio

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Initialize MCP instance
mcp = FastMCP("Unified Tool Server", stateless_http=True, port=9090)

# Load static tools
load_static_tools(mcp)

# New: Sync wrapper to run async DB loading before starting server
def load_db_tools_sync():
    async def inner():
        print("[Startup] Loading dynamic tools from DB...")
        try:
            async for db in get_db():
                tools = await db.execute(text("SELECT name, description, code FROM tools"))
                for name, description, code in tools.fetchall():
                    print(f"[DB] Registering tool: {name}")
                    fn = create_tool_function(name, code)
                    mcp.tool(name=name, description=description)(fn)
            print("[Startup] All DB tools loaded.")
        except Exception as e:
            print(f"[ERROR] Failed to load DB tools: {e}")

        tools = await mcp.list_tools()
        print("[Startup] Available tools:")
        for tool in tools:
            print(f"  - {tool.name}: {tool.description}")
            if tool.inputSchema:
                print("    Input schema:")
                for prop, details in tool.inputSchema.get("properties", {}).items():
                    print(f"      - {prop}: {details}")
            print()
    anyio.run(inner)

load_db_tools_sync()

if __name__ == "__main__":
    mcp.run(transport="sse")
