from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from agents import Agent, Runner, gen_trace_id, trace
# from agents.mcp import MCPServerSse , MCPServerStreamableHttp
from agents.mcp import MCPServerSse 
from agents.model_settings import ModelSettings
from typing import Dict, Any
import os
import httpx

load_dotenv()

app = FastAPI()
MCP_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000/sse")

class QueryRequest(BaseModel):
    query: str

class ToolCallRequest(BaseModel):
    tool_name: str
    parameters: Dict[str, Any]

async def run_agent_query(query: str) -> str:
    async with MCPServerSse(
        name="SSE Python Agent",
        params={"url": MCP_URL}
    ) as server:
        trace_id = gen_trace_id()
        with trace(workflow_name="FastAPI Agent", trace_id=trace_id):
            agent = Agent(
                name="Assistant",
                instructions="Use tools to answer the questions. and mention the tool name in the answer in the end format it as 'Tool: <tool_name>'",
                mcp_servers=[server],
                model_settings=ModelSettings(tool_choice="required"),
            )
            result = await Runner.run(starting_agent=agent, input=query)
            return result.final_output

@app.post("/ask_bot")
async def ask_agent(request: QueryRequest):
    try:
        answer = await run_agent_query(request.query)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/bot_capabilities")
async def bot_capabilities():
    try:
        async with MCPServerSse(
            name="SSE Tool Discovery",
            params={"url": MCP_URL}
        ) as server:
            tools = await server.list_tools()

            return [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.inputSchema or {}
                }
                for tool in tools
            ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch tools: {e}")

@app.post("/bot_response")
async def bot_response(request: ToolCallRequest):
    try:
        async with MCPServerSse(name="SSE Runner", params={"url": MCP_URL}) as server:
            # Create a temporary tool call message as if it were coming from the user
            message = f"Call tool {request.tool_name} with {request.parameters}"

            trace_id = gen_trace_id()
            with trace(workflow_name="Direct Tool Run", trace_id=trace_id):
                agent = Agent(
                    name="DirectToolCaller",
                    instructions="Call the tool as requested directly.",
                    mcp_servers=[server],
                    model_settings=ModelSettings(tool_choice="required"),
                )

                # Send the synthetic message through the Agent pipeline
                result = await Runner.run(starting_agent=agent, input=message)
                return {"result": result.final_output}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to run tool: {e}")
    
# @app.post("/bot_response")
# async def bot_response(request: ToolCallRequest):
#     try:
#         async with httpx.AsyncClient(timeout=15.0) as client:
#             response = await client.post(
#                 MCP_URL,
#                 json={
#                     "method": "tools/call",
#                     "params": {
#                         "name": request.tool_name,
#                         "arguments": request.parameters
#                     }
#                 }
#             )
#             response.raise_for_status()
#             return response.json()
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to call tool: {e}")
