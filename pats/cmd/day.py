"""Day command for paTS"""

import typer
from rich import print


def day(
    date: str | None = typer.Argument(
        None, help="Date in YYYY-MM-DD format (defaults to today)"
    ),
):
    """Show timesheet for a specific day"""
    print(f"[blue]📅 Daily timesheet for {date or 'today'}:[/blue]")
    print("[yellow]🚧 Command scaffolded - implementation pending[/yellow]")
