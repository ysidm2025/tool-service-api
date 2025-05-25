import pkgutil
import importlib
import inspect

def get_registered_tools():
    tools = []
    for loader, module_name, is_pkg in pkgutil.iter_modules(__path__):
        module = importlib.import_module(f"{__name__}.{module_name}")
        if hasattr(module, "get_registered_tools") and inspect.isfunction(module.get_registered_tools):
            tools.extend(module.get_registered_tools())
    return tools
