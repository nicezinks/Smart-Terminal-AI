

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

from core.config import Config
from core.logger import Logger
from core.utils import generate_id

class Cache:
    def __init__(self, cache_path: Optional[str] = None) -> None:
        self.config = Config()
        try:
            self.logger = Logger()
        except Exception:
            self.logger = None

        if cache_path:
            self.cache_file = Path(cache_path)
        else:
            base = Path.cwd()
            
            for path in [base, base.parent, base.parent.parent]:
                if (path / "config.json").exists():
                    base = path
                    break
            self.cache_file = base / "cache" / "cache.json"

        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        self.ttl_hours = self.config.get("settings.cache_ttl_hours", 24)
        self._data: Dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        if self.cache_file.exists():
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
            except Exception:
                self._data = {}
        else:
            self._data = {}

    def _save(self) -> None:
        try:
            self.cache_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=4, ensure_ascii=False)
        except Exception:
            pass

    def _is_expired(self, entry: Dict[str, Any]) -> bool:
        cached = datetime.fromisoformat(entry.get("timestamp", "2000-01-01"))
        return datetime.now() > cached + timedelta(hours=self.ttl_hours)

    def get(self, query: str) -> Optional[Dict[str, Any]]:
        key = generate_id(query.strip().lower())
        if key in self._data:
            if self._is_expired(self._data[key]):
                del self._data[key]
                self._save()
                return None
            return self._data[key]["data"]
        return None

    def set(self, query: str, data: Dict[str, Any]) -> None:
        key = generate_id(query.strip().lower())
        self._data[key] = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "data": data
        }
        self._save()

    def clear(self) -> None:
        self._data.clear()
        self._save()

    def cleanup_expired(self) -> int:
        expired = [k for k, v in self._data.items() if self._is_expired(v)]
        for k in expired:
            del self._data[k]
        if expired:
            self._save()
        return len(expired)

    def stats(self) -> Dict[str, Any]:
        total = len(self._data)
        exp = sum(1 for v in self._data.values() if self._is_expired(v))
        return {"total_entries": total, "expired_entries": exp,
                "valid_entries": total - exp, "ttl_hours": self.ttl_hours,
                "file_path": str(self.cache_file)}
