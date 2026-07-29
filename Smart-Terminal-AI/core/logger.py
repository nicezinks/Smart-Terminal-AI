"""
Sistema de logging 
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

class Logger:
    

    _instance: Optional["Logger"] = None
    _logger: Optional[logging.Logger] = None

    def __new__(cls) -> "Logger":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._setup()
        return cls._instance

    def _setup(self) -> None:
        self._logger = logging.getLogger("SmartTerminalAI")
        self._logger.setLevel(logging.DEBUG)

        if self._logger.handlers:
            return

        # Tenta arquivo — se falhar, usa null handler (silêncio total)
        try:
            current = Path(__file__).resolve().parent
            project_root = current.parent
            for _ in range(3):
                if (project_root / "config.json").exists():
                    break
                parent = project_root.parent
                if parent == project_root:
                    break
                project_root = parent

            log_dir = project_root / "logs"
            log_dir.mkdir(parents=True, exist_ok=True)
            log_file = log_dir / f"{datetime.now().strftime('%Y-%m-%d')}.log"

            file_handler = logging.FileHandler(str(log_file), encoding="utf-8")
            file_handler.setLevel(logging.DEBUG)
            fmt = logging.Formatter(
                "%(asctime)s | %(levelname)-8s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            file_handler.setFormatter(fmt)
            self._logger.addHandler(file_handler)
        except Exception:
            self._logger.addHandler(logging.NullHandler())

    def debug(self, message: str) -> None:
        if self._logger: self._logger.debug(message)

    def info(self, message: str) -> None:
        if self._logger: self._logger.info(message)

    def warning(self, message: str) -> None:
        if self._logger: self._logger.warning(message)

    def error(self, message: str, exc_info: bool = False) -> None:
        if self._logger: self._logger.error(message, exc_info=exc_info)

    def critical(self, message: str) -> None:
        if self._logger: self._logger.critical(message)

    def log_search(self, query: str, duration: float, results_count: int) -> None:
        self.info(f"PESQUISA | '{query}' | {duration:.2f}s | {results_count} resultados")
