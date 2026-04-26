"""Async HTTP client wrapper for Agrasandhani"""

import httpx
from typing import Optional, Dict, Any
from agrasandhani.config import Settings


class HTTPClient:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = httpx.AsyncClient(
            timeout=settings.scan.timeout,
            follow_redirects=settings.scan.follow_redirects,
            headers={"User-Agent": settings.scan.user_agent},
        )

    async def get(self, url: str, **kwargs) -> httpx.Response:
        """Perform GET request."""
        return await self.client.get(url, **kwargs)

    async def post(self, url: str, data: Optional[Dict] = None, **kwargs) -> httpx.Response:
        """Perform POST request."""
        return await self.client.post(url, data=data, **kwargs)

    async def close(self):
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
