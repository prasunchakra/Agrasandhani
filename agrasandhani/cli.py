"""Agrasandhani CLI - Main entry point"""

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from typing import Optional

from agrasandhani.core.scanner import Scanner
from agrasandhani.config import Settings

app = typer.Typer(
    name="agrasandhani",
    help="A focused web application security scanner aligned with OWASP Top 10",
    add_completion=False,
)
console = Console()


@app.command()
def scan(
    url: str = typer.Argument(..., help="Target URL to scan (e.g., https://example.com)"),
    config: Optional[str] = typer.Option(
        None, "--config", "-c", help="Path to custom configuration file"
    ),
    output: str = typer.Option(
        "table", "--output", "-o", help="Output format: table, json"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
):
    """
    Scan a web application for security issues aligned with OWASP Top 10.
    """
    console.print(
        Panel.fit(
            f"[bold blue]Agrasandhani[/bold blue] - Starting scan on [cyan]{url}[/cyan]",
            border_style="blue",
        )
    )

    try:
        settings = Settings.load(config)
        scanner = Scanner(target_url=url, settings=settings, verbose=verbose)

        with console.status("[bold green]Scanning in progress...[/bold green]"):
            results = scanner.run()

        if output == "json":
            import json
            console.print(json.dumps(results, indent=2, default=str))
        else:
            _display_results_table(results)

        console.print(f"\n[green]Scan completed successfully![/green]")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise typer.Exit(code=1)


def _display_results_table(results: dict):
    """Display scan results in a nice Rich table."""
    table = Table(title="Scan Results", show_lines=True)
    table.add_column("Category", style="cyan", no_wrap=True)
    table.add_column("Finding", style="white")
    table.add_column("Severity", style="red")
    table.add_column("Details", style="dim")

    for category, findings in results.get("findings", {}).items():
        for finding in findings:
            table.add_row(
                category,
                finding.get("title", "N/A"),
                finding.get("severity", "Medium"),
                finding.get("description", "")[:80] + "..."
                if len(finding.get("description", "")) > 80
                else finding.get("description", ""),
            )

    console.print(table)


@app.command()
def version():
    """Show Agrasandhani version."""
    from agrasandhani import __version__
    console.print(f"Agrasandhani version: [bold]{__version__}[/bold]")


if __name__ == "__main__":
    app()
