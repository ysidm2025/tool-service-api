from tools.tool import function_tool, Tool

@function_tool
class WeatherTool(Tool):
    """Fetches weather information for a given city."""

    def run(self, city: str, units: str = "metric") -> str:
        return f"Weather in {city} is 15°C (simulated)"
