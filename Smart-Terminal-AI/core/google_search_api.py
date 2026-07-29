

import json
import urllib.request
import urllib.error
from typing import List, Dict, Any, Optional

from core.config import Config
from core.logger import Logger

class GoogleSearchAPI:
   
    API_URL = "https://www.googleapis.com/customsearch/v1"

    def __init__(self) -> None:
        self.config = Config()
        self.logger = Logger()
        self.api_key = self.config.get("google_search.api_key", "")
        self.cx = self.config.get("google_search.cx", "")
        self.enabled = bool(self.api_key and self.cx and self.api_key.strip() and self.cx.strip())

    def search(self, query: str, num_results: int = 10) -> List[Dict[str, str]]:
       
        if not self.enabled:
            self.logger.info("API Google Custom Search não configurada. Pulando.")
            return []

        results = []
        num_results = min(num_results, 10) # API limita a 10 por request

        try:
            url = (
                f"{self.API_URL}?"
                f"key={self.api_key}&"
                f"cx={self.cx}&"
                f"q={urllib.parse.quote_plus(query)}&"
                f"num={num_results}&"
                f"lr=lang_pt&"
                f"safe=active"
            )

            req = urllib.request.Request(url, headers={
                "Accept": "application/json",
                "User-Agent": "SmartTerminalAI/1.0"
            })

            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode("utf-8"))

            items = data.get("items", [])
            for item in items:
                results.append({
                    "title": item.get("title", "Sem título"),
                    "url": item.get("link", ""),
                    "snippet": item.get("snippet", ""),
                    "source": "Google API"
                })

            self.logger.info(f"Google API retornou {len(results)} resultados")

        except urllib.error.HTTPError as e:
            if e.code == 403:
                self.logger.error("Google API: Quota excedida ou key inválida")
            elif e.code == 400:
                self.logger.error("Google API: Parâmetros inválidos (verifique cx e key)")
            else:
                self.logger.error(f"Google API HTTP {e.code}: {e.reason}")
        except Exception as e:
            self.logger.error(f"Google API erro: {e}")

        return results
