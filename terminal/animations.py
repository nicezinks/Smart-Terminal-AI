"""
Animações e efeitos visuais para o terminal.
Barras de progresso, spinners e transições.
"""

import asyncio
import itertools
import sys
import time
from typing import List, Optional, Callable

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.panel import Panel
from rich.text import Text

from terminal.colors import Colors


console = Console()


class TerminalAnimations:
    """Gerenciador de animações do terminal."""

    SPINNER_FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    DOTS_FRAMES = ["   ", ".  ", ".. ", "..."]

    def __init__(self) -> None:
        self._running = False
        self._current_task = ""

    def show_banner(self) -> None:
        """Exibe o banner principal do aplicativo."""
        banner_text = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           🤖  Smart Terminal AI Search  🤖                   ║
║                                                              ║
║     Assistente inteligente de pesquisa web via terminal      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """
        console.print(Panel(
            Text(banner_text, style="bold cyan"),
            border_style="cyan",
            padding=(1, 2)
        ))

    def show_welcome(self) -> None:
        """Exibe mensagem de boas-vindas."""
        console.print(Panel(
            "[bold green]Bem-vindo![/bold green]\n"
            "[white]Digite sua pergunta abaixo ou use [bold]/ajuda[/bold] para ver os comandos.[/white]",
            border_style="green",
            title="👋 Olá!",
            title_align="left"
        ))

    def show_spinner(self, message: str, duration: float = 2.0) -> None:
        """Exibe um spinner com mensagem por um tempo determinado."""
        with console.status(f"[cyan]{message}[/cyan]", spinner="dots"):
            time.sleep(duration)

    def show_progress_steps(self, steps: List[str], step_duration: float = 1.5) -> None:
        """Exibe progresso visual de múltiplas etapas."""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=40),
            TaskProgressColumn(),
            console=console,
            transient=True
        ) as progress:
            task = progress.add_task("[cyan]Processando...", total=len(steps))
            for step in steps:
                progress.update(task, description=f"[cyan]{step}[/cyan]")
                time.sleep(step_duration)
                progress.advance(task)

    def show_typing_effect(self, text: str, delay: float = 0.01) -> None:
        """Simula efeito de digitação no terminal."""
        for char in text:
            console.print(char, end="")
            time.sleep(delay)
        console.print()

    def show_separator(self, char: str = "═", length: int = 60) -> None:
        """Exibe uma linha separadora decorativa."""
        console.print(f"[cyan]{char * length}[/cyan]")

    def show_success(self, message: str) -> None:
        """Exibe mensagem de sucesso."""
        console.print(f"[bold green]✓[/bold green] {message}")

    def show_error(self, message: str) -> None:
        """Exibe mensagem de erro."""
        console.print(f"[bold red]✗[/bold red] {message}")

    def show_info(self, message: str) -> None:
        """Exibe mensagem informativa."""
        console.print(f"[bold blue]ℹ[/bold blue] {message}")

    def show_warning(self, message: str) -> None:
        """Exibe mensagem de aviso."""
        console.print(f"[bold yellow]⚠[/bold yellow] {message}")

    def show_panel(self, title: str, content: str, style: str = "cyan") -> None:
        """Exibe conteúdo em um painel decorativo."""
        console.print(Panel(
            content,
            title=f"[bold]{title}[/bold]",
            border_style=style,
            padding=(1, 2)
        ))

    def show_link_list(self, links: List[dict]) -> None:
        """Exibe lista de links formatada."""
        if not links:
            return

        console.print("\n[bold cyan]📚 Você deseja saber mais?[/bold cyan]\n")
        for i, link in enumerate(links, 1):
            title = link.get("title", "Sem título")
            url = link.get("url", "")
            snippet = link.get("snippet", "")

            content = f"[bold white]{title}[/bold white]\n"
            if snippet:
                content += f"[dim]{snippet[:100]}...[/dim]\n"
            content += f"[blue underline]{url}[/blue underline]"

            console.print(Panel(
                content,
                title=f"[bold]{i}[/bold]",
                border_style="blue",
                padding=(0, 1)
            ))

    def show_response(self, response: str) -> None:
        """Exibe a resposta da IA formatada."""
        console.print(Panel(
            response,
            title="[bold green]🤖 Resposta da IA[/bold green]",
            border_style="green",
            padding=(1, 2)
        ))

    def show_stats(self, duration: float, sources: int, from_cache: bool = False) -> None:
        """Exibe estatísticas da pesquisa."""
        cache_status = "[yellow](do cache)[/yellow]" if from_cache else ""
        stats_text = (
            f"⏱ Tempo: [bold]{duration:.1f}s[/bold] {cache_status} | "
            f"📄 Fontes: [bold]{sources}[/bold]"
        )
        console.print(f"\n[dim]{stats_text}[/dim]\n")
