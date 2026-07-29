

import json
from pathlib import Path
from typing import List, Dict, Set
from urllib.parse import urlparse

from core.config import Config
from core.logger import Logger

class TrustedSourceManager:
    """Gerencia domínios confiáveis e filtra resultados de busca."""

    def __init__(self) -> None:
        self.config = Config()
        self.logger = Logger()
        self._domains: Set[str] = set()
        self._load_domains()

    def _load_domains(self) -> None:
        """Extrai domínios do trusted_sources.json."""
        base = Path(__file__).resolve().parent.parent
        sources_file = base / "trusted_sources.json"

        if not sources_file.exists():
            return

        try:
            with open(sources_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            for category, sites in data.items():
                for site in sites:
                    url = site.get("url", "")
                    if url:
                        parsed = urlparse(url)
                        domain = parsed.netloc.replace("www.", "")
                        if domain:
                            self._domains.add(domain)
                            # Também adiciona com www
                            self._domains.add("www." + domain)

            self.logger.info(f"{len(self._domains)} domínios confiáveis carregados")
        except Exception:
            pass

    def is_trusted(self, url: str) -> bool:
        """Verifica se uma URL pertence a um domínio confiável."""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.replace("www.", "")
            return domain in self._domains or ("www." + domain) in self._domains
        except Exception:
            return False

    def score_result(self, url: str) -> int:
        """Retorna score de confiança (mais alto = mais confiável)."""
        if self.is_trusted(url):
            return 100
        return 0

    def filter_and_sort(self, results: List[Dict]) -> List[Dict]:
        """Reordena resultados colocando fontes confiáveis primeiro."""
        scored = []
        for r in results:
            url = r.get("url", "")
            score = self.score_result(url)
            scored.append((score, r))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [r for _, r in scored]
