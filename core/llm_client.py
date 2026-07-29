"""Cliente LLM gratuito via Pollinations AI."""
import json
import urllib.request
from typing import List, Any

class LLMClient:
    API_URL = "https://text.pollinations.ai/"

    def generate(self, query: str, search_results: List[Any]) -> str:
        context = ""
        for i, r in enumerate(search_results[:8], 1):
            d = r.to_dict() if hasattr(r, 'to_dict') else r
            snippet = d.get("snippet", "") or d.get("title", "")
            context += f"[{i}] {snippet}\n"

        prompt = (
            f"Voce e um assistente de pesquisa. Responda em portugues do Brasil "
            f"de forma clara, organizada, usando markdown com titulos e listas.\n\n"
            f"INFORMACOES DA WEB:\n{context}\n\n"
            f"PERGUNTA: {query}\n\n"
            f"Resposta:"
        )

        try:
            payload = json.dumps({
                "messages": [
                    {"role": "system", "content": "Voce e um assistente util que responde em portugues."},
                    {"role": "user", "content": prompt}
                ],
                "model": "openai",
                "seed": 42
            }).encode("utf-8")

            req = urllib.request.Request(
                self.API_URL, data=payload,
                headers={"Content-Type": "application/json"},
                method="POST"
            )

            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read().decode("utf-8").strip()
        except Exception:
            lines = [f"## {query}", ""]
            for i, r in enumerate(search_results[:5], 1):
                d = r.to_dict() if hasattr(r, 'to_dict') else r
                lines.append(f"{i}. **{d.get('title', 'Link')}**")
                if d.get('snippet'): lines.append(f"   {d['snippet']}")
                lines.append(f"   {d.get('url', '')}")
                lines.append("")
            return "\n".join(lines)
