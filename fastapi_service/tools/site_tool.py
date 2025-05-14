from tools.tool import function_tool, Tool

@function_tool
class SiteTool(Tool):
    """Helps debug site-related issues like performance or downtime."""

    def run(self, issue: str) -> str:
        return f"Analyzing issue: '{issue}'. Suggest restarting the server (simulated)."