from fastapi import FastAPI, HTTPException
from models import ToolCallRequest, NaturalLanguageQuery
# from utils import get_tool_metadata, run_tool
from agent_sdk import answer_with_tools
# from mcp_client import get_mcp_tools, call_mcp_tool
import httpx
from utils import get_tool_metadata_from_mcp

app = FastAPI()

# @app.get("/bot_capabilities")
# def bot_capabilities():
#     return get_tool_metadata()

# @app.post("/bot_response")
# def bot_response(request: ToolCallRequest):
#     try:
#         print(f"Received request: {request}")  # Debugging line
#         return run_tool(request.tool_name, request.tool_parameters)
#     except ValueError as e:
#         raise HTTPException(status_code=404, detail=str(e))
#     except TypeError as e:
#         raise HTTPException(status_code=400, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@app.get("/bot_capabilities")
def bot_capabilities():
    return get_tool_metadata_from_mcp()

@app.post("/ask_agent")
def ask_agent(request: NaturalLanguageQuery):
    try:
        print(f"Received query: {request.query}")  # Debugging line
        answer = answer_with_tools(request.query)  # Check if this works as expected
        print(f"Answer from tools: {answer}")  # Debugging line
        return {"answer": answer}
    except Exception as e:
        print(f"Error in ask_agent: {e}")  # Debugging line
        raise HTTPException(status_code=500, detail=str(e))

# from fastapi import FastAPI, HTTPException
# from openai import OpenAI  # new SDK usage
# from typing import List
# import httpx
# import os
# from dotenv import load_dotenv # type: ignore

# app = FastAPI()

# # Constants for the MCP server
# MCP_SERVER_URL = "http://localhost:9090"

# load_dotenv()
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# # Function to get tools from MCP
# async def get_tools_from_mcp() -> List[dict]:
#     """Fetch available tools from MCP."""
#     async with httpx.AsyncClient() as http_client:
#         response = await http_client.get(f"{MCP_SERVER_URL}/tools")
#         response.raise_for_status()
#         return response.json()

# # Function to call OpenAI Chat Completions API
# async def ask_openai_agent(query: str, tools: List[dict]) -> str:
#     """Use OpenAI Agent SDK to get an answer for the user query."""
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": f"Answer the query: '{query}' using the following tools: {tools} dont just run tool give answer in your own language."}
#         ],
#         max_tokens=100
#     )
#     return response.choices[0].message.content.strip()

# @app.post("/ask_agent")
# async def ask_agent(query: str):
#     """Endpoint to ask the OpenAI Agent."""
#     try:
#         tools = await get_tools_from_mcp()
        
#         # Debug output: print tools to console or logs
#         print(f"[DEBUG] Tools received from MCP: {tools}")
        
#         if not tools:
#             return {"message": "No tools available from MCP."}
        
#         answer = await ask_openai_agent(query, tools)
#         return {"answer": answer}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

