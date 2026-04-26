"""Base class for all security checks"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseCheck(ABC):
    """Abstract base class for security checks."""

    name: str = "Base Check"
    category: str = "General"

    @abstractmethod
    async def run(self, target_url: str, client) -> List[Dict[str, Any]]:
        """Run the security check and return list of findings."""
        pass
