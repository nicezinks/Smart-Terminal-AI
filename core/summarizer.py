

import json
import re
from pathlib import Path
from typing import List, Dict, Any, Optional

from core.config import Config
from core.logger import Logger
from core.utils import truncate_text, current_timestamp

class Summarizer:
    """Motor de sumarização e geração de respostas."""

    def __init__(self) -> None:
        self.config = Config()
        self.logger = Logger()
        self._prompts = self._load_prompts()

    def _load_prompts(self) -> Dict[str, str]:
        """Carrega prompts do arquivo prompts.json."""
        base = Path(__file__).resolve().parent.parent
        prompts_file = base / "prompts.json"
        if prompts_file.exists():
            try:
                with open(prompts_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                self.logger.error(f"Erro ao carregar prompts: {e}")
                return {}

    def _extract_key_sentences(self, text: str, max_sentences: int = 10) -> List[str]:
        """Extrai sentenças mais relevantes por heurística simples."""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]

        # Heurística: sentenças com números, datas ou termos técnicos são mais informativas
        scored = []
        for sent in sentences:
            score = 0
            if re.search(r'\d{4}|\d+%|\d+\s*(milhões?|bilhões?|trilhões?)', sent):
                score += 3
            if re.search(r'[A-Z][a-z]+\s+(disse|afirmou|explicou|destacou)', sent):
                score += 2
            if len(sent) > 100:
                score += 1
            scored.append((score, sent))

        scored.sort(reverse=True)
        return [s for _, s in scored[:max_sentences]]

    def _structure_response(self, query: str, contents: List[Dict[str, Any]],
                            sources: List[Dict[str, str]]) -> str:
        """Estrutura uma resposta completa baseada no conteúdo extraído."""

        # Concatena textos relevantes
        all_text = "\n\n".join([
            f"FONTE: {c.get('title', 'Desconhecido')}\n{c.get('text', '')}"
            for c in contents if c.get('text')
        ])

        if not all_text.strip():
            return self._prompts.get("error_prompt",
                "Não foi possível obter informações suficientes.")

        # Extrai sentenças-chave
        key_sentences = self._extract_key_sentences(all_text, max_sentences=15)

        # Gera resposta estruturada
        response_parts = []

        # Introdução contextual
        response_parts.append(f"## Resposta sobre: {query}")
        response_parts.append("")

        # Resumo executivo
        response_parts.append("### Resumo")
        summary_sentences = key_sentences[:5]
        response_parts.append(" ".join(summary_sentences))
        response_parts.append("")

        # Pontos principais
        response_parts.append("### Principais Informações")
        for i, sent in enumerate(key_sentences[5:12], 1):
            response_parts.append(f"{i}. {sent}")
        response_parts.append("")

        # Detalhes adicionais se modo detalhado
        if self.config.get("settings.detailed_mode", True):
            response_parts.append("### Detalhes")
            for content in contents[:3]:
                title = content.get('title', 'Fonte')
                text = content.get('text', '')
                if text:
                    response_parts.append(f"**{title}**: {truncate_text(text, 300)}")
            response_parts.append("")

        # Conclusão
        response_parts.append("### Conclusão")
        response_parts.append(
            f"Com base nas fontes consultadas, as informações sobre '{query}' "
            f"indicam os pontos acima. Recomenda-se verificar as fontes originais "
            f"para mais detalhes."
        )

        return "\n".join(response_parts)

    def summarize(self, query: str, scraped_contents: List[Any],
                  search_results: List[Any]) -> str:
        """Gera resposta sumarizada a partir do conteúdo extraído."""
        self.logger.info(f"Gerando resumo para query: {query[:50]}...")

        contents = [c.to_dict() if hasattr(c, 'to_dict') else c for c in scraped_contents]
        sources = [r.to_dict() if hasattr(r, 'to_dict') else r for r in search_results]

        response = self._structure_response(query, contents, sources)
        self.logger.info("Resumo gerado com sucesso")
        return response

    def generate_follow_up(self, query: str) -> List[str]:
        """Gera sugestões de perguntas de acompanhamento."""
        templates = [
            f"Quais são as vantagens de {query}?",
            f"Quais são as desvantagens de {query}?",
            f"Como {query} funciona na prática?",
            f"Qual a história/origem de {query}?",
            f"Quais são as alternativas para {query}?",
        ]
        return templates[:3]
