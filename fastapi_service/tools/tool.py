from abc import ABC, abstractmethod
from typing import Any

class Tool(ABC):
    @abstractmethod
    def run(self, **kwargs: Any) -> str:
        """Each tool must implement the run method."""
        pass
