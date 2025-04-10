from .tool import Tool
# from tools.tool import Tool

def function_tool(cls):
    cls.is_function_tool = True
    return cls

@function_tool
class WeatherTool(Tool):
    """
    Fetches weather information for a given city.
    """

    def run(self, city: str, units: str = "metric") -> str:
        return f"Weather in {city} is 22°C in {units} units."
