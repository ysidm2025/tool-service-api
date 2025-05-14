import importlib
import inspect
import pkgutil
from typing import List, Dict, Any
from models import ToolMetadata
from tools import __path__ as tools_path
from decorators import function_tool
from tools.tool import Tool
import os

def load_tools() -> List[type]:
    tools = []
    for _, module_name, _ in pkgutil.iter_modules(tools_path):
        try:
            module = importlib.import_module(f"tools.{module_name}")
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if getattr(obj, "is_function_tool", False):
                    tools.append(obj)
                    print(f"Loaded tool: {obj.__name__}")  # Debugging line
        except Exception as e:
            print(f"Error loading module {module_name}: {e}")
            continue
    return tools


# def get_tool_metadata() -> List[Dict[str, Any]]:
#     tools = load_tools()
#     metadata = []

#     print(f"Loaded tools: {tools}")  # Debugging line

#     for tool in tools:
#         try:
#             run_signature = inspect.signature(tool.run)
#             parameters = list(run_signature.parameters.keys())[1:]  # skip 'self'
#             metadata.append({
#                 "tool_name": tool.__name__,
#                 "description": tool.__doc__ or "No description provided.",
#                 "parameters": parameters
#             })
#             print(f"Tool metadata: {metadata[-1]}")  # Debugging line
#         except Exception as e:
#             print(f"Error processing tool {tool.__name__}: {e}")
#             continue
#     return metadata


# def get_tool_instances() -> Dict[str, Dict[str, Any]]:
#     tools = load_tools()
#     instances = {}

#     for tool in tools:
#         try:
#             run_signature = inspect.signature(tool.run)
#             parameters = list(run_signature.parameters.keys())[1:]
#             instance = tool()  # Create an instance of the tool
#             instances[tool.__name__] = {
#                 "tool_name": tool.__name__,
#                 "description": tool.__doc__ or "No description provided.",
#                 "parameters": parameters,
#                 "function": instance.run  # Link the function that can be called
#             }
#         except Exception as e:
#             print(f"Error instantiating tool {tool.__name__}: {e}")
#             continue
#     return instances

import requests
import os

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000/mcp/")

import os
import asyncio
from typing import List, Dict, Any
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000/mcp/")

def get_tool_metadata_from_mcp() -> List[Dict[str, Any]]:
    async def _get_tools():
        async with streamablehttp_client(MCP_SERVER_URL) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = await session.list_tools()
                return [
                    {
                        "tool_name": tool.name,
                        "description": tool.description or "",
                        "parameters": list(tool.schema.get("parameters", {}).get("properties", {}).keys())
                    }
                    for tool in tools
                ]

    return asyncio.run(_get_tools())

def call_mcp_tool(tool_name: str, arguments: dict) -> str:
    async def _call():
        async with streamablehttp_client(MCP_SERVER_URL) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool(tool_name, arguments)
                return result

    return asyncio.run(_call())


def run_tool(tool_name: str, tool_parameters: Dict[str, Any]) -> Any:
    tools = load_tools()
    print(f"Loaded tools in run_tool: {tools}")  # Debugging line

    for tool in tools:
        print(f"Checking tool: {tool.__name__}")  # Debugging line
        if tool.__name__ == tool_name:
            try:
                instance = tool()  # Instantiate the tool
                print(f"Running tool {tool_name} with params {tool_parameters}")  # Debugging line
                return instance.run(**tool_parameters)  # Call the 'run' method
            except Exception as e:
                print(f"Error running tool: {e}")  # Debugging line
                raise RuntimeError(f"Error running tool '{tool_name}': {e}")
    raise ValueError(f"Tool '{tool_name}' not found.")