from pydantic import BaseModel
from typing import List, Dict

class ToolMetadata(BaseModel):
    tool_name: str
    description: str
    parameters: List[str]

class ToolCallRequest(BaseModel):
    tool_name: str
    tool_parameters: Dict

class NaturalLanguageQuery(BaseModel):
    query: str
