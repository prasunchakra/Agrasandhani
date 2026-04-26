"""Configuration management for Agrasandhani"""

from pathlib import Path
from typing import Optional
import yaml
from pydantic import BaseModel, Field


class ScanConfig(BaseModel):
    """Scan related configuration."""
    timeout: int = Field(default=30, description="Request timeout in seconds")
    max_depth: int = Field(default=2, description="Maximum crawl depth")
    follow_redirects: bool = Field(default=True)
    user_agent: str = Field(
        default="Agrasandhani/0.1 (+https://github.com/yourusername/agrasandhani)"
    )


class Settings(BaseModel):
    """Main application settings."""
    scan: ScanConfig = Field(default_factory=ScanConfig)
    verbose: bool = False

    @classmethod
    def load(cls, config_path: Optional[str] = None) -> "Settings":
        """Load settings from YAML file or return defaults."""
        if config_path and Path(config_path).exists():
            with open(config_path, "r") as f:
                data = yaml.safe_load(f) or {}
            return cls(**data)
        return cls()
