import httpx
from typing import List, Dict, Any

MCP_BASE_URL = "http://localhost:9090" # Adjust as per your MCP server address

async def get_mcp_tools() -> List[Dict[str, Any]]:
	async with httpx.AsyncClient() as client:
		response = await client.get(f"{MCP_BASE_URL}/.well-known/ai-plugin.json") # or another discovery endpoint
		response.raise_for_status()
		return response.json()["tools"]

async def call_mcp_tool(tool_name: str, parameters: Dict[str, Any]) -> Any:
	payload = {
		"tool_name": tool_name,
		"tool_parameters": parameters
	}
	async with httpx.AsyncClient() as client:
		response = await client.post(f"{MCP_BASE_URL}/invoke", json=payload)
		response.raise_for_status()
		return response.json()

