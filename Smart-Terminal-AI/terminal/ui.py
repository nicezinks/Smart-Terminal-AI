"""
Interface do usuário principal
"""

import asyncio
import sys
import time
from typing import List, Dict, Any, Optional

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from core.ai import AIAssistant
from core.cache import Cache
from core.config import Config
from core.history import History
from core.logger import Logger
from terminal.animations import TerminalAnimations
from terminal.colors import Colors

class SmartTerminalUI:
    """Interface de terminal interativa e visualmente rica."""

    COMMANDS = [
        "/ajuda", "/help",
        "/sair", "/exit", "/quit",
        "/historico", "/history",
        "/limpar", "/clear",
        "/cache", "/stats",
        "/config",
        "/sobre", "/about"
    ]

    def __init__(self) -> None:
        self.config = Config()
        self.logger = Logger()
        self.ai = AIAssistant()
        self.animations = TerminalAnimations()
        self.console = Console()
        self.cache = Cache()
        self.history = History()

        self.session = PromptSession(
            completer=WordCompleter(self.COMMANDS, ignore_case=True),
            style=Style.from_dict({
                "prompt": "ansicyan bold",
                "": "ansigreen",
            })
        )
        self._running = True

    def _print_header(self) -> None:
        """Exibe o cabeçalho do aplicativo."""
        self.console.clear()
        self.animations.show_banner()
        self.animations.show_welcome()
        self.console.print()

    def _print_help(self) -> None:
        """Exibe ajuda com comandos disponíveis."""
        help_text = """
[bold cyan]Comandos disponíveis:[/bold cyan]

  [green]/ajuda[/green] ou [green]/help[/green] - Mostra esta mensagem
  [green]/sair[/green] ou [green]/exit[/green] - Encerra o programa
  [green]/historico[/green] ou [green]/history[/green] - Mostra histórico de pesquisas
  [green]/limpar[/green] ou [green]/clear[/green] - Limpa o histórico
  [green]/cache[/green] - Mostra estatísticas do cache
  [green]/stats[/green] - Mostra estatísticas gerais
  [green]/config[/green] - Mostra configurações atuais
  [green]/sobre[/green] ou [green]/about[/green] - Informações sobre o programa

[bold yellow]Dica:[/bold yellow] Digite qualquer pergunta para pesquisar na web!
        """
        self.console.print(Panel(help_text, border_style="cyan", title=" Ajuda", title_align="left"))

    def _print_history(self) -> None:
        """Exibe histórico de pesquisas."""
        entries = self.history.get_recent(limit=10)
        if not entries:
            self.animations.show_info("Nenhuma pesquisa no histórico ainda.")
            return

        history_text = ""
        for entry in entries:
            history_text += (
                f"\n[bold cyan]#{entry['id']}" + "[/bold cyan] [dim]" + f"{entry['date']} {entry['time']}" + "[/dim]\n"
                f"  [white]Q:[/white] {entry['query']}\n"
                f"  [dim]⏱ {entry['duration_seconds']}s | 📄 {entry['source_count']} fontes[/dim]\n"
            )

        self.console.print(Panel(
            history_text,
            border_style="magenta",
            title=" Histórico",
            title_align="left"
        ))

    def _print_stats(self) -> None:
        """Exibe estatísticas do sistema."""
        stats = self.ai.get_stats()
        cache_stats = stats.get("cache", {})
        history_stats = stats.get("history", {})

        stats_text = f"""
[bold cyan]Estatísticas do Sistema[/bold cyan]

[green]Cache:[/green]
  • Entradas totais: {cache_stats.get('total_entries', 0)}
  • Entradas válidas: {cache_stats.get('valid_entries', 0)}
  • TTL: {cache_stats.get('ttl_hours', 24)} horas

[green]Histórico:[/green]
  • Total de pesquisas: {history_stats.get('total', 0)}
  • Tempo médio: {history_stats.get('avg_duration', 0)}s

[green]Versão:[/green] {stats.get('version', '1.0.0')}
        """
        self.console.print(Panel(stats_text, border_style="green", title="📊 Estatísticas"))

    def _print_config(self) -> None:
        """Exibe configurações atuais."""
        settings = self.config.all()
        config_text = f"""
[bold cyan]Configurações Atuais[/bold cyan]

[green]Tema:[/green] {settings.get('settings', {}).get('theme', 'default')}
[green]Idioma:[/green] {settings.get('settings', {}).get('language', 'pt-BR')}
[green]Modo detalhado:[/green] {settings.get('settings', {}).get('detailed_mode', True)}
[green]Modo silencioso:[/green] {settings.get('settings', {}).get('silent_mode', False)}
[green]Animações:[/green] {settings.get('settings', {}).get('animations', True)}
[green]Cache TTL:[/green] {settings.get('settings', {}).get('cache_ttl_hours', 24)} horas
[green]Max links:[/green] {settings.get('settings', {}).get('max_suggested_links', 5)}
        """
        self.console.print(Panel(config_text, border_style="blue", title="⚙️ Configurações"))

    def _print_about(self) -> None:
        """Exibe informações sobre o programa."""
        about_text = f"""
[bold cyan]{self.config.app_name}[/bold cyan]
[white]Versão:[/white] {self.config.version}

Assistente inteligente de pesquisa web que utiliza navegação
headless para encontrar, extrair e sumarizar informações da
internet em tempo real.

[green]Tecnologias:[/green]
  • Python 3.12+
  • Playwright (automação de navegador)
  • BeautifulSoup4 (parsing HTML)
  • Rich (interface rica no terminal)
  • Prompt Toolkit (input interativo)

[dim]Desenvolvido com  para facilitar suas pesquisas.[/dim]
        """
        self.console.print(Panel(about_text, border_style="yellow", title=" Sobre"))

    async def _process_command(self, command: str) -> bool:
        """Processa comandos especiais. Retorna False se deve continuar loop."""
        cmd = command.lower().strip()

        if cmd in ("/sair", "/exit", "/quit"):
            self.animations.show_info("Até logo! ")
            self._running = False
            return False

        elif cmd in ("/ajuda", "/help"):
            self._print_help()

        elif cmd in ("/historico", "/history"):
            self._print_history()

        elif cmd in ("/limpar", "/clear"):
            self.cache.clear()
            self.history.clear()
            self.animations.show_success("Cache e histórico limpos!")

        elif cmd == "/cache":
            stats = self.cache.stats()
            self.console.print(Panel(
                f"Entradas: {stats['total_entries']}\n"
                f"Válidas: {stats['valid_entries']}\n"
                f"Expiradas: {stats['expired_entries']}",
                border_style="blue",
                title=" Cache"
            ))

        elif cmd == "/stats":
            self._print_stats()

        elif cmd == "/config":
            self._print_config()

        elif cmd in ("/sobre", "/about"):
            self._print_about()

        else:
            self.animations.show_warning(f"Comando desconhecido: {command}")
            self.animations.show_info("Use /ajuda para ver os comandos disponíveis.")

        return True

    async def _process_query(self, query: str) -> None:
        """Processa uma pergunta do usuário e exibe resultados."""
        self.console.print()

        # Animação de análise
        steps = [
            " Analisando pergunta...",
            " Iniciando navegador headless...",
            " Pesquisando na web...",
            " Encontrando páginas relevantes...",
            " Extraindo conteúdo...",
            " Gerando resumo..."
        ]

        self.animations.show_progress_steps(steps, step_duration=0.8)
        self.console.print()

        # Processa a query de forma assíncrona nativa
        try:
            result = await self.ai.process_query(query)
        except Exception as e:
            self.logger.error(f"Erro ao processar query: {e}", exc_info=True)
            self.animations.show_error(f"Erro na pesquisa: {e}")
            return

        # Exibe resposta
        self.animations.show_response(result["response"])

        # Exibe links
        if result.get("links"):
            self.animations.show_link_list(result["links"])

        # Exibe estatísticas
        self.animations.show_stats(
            duration=result["duration"],
            sources=result["sources_count"],
            from_cache=result.get("from_cache", False)
        )

        self.console.print()

    async def run(self) -> None:
        """Loop principal da interface (ASSÍNCRONO NATIVO)."""
        self._print_header()

        while self._running:
            try:
                # Usa prompt_async para compatibilidade com o loop de eventos
                user_input = await self.session.prompt_async(
                    "> ",
                    placeholder="Digite sua pergunta..."
                )
                user_input = user_input.strip()

                if not user_input:
                    continue

                if user_input.startswith("/"):
                    await self._process_command(user_input)
                else:
                    await self._process_query(user_input)

            except KeyboardInterrupt:
                self.console.print("\n")
                self.animations.show_info("Use /sair para encerrar ou continue pesquisando.")
            except EOFError:
                break
            except Exception as e:
                self.logger.error(f"Erro na UI: {e}", exc_info=True)
                self.animations.show_error(f"Erro inesperado: {e}")

        self.console.print("\n[dim]Smart Terminal AI Search encerrado.[/dim]")

def main() -> None:
    """Ponto de entrada da interface."""
    ui = SmartTerminalUI()
    try:
        asyncio.run(ui.run())
    except KeyboardInterrupt:
        print("\nEncerrado pelo usuário.")
    except Exception as e:
        print(f"Erro fatal: {e}")
        sys.exit(1)
