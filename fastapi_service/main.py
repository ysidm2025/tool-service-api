from fastapi import FastAPI, HTTPException # type: ignore
from typing import List
from .models import ToolMetadata, ToolRequest
from .utils import get_tool_metadata, run_tool

app = FastAPI()

@app.get("/bot_capabilities", response_model=List[ToolMetadata])
def get_capabilities():
    try:
        return get_tool_metadata()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/bot_response")
def bot_response(request: ToolRequest):
    try:
        return run_tool(request.tool_name, request.tool_parameters)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
