# tools/string_tools.py

_registered_tools = []

def register_tool(fn, name=None, description=None):
    _registered_tools.append({
        "name": name or fn.__name__,
        "description": description or fn.__doc__ or "",
        "fn": fn
    })
    return fn

@register_tool
def reverse_string(text: str) -> str:
    """Reverse a string"""
    return text[::-1]

@register_tool
def uppercase_string(text: str) -> str:
    """Uppercase a string"""
    return text.upper()

def get_registered_tools():
    return _registered_tools
