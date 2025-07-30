"""Month command for paTS"""

import typer
from rich import print


def month(
    date: str | None = typer.Argument(
        None, help="Date in YYYY-MM format (defaults to current month)"
    ),
):
    """Show timesheet for a specific month"""
    print(f"[blue]📈 Monthly timesheet for {date or 'current month'}:[/blue]")
    print("[yellow]🚧 Command scaffolded - implementation pending[/yellow]")
