
import time
from typing import Dict, Any

from core.cache import Cache
from core.config import Config
from core.history import History
from core.logger import Logger
from core.llm_client import LLMClient
from core.search import search_duckduckgo

class AIAssistant:
    def __init__(self):
        self.config = Config()
        self.logger = Logger()
        self.cache = Cache()
        self.history = History()
        self.llm = LLMClient()

    async def process_query(self, query: str) -> Dict[str, Any]:
        start = time.time()

        cached = self.cache.get(query)
        if cached:
            return {**cached, "duration": 0.0, "from_cache": True}

        try:
            results = search_duckduckgo(query, max_results=10)

            if not results:
                return {
                    "query": query,
                    "response": " Nao encontrei resultados. Tente reformular a pergunta.",
                    "links": [],
                    "duration": time.time() - start,
                    "from_cache": False,
                    "sources_count": 0
                }

            response = self.llm.generate(query, results)
            links = [{"title": r.title, "url": r.url, "snippet": r.snippet} for r in results[:10]]
            duration = time.time() - start

            self.cache.set(query, {"response": response, "links": links, "sources_count": len(links)})
            self.history.add(query, response, links, duration, len(links))
            self.logger.log_search(query, duration, len(links))

            return {
                "query": query,
                "response": response,
                "links": links,
                "duration": duration,
                "from_cache": False,
                "sources_count": len(links)
            }
        except Exception as e:
            return {
                "query": query,
                "response": f" Erro: {e}",
                "links": [],
                "duration": time.time() - start,
                "from_cache": False,
                "sources_count": 0
            }

    def get_stats(self):
        return {"cache": self.cache.stats(), "history": self.history.stats(), "version": self.config.version}
