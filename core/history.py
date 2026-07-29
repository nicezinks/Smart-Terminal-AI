"""
Histórico de pesquisas.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from core.config import Config
from core.logger import Logger

class History:
    def __init__(self, history_path: Optional[str] = None) -> None:
        self.config = Config()
        try:
            self.logger = Logger()
        except Exception:
            self.logger = None

        if history_path:
            self.history_file = Path(history_path)
        else:
            base = Path.cwd()
            for path in [base, base.parent, base.parent.parent]:
                if (path / "config.json").exists():
                    base = path
                    break
            self.history_file = base / "history.json"

        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        self._entries: List[Dict[str, Any]] = []
        self._load()

    def _load(self) -> None:
        if self.history_file.exists():
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    self._entries = json.load(f)
            except Exception:
                self._entries = []
        else:
            self._entries = []

    def _save(self) -> None:
        try:
            self.history_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self._entries, f, indent=4, ensure_ascii=False)
        except Exception:
            pass

    def add(self, query: str, response: str, links: List[Dict[str, str]],
            duration: float, source_count: int) -> None:
        entry = {
            "id": len(self._entries) + 1,
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "query": query,
            "response": response,
            "links": links,
            "duration_seconds": round(duration, 2),
            "source_count": source_count
        }
        self._entries.append(entry)
        self._save()

    def get_all(self) -> List[Dict[str, Any]]:
        return self._entries.copy()

    def get_recent(self, limit: int = 10) -> List[Dict[str, Any]]:
        return self._entries[-limit:][::-1]

    def search(self, keyword: str) -> List[Dict[str, Any]]:
        kw = keyword.lower()
        return [e for e in self._entries
                if kw in e.get("query", "").lower() or kw in e.get("response", "").lower()]

    def clear(self) -> None:
        self._entries.clear()
        self._save()

    def stats(self) -> Dict[str, Any]:
        if not self._entries:
            return {"total": 0, "avg_duration": 0, "first_query": None, "last_query": None}
        durations = [e.get("duration_seconds", 0) for e in self._entries]
        return {"total": len(self._entries), "avg_duration": round(sum(durations)/len(durations), 2),
                "first_query": self._entries[0].get("date"), "last_query": self._entries[-1].get("date")}
