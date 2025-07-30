"""Week command for paTS"""

import typer
from rich import print


def week(
    date: str | None = typer.Argument(
        None, help="Date in YYYY-MM-DD format (defaults to current week)"
    ),
):
    """Show timesheet for a specific week"""
    print(f"[blue]📊 Weekly timesheet for week containing {date or 'today'}:[/blue]")
    print("[yellow]🚧 Command scaffolded - implementation pending[/yellow]")
