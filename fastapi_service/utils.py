import inspect
import importlib
import pkgutil
from typing import List, Dict, Any
from .models import ToolMetadata
from .tools.tool import Tool  # Base Tool class

# Ensure tools module is imported
from . import tools  # Import the tools folder

def get_tool_metadata() -> List[ToolMetadata]:
    tool_classes = []

    # Scan the 'tools' package for all classes annotated with 'function_tool'
    for _, module_name, _ in pkgutil.iter_modules(tools.__path__):
        # Dynamically import each module in the 'tools' package
        module = importlib.import_module(f".tools.{module_name}", package="fastapi_service")
        
        # Iterate over all classes in the module
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if hasattr(obj, 'is_function_tool') and getattr(obj, 'is_function_tool', False):
                # Get the parameters of the 'run' method dynamically
                signature = inspect.signature(obj.run)
                param_names = [param.name for param in signature.parameters.values() if param.name != 'self']
                
                # Add the tool's metadata
                tool_classes.append(
                    ToolMetadata(
                        tool_name=name,
                        description=obj.__doc__ or "No description",
                        parameters=param_names
                    )
                )
    return tool_classes

def run_tool(tool_name: str, tool_parameters: Dict[str, Any]) -> Dict[str, Any]:
    # Iterate over all tool classes to find the requested one
    for module in [tools.weather_tool]:  # Add other tool modules here as needed
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if name == tool_name:
                # Create an instance of the tool class and run it with provided parameters
                instance = obj()
                return {"result": instance.run(**tool_parameters)}

    raise ValueError(f"Tool '{tool_name}' not found.")
