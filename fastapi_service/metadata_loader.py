import json
import os

def load_tool_descriptions():
    path = os.path.join(os.path.dirname(__file__), "tool_data", "tools.json")
    with open(path, "r") as file:
        tools = json.load(file)
    return json.dumps(tools, indent=2)
