import ast
from types import FunctionType

# def create_tool_function(name: str, code: str) -> FunctionType:
#     # Wrap the body into a function definition
#     source = f"def {name}(**kwargs):\n"
#     for line in code.splitlines():
#         source += f"    {line}\n"
#     local_vars = {}
#     exec(source, {}, local_vars)
#     return local_vars[name]

def create_tool_function(name: str, code: str):
    """
    Executes user-defined function code from DB and wraps it
    to be MCP-compatible. Handles {'kwargs': value} input format.
    """
    local_vars = {}

    # Execute user-defined code (e.g., def chat(query): ...)
    exec(code, {}, local_vars)

    # Extract first callable function defined
    user_fn = next((v for v in local_vars.values() if callable(v)), None)

    if not user_fn:
        raise ValueError("No callable found in provided code.")

    # Wrapper to handle {'kwargs': "something"} style input
    def wrapper(**kwargs):
        # If kwargs contains 'kwargs' as string → wrap into expected arg
        if "kwargs" in kwargs:
            val = kwargs["kwargs"]
            if isinstance(val, str):
                # Example: chat(query=val)
                return user_fn(query=val)
            elif isinstance(val, dict):
                # Example: chat(**val)
                return user_fn(**val)
        # If passed normally
        return user_fn(**kwargs)

    return wrapper
