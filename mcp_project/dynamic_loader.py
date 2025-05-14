import ast
from types import FunctionType

def create_tool_function(name: str, code: str) -> FunctionType:
    # Wrap the body into a function definition
    source = f"def {name}(**kwargs):\n"
    for line in code.splitlines():
        source += f"    {line}\n"
    local_vars = {}
    exec(source, {}, local_vars)
    return local_vars[name]
