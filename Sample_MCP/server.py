import random
import asyncio
import uvicorn
import requests
import threading
from mcp.server.fastmcp import FastMCP
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from mcp.server.fastmcp import FastMCP

# Create server
mcp = FastMCP("Echo Server", stateless_http=True)

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    print(f"[debug-server] add({a}, {b})")
    return a + b

@mcp.tool()
def get_secret_word() -> str:
    print("[debug-server] get_secret_word()")
    return random.choice(["apple", "banana", "cherry"])

@mcp.tool()
def get_current_weather(city: str) -> str:
    print(f"[debug-server] get_current_weather({city})")

    endpoint = "https://wttr.in"
    response = requests.get(f"{endpoint}/{city}")
    return response.text

# # Create FastAPI app
# app = FastAPI()

# # Add a GET endpoint to return all tools
# @app.get("/tools")
# async def list_tools():
#     tools = await mcp.list_tools()
#     return JSONResponse([
#         {
#             "name": tool.name,
#             "description": tool.description,
#             "input_schema": tool.inputSchema,
#         }
#         for tool in tools
#     ])

# def start_fastapi():
#     uvicorn.run(app, host="127.0.0.1", port=9000)

if __name__ == "__main__":
    mcp.run(transport="sse")


    # async def print_tools():
    #     tools = await mcp.list_tools()
    #     for tool in tools:
    #         print(f"Tool name: {tool.name}")
    #         print(f"Description: {tool.description}")
    #         print(f"Input schema: {tool.inputSchema}")
    #         print("-" * 40)

    # asyncio.run(print_tools())
    # mcp.run(transport="sse")

    # Start FastAPI on a separate thread
    # threading.Thread(target=start_fastapi, daemon=True).start()

# import random
# import requests
# from fastapi import FastAPI, Request
# from fastapi.responses import JSONResponse
# from mcp.server.fastmcp import FastMCP

# mcp = FastMCP("Echo Server", stateless_http=True)

# @mcp.tool()
# def add(a: int, b: int) -> int:
#     return a + b

# @mcp.tool()
# def get_secret_word() -> str:
#     return random.choice(["apple", "banana", "cherry"])

# @mcp.tool()
# def get_current_weather(city: str) -> str:
#     response = requests.get(f"https://wttr.in/{city}?format=3")
#     return response.text

# app = FastAPI()

# app.mount("/", mcp.streamable_http_app())

# @app.get("/tools")
# async def list_tools():
#     tools = await mcp.list_tools()
#     return JSONResponse([
#         {
#             "name": tool.name,
#             "description": tool.description,
#             "input_schema": tool.inputSchema,
#         }
#         for tool in tools
#     ])

# # ////////////////////////////
# # import asyncio

# # if __name__ == "__main__":
# #     async def print_tools():
# #         tools = await mcp.list_tools()
# #         for tool in tools:
# #             print(f"Tool name: {tool.name}")
# #             print(f"Description: {tool.description}")
# #             print(f"Input schema: {tool.inputSchema}")
# #             print("-" * 40)

# #     asyncio.run(print_tools())

# #     mcp.run(transport="sse")
#     # ////////////////////////////

# # Step 5: Run the app
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)