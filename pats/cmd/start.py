"""Start command for paTS"""

import typer
from rich import print


def start(
    project: str | None = typer.Argument(None, help="Project name to start tracking"),
    description: str | None = typer.Option(
        None, "--desc", "-d", help="Description of the work"
    ),
):
    """Start tracking time for a project"""
    print("[green]⏱️  Starting time tracker...[/green]")
    if project:
        print(f"[blue]Project:[/blue] {project}")
    if description:
        print(f"[blue]Description:[/blue] {description}")
    print("[yellow]🚧 Command scaffolded - implementation pending[/yellow]")
