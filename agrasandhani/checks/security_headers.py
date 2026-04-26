"""Security Headers Check - Maps to Security Misconfiguration (Top 10)"""

from typing import List, Dict, Any
from agrasandhani.checks.base import BaseCheck


class SecurityHeadersCheck(BaseCheck):
    name = "Security Headers Check"
    category = "Security Misconfiguration"

    async def run(self, target_url: str, client) -> List[Dict[str, Any]]:
        findings = []
        try:
            response = await client.get(target_url)
            headers = response.headers

            security_headers = {
                "Content-Security-Policy": "Missing Content-Security-Policy header",
                "X-Frame-Options": "Missing X-Frame-Options header (Clickjacking protection)",
                "X-Content-Type-Options": "Missing X-Content-Type-Options header",
                "Strict-Transport-Security": "Missing HSTS header",
            }

            for header, message in security_headers.items():
                if header not in headers:
                    findings.append({
                        "title": message,
                        "severity": "Medium",
                        "description": f"Recommended security header '{header}' is missing.",
                        "remediation": f"Add the {header} header to your web server configuration."
                    })

        except Exception as e:
            findings.append({
                "title": "Header Check Failed",
                "severity": "Low",
                "description": str(e)
            })

        return findings
