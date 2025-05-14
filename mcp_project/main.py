from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from mcp.server.fastmcp import FastMCP
from tool_loader import load_static_tools
from dynamic_loader import create_tool_function
from db import get_db
from sqlalchemy import text
import logging

# Set logging level
logging.basicConfig(level=logging.DEBUG)

# Initialize MCP instance
mcp = FastMCP("Unified Tool Server", stateless_http=True)

# Define application lifespan logic
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Load tools from static sources
    load_static_tools(mcp)
    print(await mcp.list_tools())
    # Load tools dynamically from the database
    try:
        async for db in get_db():
            tools = await db.execute(text("SELECT name, description, code FROM tools"))
            for name, description, code in tools.fetchall():
                print("--------  Tools from databse in raw format -------- ")
                print(f"\nTool from DB:\nName: {name}\nDescription: {description}\nCode:\n{code}\n")
                print("\n--------  Tools from databse in raw format -------- ")
                fn = create_tool_function(name, code)
                mcp.tool(name=name, description=description)(fn)
        print("[Server] All tools loaded from DB.")
    except Exception as e:
        print("[ERROR] Failed to load tools from DB:", e)

    # Print all tools (static + DB-loaded)
    # print("[Server] Full tool list after DB load:", await mcp.list_tools())
    tools = await mcp.list_tools()
    print("[Server] Full tool list after DB load:")
    for tool in tools:
        print(f"  - Name       : {tool.name}")
        print(f"    Description: {tool.description}")
        print(f"    Input Schema:")
        for prop, details in tool.inputSchema.get("properties", {}).items():
            print(f"      - {prop}: {details}")
        print()
    yield  # Startup complete; app is running

# Create FastAPI app with lifespan context
app = FastAPI(lifespan=lifespan)

# Mount MCP's streamable HTTP endpoint
app.mount("/mcp/", mcp.streamable_http_app())
print("MCP server mounted at /mcp/")


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

# ////////////////////////////////////////////////
# from contextlib import asynccontextmanager
# from typing import AsyncGenerator

# from mcp.server.fastmcp import FastMCP
# from tool_loader import load_static_tools
# from dynamic_loader import create_tool_function
# from db import get_db
# from sqlalchemy import text
# import logging

# # Initialize MCP instance
# mcp = FastMCP("Unified Tool Server", stateless_http=True)

# # Define lifespan logic
# @asynccontextmanager
# async def lifespan(server: FastMCP) -> AsyncGenerator[None, None]:
#     load_static_tools(mcp)
#     print(mcp.list_tools())
#     async for db in get_db():
#         tools = await db.execute(text("SELECT name, description, code FROM tools"))
#         for name, description, code in tools.fetchall():
#             fn = create_tool_function(name, code)
#             mcp.tool(name=name, description=description)(fn)

#     print("[Server] All tools loaded from DB.")
#     yield

# # Attach lifespan
# mcp = FastMCP("Unified Tool Server", stateless_http=True, lifespan=lifespan)

# # Set logging
# logging.basicConfig(level=logging.DEBUG)

# # Entry point to run directly or via MCP Inspector
# if __name__ == "__main__":
#     mcp.run()

# //////////////////////////////////////////////////

# import sys
# import asyncio
# from contextlib import asynccontextmanager
# from typing import AsyncGenerator
# from mcp.server.fastmcp import FastMCP
# from tool_loader import load_static_tools
# from dynamic_loader import create_tool_function
# from db import get_db
# from sqlalchemy import text
# import logging

# # Windows fix for asyncio
# if sys.platform.startswith('win'):
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# # Initialize MCP server
# mcp = FastMCP("Unified Tool Server", stateless_http=True)

# # Define async startup (lifespan) logic
# @asynccontextmanager
# async def lifespan(server: FastMCP) -> AsyncGenerator[None, None]:
#     load_static_tools(mcp)
#     print(mcp.list_tools())
#     async for db in get_db():
#         tools = await db.execute(text("SELECT name, description, code FROM tools"))
#         for name, description, code in tools.fetchall():
#             fn = create_tool_function(name, code)
#             mcp.tool(name=name, description=description)(fn)
#     print("[Server] All tools loaded from DB.")
#     yield

# # Attach lifespan to MCP
# mcp.settings.lifespan = lifespan

# # Create ASGI app for uvicorn
# app = mcp.streamable_http_app()

# # Enable debug logs
# logging.basicConfig(level=logging.DEBUG)
