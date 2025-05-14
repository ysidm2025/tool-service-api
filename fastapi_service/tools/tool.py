from abc import ABC, abstractmethod
from typing import Any

class Tool(ABC):
    @abstractmethod
    def run(self, **kwargs: Any) -> str:
        pass

def function_tool(cls):
    cls.is_function_tool = True
    return cls