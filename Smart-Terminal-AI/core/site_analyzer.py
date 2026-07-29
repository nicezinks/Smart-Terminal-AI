

import json
import sys
import urllib.request
import urllib.parse
from typing import Optional, Dict, Any

from core.config import Config
from core.logger import Logger
from core.utils import is_valid_url, clean_text, truncate_text


class SiteAnalyzer:
    
    JINA_READER_URL = "https://r.jina.ai/http://{url}"
    POLLINATIONS_API = "https://text.pollinations.ai/"

    def __init__(self) -> None:
        self.config = Config()
        self.logger = Logger()

    
    def _fetch_content(self, url: str) -> Optional[str]:
     
        if not is_valid_url(url):
            self.logger.error(f"URL inválida: {url}")
            return None

        # Remove protocolo se existir para compatibilidade com Jina
        clean_url = url.replace("https://", "").replace("http://", "")
        jina_url = f"https://r.jina.ai/http://{clean_url}"

        self.logger.info(f"Extraindo conteúdo de: {url}")

        try:
            req = urllib.request.Request(
                jina_url,
                headers={
                    "User-Agent": "SmartTerminalAI-SiteAnalyzer/1.0",
                    "Accept": "text/plain"
                },
                method="GET"
            )

            with urllib.request.urlopen(req, timeout=30) as response:
                content = response.read().decode("utf-8").strip()

            if not content or len(content) < 100:
                self.logger.warning(f"Conteúdo muito curto ou vazio para: {url}")
                return None

            self.logger.info(f"Conteúdo extraído: {len(content)} caracteres")
            return content

        except urllib.error.HTTPError as e:
            self.logger.error(f"Jina Reader HTTP {e.code}: {e.reason}")
            return None
        except Exception as e:
            self.logger.error(f"Erro ao extrair conteúdo: {e}")
            return None

   
    def _generate_summary(self, content: str, url: str) -> str:
    
        # Trunca o conteúdo para não exceder limites da API
        truncated = truncate_text(content, 8000)

        prompt = (
            f"Você é um analisador de conteúdo web especializado. "
            f"Analise o texto a seguir extraído do site '{url}' e gere "
            f"um resumo COMPLETO e ESTRUTURADO em português do Brasil.

"
            f"O resumo deve responder:
"
            f"1. O que este site/site quer transmitir ao leitor?
"
            f"2. Qual é a mensagem principal ou tema central?
"
            f"3. Quem é o público-alvo?
"
            f"4. Qual é a intenção do site (informar, vender, ensinar, etc.)?
"
            f"5. Quais são os pontos-chave mais importantes?
"
            f"6. Há alguma chamada para ação ou próximo passo sugerido?

"
            f"Use markdown com títulos, listas e formatação clara. "
            f"Seja objetivo, completo e natural.

"
            f"--- CONTEÚDO DO SITE ---
{truncated}
"
            f"--- FIM DO CONTEÚDO ---

"
            f"Resumo estruturado:"
        )

        self.logger.info("Gerando resumo inteligente via Pollinations AI...")

        try:
            payload = json.dumps({
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "Você é um analisador de conteúdo web especializado. "
                            "Responda sempre em português do Brasil de forma clara, "
                            "organizada e completa."
                        )
                    },
                    {"role": "user", "content": prompt}
                ],
                "model": "openai",
                "seed": 42,
                "temperature": 0.7
            }).encode("utf-8")

            req = urllib.request.Request(
                self.POLLINATIONS_API,
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST"
            )

            with urllib.request.urlopen(req, timeout=60) as resp:
                summary = resp.read().decode("utf-8").strip()

            self.logger.info("Resumo gerado com sucesso")
            return summary

        except Exception as e:
            self.logger.error(f"Erro ao gerar resumo: {e}")
            # Fallback: retorna um resumo básico baseado no conteúdo
            return self._fallback_summary(content, url)

    def _fallback_summary(self, content: str, url: str) -> str:
        """Resumo básico caso a API de IA falhe."""
        lines = content.split("\n")
        title = lines[0] if lines else "Sem título"
        paragraphs = [l for l in lines[1:] if len(l.strip()) > 50][:5]

        summary = f"""##  Análise do Site: {url}

###  Título/Resumo Rápido
{title}

###  O que o site transmite
{" ".join(paragraphs)}

###  Nota
O resumo inteligente não pôde ser gerado (serviço temporariamente indisponível).
Acima está o conteúdo bruto extraído do site.
"""
        return summary

   
    def analyze(self, url: str) -> Dict[str, Any]:
        """
        Analisa um site completo: extrai conteúdo e gera resumo.

        Args:
            url: Endereço do site a ser analisado

        Returns:
            Dict com: url, title, content_length, summary, success
        """
        if not is_valid_url(url):
            return {
                "url": url,
                "title": "",
                "content_length": 0,
                "summary": " URL inválida. Por favor, forneça um link completo (ex: https://exemplo.com)",
                "success": False
            }

        content = self._fetch_content(url)

        if not content:
            return {
                "url": url,
                "title": "",
                "content_length": 0,
                "summary": (
                    f" Não foi possível extrair o conteúdo de: {url}\n\n"
                    f"Possíveis causas:
"
                    f"• O site bloqueia bots ou requer JavaScript\n"
                    f"• O site está fora do ar ou inacessível\n"
                    f"• A URL está incorreta ou redireciona para login\n\n"
                    f"Tente outro link ou verifique se o site está online."
                ),
                "success": False
            }

        # Extrai título (primeira linha do conteúdo Jina geralmente é o título)
        lines = content.split("\n")
        title = lines[0].strip() if lines else "Sem título"

        summary = self._generate_summary(content, url)

        return {
            "url": url,
            "title": title,
            "content_length": len(content),
            "summary": summary,
            "success": True
        }

    def print_analysis(self, url: str) -> None:
        """
        Analisa um site e imprime o resultado formatado no terminal.
        Método conveniente para uso via linha de comando.
        """
        print(f"\n{'═' * 70}")
        print(f"  🔗 Analisando: {url}")
        print(f"{'═' * 70}\n")

        result = self.analyze(url)

        if result["success"]:
            print(f" Análise concluída!")
            print(f" Título: {result['title']}")
            print(f" Caracteres extraídos: {result['content_length']}")
            print(f"\n{'─' * 70}")
            print(result["summary"])
            print(f"{'─' * 70}\n")
        else:
            print(result["summary"])
            print()



def main() -> None:
    """
    Ponto de entrada para uso via linha de comando.

    Exemplos:
        python core/site_analyzer.py https://openai.com
        python core/site_analyzer.py https://g1.globo.com
        python -m core.site_analyzer https://exemplo.com
    """
    if len(sys.argv) < 2:
        print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🌐 SMART TERMINAL AI — SITE ANALYZER                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Uso:  python core/site_analyzer.py <URL>                                  ║
║                                                                              ║
║  Exemplos:                                                                   ║
║    python core/site_analyzer.py https://openai.com                          ║
║    python core/site_analyzer.py https://g1.globo.com                       ║
║    python core/site_analyzer.py https://www.bbc.com/news                   ║
║                                                                              ║
║  Descrição:                                                                  ║
║    Este módulo analisa qualquer site e gera um resumo completo explicando  ║
║    o que o site quer transmitir ao leitor. Usa APIs públicas gratuitas:      ║
║    • Jina AI Reader  → extração de texto                                   ║
║    • Pollinations AI → resumo inteligente                                  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """)
        sys.exit(0)

    url = sys.argv[1]
    analyzer = SiteAnalyzer()
    analyzer.print_analysis(url)


if __name__ == "__main__":
    main()
