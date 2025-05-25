import os
import asyncio
from agents import Agent, Runner, gen_trace_id, trace
from agents.mcp import MCPServerSse
from agents.model_settings import ModelSettings
from dotenv import load_dotenv

load_dotenv()

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class OpenAIAgentClient:
    def __init__(self, mcp_url: str):
        self.mcp_url = mcp_url
        self.mcp_server = None

    async def __aenter__(self):
        # Create MCP SSE client connected to your MCP SSE server URL
        self.mcp_server = await MCPServerSse.create(
            name="FastAPI MCP Client",
            params={"url": self.mcp_url},
        )
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.mcp_server.aclose()

    async def discover_tools(self):
        tools = await self.mcp_server.list_tools()
        return tools

    async def run_agent(self, query: str):
        agent = Agent(
            name="Assistant",
            instructions="Use the tools to answer the questions.",
            mcp_servers=[self.mcp_server],
            model_settings=ModelSettings(tool_choice="required"),
        )

        trace_id = gen_trace_id()
        with trace(workflow_name="User Query", trace_id=trace_id):
            result = await Runner.run(starting_agent=agent, input=query)
        return result.final_output
