# tools/math_tools.py
_registered_tools = []

def register_tool(fn, name=None, description=None):
    _registered_tools.append({
        "name": name or fn.__name__,
        "description": description or fn.__doc__ or "",
        "fn": fn
    })
    return fn

@register_tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@register_tool
def multiply(x: int, y: int) -> int:
    """Multiply two numbers"""
    return x * y

def get_registered_tools():
    return _registered_tools
