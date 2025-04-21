import importlib
import inspect
import pkgutil
from typing import List, Dict, Any
from models import ToolMetadata
from tools import __path__ as tools_path
from decorators import function_tool
from tools.tool import Tool
import os
# def load_tools() -> List[type]:
#     tools = []
#     for _, module_name, _ in pkgutil.iter_modules(tools_path):
#         try:
#             module = importlib.import_module(f"tools.{module_name}")
#             for name, obj in inspect.getmembers(module, inspect.isclass):
#                 if getattr(obj, "is_function_tool", False):
#                     tools.append(obj)
#         except Exception as e:
#             print(f"Error loading module {module_name}: {e}")
#             continue
#     return tools


# def get_tool_metadata() -> List[Dict[str, Any]]:
#     tools = load_tools()
#     metadata = []

#     for tool in tools:
#         try:
#             run_signature = inspect.signature(tool.run)
#             parameters = list(run_signature.parameters.keys())[1:]  # skip 'self'
#             metadata.append({
#                 "tool_name": tool.__name__,
#                 "description": tool.__doc__ or "No description provided.",
#                 "parameters": parameters
#             })
#         except Exception as e:
#             print(f"Error processing tool {tool.__name__}: {e}")
#             continue
#     return metadata


# def get_tool_instances() -> List[Dict[str, Any]]:
#     tools = load_tools()
#     instances = []

#     for tool in tools:
#         try:
#             run_signature = inspect.signature(tool.run)
#             parameters = list(run_signature.parameters.keys())[1:]
#             instance = tool()
#             instances.append({
#                 "tool_name": tool.__name__,
#                 "description": tool.__doc__ or "No description provided.",
#                 "parameters": parameters,
#                 "function": instance.run
#             })
#         except Exception as e:
#             print(f"Error instantiating tool {tool.__name__}: {e}")
#             continue
#     return instances


# def run_tool(tool_name: str, tool_parameters: Dict[str, Any]) -> Any:
#     tools = load_tools()
#     for tool in tools:
#         if tool.__name__ == tool_name:
#             try:
#                 instance = tool()
#                 return instance.run(**tool_parameters)
#             except Exception as e:
#                 raise RuntimeError(f"Error running tool '{tool_name}': {e}")
#     raise ValueError(f"Tool '{tool_name}' not found.")


def load_tools() -> list[type]:
    tools = []
    for _, module_name, _ in pkgutil.iter_modules(tools_path):
        try:
            module = importlib.import_module(f"tools.{module_name}")
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if getattr(obj, "is_function_tool", False):
                    tools.append(obj)
        except Exception as e:
            print(f"Error loading module {module_name}: {e}")
            continue
    return tools


def get_tool_metadata() -> list[dict[str, Any]]:
    tools = load_tools()
    metadata = []

    for tool in tools:
        try:
            run_signature = inspect.signature(tool.run)
            parameters = list(run_signature.parameters.keys())[1:]  # skip 'self'
            metadata.append({
                "tool_name": tool.__name__,
                "description": tool.__doc__ or "No description provided.",
                "parameters": parameters
            })
        except Exception as e:
            print(f"Error processing tool {tool.__name__}: {e}")
            continue
    return metadata


def get_tool_instances() -> list[Tool]:
    tools = load_tools()
    instances = []

    for tool in tools:
        try:
            run_signature = inspect.signature(tool.run)
            parameters = list(run_signature.parameters.keys())[1:]
            instance = tool()
            instances.append({
                "tool_name": tool.__name__,
                "description": tool.__doc__ or "No description provided.",
                "parameters": parameters,
                "function": instance.run
            })
        except Exception as e:
            print(f"Error instantiating tool {tool.__name__}: {e}")
            continue
    return instances


def run_tool(tool_name: str, tool_parameters: dict[str, Any]) -> Any:
    tools = load_tools()
    for tool in tools:
        if tool.__name__ == tool_name:
            try:
                instance = tool()
                return instance.run(**tool_parameters)
            except Exception as e:
                raise RuntimeError(f"Error running tool '{tool_name}': {e}")
    raise ValueError(f"Tool '{tool_name}' not found.")