# from tools.math_tools import get_registered_tools as get_math_tools
# from tools.string_tools import get_registered_tools as get_string_tools

# def load_static_tools(mcp):
#     for tool in get_math_tools() + get_string_tools():
#         mcp.tool(name=tool["name"], description=tool["description"])(tool["fn"])

from tools import get_registered_tools

def load_static_tools(mcp):
    for tool in get_registered_tools():
        mcp.tool(name=tool["name"], description=tool["description"])(tool["fn"])
        print(f"Loaded tool: {tool['name']}")

