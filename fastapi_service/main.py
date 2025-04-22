from fastapi import FastAPI, HTTPException
from models import ToolCallRequest, NaturalLanguageQuery
from utils import get_tool_metadata, run_tool
from agent_sdk import answer_with_tools

app = FastAPI()

@app.get("/bot_capabilities")
def bot_capabilities():
    return get_tool_metadata()

@app.post("/bot_response")
def bot_response(request: ToolCallRequest):
    try:
        print(f"Received request: {request}")  # Debugging line
        return run_tool(request.tool_name, request.tool_parameters)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except TypeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @app.post("/ask_agent")
# def ask_agent(request: NaturalLanguageQuery):
#     try:
#         return {"answer": answer_with_tools(request.query)}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

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
