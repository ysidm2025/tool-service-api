import importlib
import inspect
import pkgutil
from typing import List, Dict, Any
from models import ToolMetadata
from tools import __path__ as tools_path
from decorators import function_tool
from tools.tool import Tool
import os

# def load_tools() -> list:  # Use list instead of List
#     tools = []
#     for _, module_name, _ in pkgutil.iter_modules(tools_path):
#         try:
#             module = importlib.import_module(f"tools.{module_name}")
#             for name, obj in inspect.getmembers(module, inspect.isclass):
#                 if getattr(obj, "is_function_tool", False):  # Check if the class is a function tool
#                     tools.append(obj)
#         except Exception as e:
#             print(f"Error loading module {module_name}: {e}")
#             continue
#     return tools

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

# def get_tool_metadata() -> list:  # Avoid using List here, use plain list
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

def get_tool_metadata() -> List[Dict[str, Any]]:
    tools = load_tools()
    metadata = []

    print(f"Loaded tools: {tools}")  # Debugging line

    for tool in tools:
        try:
            run_signature = inspect.signature(tool.run)
            parameters = list(run_signature.parameters.keys())[1:]  # skip 'self'
            metadata.append({
                "tool_name": tool.__name__,
                "description": tool.__doc__ or "No description provided.",
                "parameters": parameters
            })
            print(f"Tool metadata: {metadata[-1]}")  # Debugging line
        except Exception as e:
            print(f"Error processing tool {tool.__name__}: {e}")
            continue
    return metadata

# def get_tool_instances() -> list:  # Avoid using List here as well
#     tools = load_tools()
#     instances = []

#     for tool in tools:
#         try:
#             run_signature = inspect.signature(tool.run)
#             parameters = list(run_signature.parameters.keys())[1:]
#             instance = tool()  # Create an instance of the tool
#             instances.append({
#                 "tool_name": tool.__name__,
#                 "description": tool.__doc__ or "No description provided.",
#                 "parameters": parameters,
#                 "function": instance.run  # Link the function that can be called
#             })
#         except Exception as e:
#             print(f"Error instantiating tool {tool.__name__}: {e}")
#             continue
#     return instances

def get_tool_instances() -> Dict[str, Dict[str, Any]]:
    tools = load_tools()
    instances = {}

    for tool in tools:
        try:
            run_signature = inspect.signature(tool.run)
            parameters = list(run_signature.parameters.keys())[1:]
            instance = tool()  # Create an instance of the tool
            instances[tool.__name__] = {
                "tool_name": tool.__name__,
                "description": tool.__doc__ or "No description provided.",
                "parameters": parameters,
                "function": instance.run  # Link the function that can be called
            }
        except Exception as e:
            print(f"Error instantiating tool {tool.__name__}: {e}")
            continue
    return instances

# def run_tool(tool_name: str, tool_parameters: dict) -> Any:  # Change Dict[str, Any] to dict
#     tools = load_tools()
#     for tool in tools:
#         if tool.__name__ == tool_name:
#             try:
#                 instance = tool()  # Ensure the tool is properly instantiated
#                 return instance.run(**tool_parameters)  # pass the parameters to the tool
#             except Exception as e:
#                 raise RuntimeError(f"Error running tool '{tool_name}': {e}")
#     raise ValueError(f"Tool '{tool_name}' not found.")

# def run_tool(tool_name: str, tool_parameters: dict) -> Any:
#     tools = load_tools()
#     print(f"Loaded tools: {tools}")  # Debugging line
#     for tool in tools:
#         print(f"Checking tool: {tool.__name__}")  # Debugging line
#         if tool.__name__ == tool_name:
#             try:
#                 instance = tool()  # Instantiate the tool
#                 print(f"Running tool {tool_name} with params {tool_parameters}")  # Debugging line
#                 return instance.run(**tool_parameters)  # Call the 'run' method
#             except Exception as e:
#                 print(f"Error running tool: {e}")  # Debugging line
#                 raise RuntimeError(f"Error running tool '{tool_name}': {e}")
#     raise ValueError(f"Tool '{tool_name}' not found.")
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