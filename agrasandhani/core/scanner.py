"""Core Scanner class for Agrasandhani"""

from typing import Dict, Any
from agrasandhani.config import Settings
from agrasandhani.core.http_client import HTTPClient


class Scanner:
    def __init__(self, target_url: str, settings: Settings, verbose: bool = False):
        self.target_url = target_url.rstrip("/")
        self.settings = settings
        self.verbose = verbose
        self.findings: Dict[str, list] = {}

    async def _basic_recon(self, client: HTTPClient):
        """Basic reconnaissance."""
        try:
            response = await client.get(self.target_url)
            if response.status_code == 200:
                self.findings.setdefault("Information Gathering", []).append({
                    "title": "Homepage accessible",
                    "severity": "Info",
                    "description": f"Target responded with status code {response.status_code}"
                })
        except Exception as e:
            self.findings.setdefault("Errors", []).append({
                "title": "Connection Error",
                "severity": "High",
                "description": str(e)
            })

    def run(self) -> Dict[str, Any]:
        """Run the scan (synchronous wrapper for now)."""
        import asyncio

        async def _run():
            async with HTTPClient(self.settings) as client:
                await self._basic_recon(client)
                # TODO: Add more checks here (Security Headers, Misconfiguration, etc.)

        asyncio.run(_run())

        return {
            "target": self.target_url,
            "findings": self.findings,
            "summary": {
                "total_findings": sum(len(v) for v in self.findings.values())
            }
        }
