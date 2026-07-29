"""
configuração global.
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional

DEFAULT_CONFIG: Dict[str, Any] = {
    "app_name": "Smart Terminal AI Search",
    "version": "1.0.0",
    "author": "Python dev",
    "paths": {
        "logs": "logs",
        "cache": "cache",
        "data": "data",
        "assets": "assets",
        "plugins": "plugins"
    },
    "browser": {
        "headless": True,
        "timeout": 15000,
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "viewport": {"width": 1920, "height": 1080},
        "locale": "pt-BR"
    },
    "search": {
        "engine": "google",
        "max_results": 10,
        "max_pages_to_visit": 5,
        "delay_between_requests": 0.5
    },
    "ai": {
        "model": "local",
        "max_tokens": 2048,
        "temperature": 0.7,
        "language": "pt-BR"
    },
    "google_search": {
        "api_key": "",
        "cx": "",
        "enabled": False
    },
    "llm": {
        "enabled": True,
        "api_key": "",
        "base_url": "https://openrouter.ai/api/v1",
        "model": "meta-llama/llama-3.1-8b-instruct:free",
        "timeout": 30,
        "max_tokens": 2048,
        "temperature": 0.7
    },
    "settings": {
        "theme": "default",
        "language": "pt-BR",
        "max_search_time": 60,
        "max_suggested_links": 10,
        "cache_ttl_hours": 24,
        "detailed_mode": True,
        "silent_mode": False,
        "animations": True,
        "auto_update": False,
        "save_history": True,
        "log_level": "INFO"
    }
}

class Config:
    """Gerenciador centralizado de configurações."""

    _instance: Optional["Config"] = None
    _config_data: Dict[str, Any] = {}

    def __new__(cls, config_path: Optional[str] = None) -> "Config":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load(config_path)
        return cls._instance

    def _find_project_root(self) -> Path:
        current = Path(__file__).resolve().parent
        project_root = current.parent
        for _ in range(3):
            if (project_root / "config.json").exists():
                return project_root
            parent = project_root.parent
            if parent == project_root:
                break
            project_root = parent
        return current.parent

    def _load(self, config_path: Optional[str] = None) -> None:
        if config_path:
            path = Path(config_path)
        else:
            path = self._find_project_root() / "config.json"

        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self._config_data = json.load(f)
                return
            except (json.JSONDecodeError, IOError):
                pass

        self._config_data = DEFAULT_CONFIG.copy()

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split(".")
        value = self._config_data
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    def all(self) -> Dict[str, Any]:
        return self._config_data.copy()

    @property
    def app_name(self) -> str:
        return self.get("app_name", "Smart Terminal AI")

    @property
    def version(self) -> str:
        return self.get("version", "1.0.0")
