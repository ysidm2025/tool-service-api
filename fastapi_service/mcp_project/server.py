# from fastapi import FastAPI
# from contextlib import asynccontextmanager
# from typing import AsyncGenerator

# from mcp.server.fastmcp import FastMCP
# from tool_loader import load_static_tools
# from dynamic_loader import create_tool_function
# from db import get_db
# from sqlalchemy import text
# import logging
# import asyncio

# # Set logging level
# logging.basicConfig(level=logging.DEBUG)

# # Initialize MCP instance
# mcp = FastMCP("Unified Tool Server", stateless_http=True)

# # Define application lifespan logic
# @asynccontextmanager
# async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
#     # Load tools from static sources
#     load_static_tools(mcp)
#     print(await mcp.list_tools())
#     # Load tools dynamically from the database
#     try:
#         async for db in get_db():
#             tools = await db.execute(text("SELECT name, description, code FROM tools"))
#             for name, description, code in tools.fetchall():
#                 print("--------  Tools from databse in raw format -------- ")
#                 print(f"\nTool from DB:\nName: {name}\nDescription: {description}\nCode:\n{code}\n")
#                 print("\n--------  Tools from databse in raw format -------- ")
#                 fn = create_tool_function(name, code)
#                 mcp.tool(name=name, description=description)(fn)
#         print("[Server] All tools loaded from DB.")
#     except Exception as e:
#         print("[ERROR] Failed to load tools from DB:", e)

#     # Print all tools (static + DB-loaded)
#     # print("[Server] Full tool list after DB load:", await mcp.list_tools())
#     tools = await mcp.list_tools()
#     print("[Server] Full tool list after DB load:")
#     for tool in tools:
#         print(f"  - Name       : {tool.name}")
#         print(f"    Description: {tool.description}")
#         print(f"    Input Schema:")
#         for prop, details in tool.inputSchema.get("properties", {}).items():
#             print(f"      - {prop}: {details}")
#         print()
#     yield  # Startup complete; app is running

# # Create FastAPI app with lifespan context
# app = FastAPI(lifespan=lifespan)

# # Mount MCP's streamable HTTP endpoint
# app.mount("/mcp/", mcp.streamable_http_app())
# print("MCP server mounted at /mcp/")

# ///////////////////////////////////////////////////////////////////

# import logging
# import anyio
# import random
# import requests
# from mcp.server.fastmcp import FastMCP
# from sqlalchemy import text
# from tool_loader import load_static_tools
# from dynamic_loader import create_tool_function
# from db import get_db

# # Setup logging
# logging.basicConfig(level=logging.DEBUG)

# # Initialize MCP instance
# mcp = FastMCP("Unified Tool Server", stateless_http=True)

# # Load static tools
# load_static_tools(mcp)

# # Define async startup hook to load dynamic tools
# async def on_startup():
#     print("[Startup] Loading dynamic tools from DB...")

#     try:
#         async for db in get_db():
#             tools = await db.execute(text("SELECT name, description, code FROM tools"))
#             for name, description, code in tools.fetchall():
#                 print(f"[DB] Registering tool: {name}")
#                 fn = create_tool_function(name, code)
#                 mcp.tool(name=name, description=description)(fn)
#         print("[Startup] All DB tools loaded.")
#     except Exception as e:
#         print(f"[ERROR] Failed to load DB tools: {e}")

#     tools = await mcp.list_tools()
#     print("[Startup] Available tools:")
#     for tool in tools:
#         print(f"  - {tool.name}: {tool.description}")
#         if tool.inputSchema:
#             print("    Input schema:")
#             for prop, details in tool.inputSchema.get("properties", {}).items():
#                 print(f"      - {prop}: {details}")
#         print()

# on_startup()
# # Start the SSE server with a custom startup coroutine
# if __name__ == "__main__":
#     anyio.run(on_startup)
#     mcp.run(transport="sse")

# ///////////////////////////////////////////////////////////////////////

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
mcp = FastMCP("Unified Tool Server", stateless_http=True)

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
