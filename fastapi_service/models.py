from pydantic import BaseModel # type: ignore
from typing import List, Dict, Any

class ToolMetadata(BaseModel):
    tool_name: str
    description: str
    parameters: List[str]

class ToolRequest(BaseModel):
    tool_name: str
    tool_parameters: Dict[str, Any]
