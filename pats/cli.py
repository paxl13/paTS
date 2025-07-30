"""Main CLI interface for paTS (Python Timesheet System)"""

import typer
from rich import print

app = typer.Typer(help="paTS - Python Timesheet System")


@app.command()
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


@app.command()
def stop():
    """Stop the current time tracking session"""
    print("[red]⏹️  Stopping time tracker...[/red]")
    print("[yellow]🚧 Command scaffolded - implementation pending[/yellow]")


@app.command()
def info():
    """Show current tracking session information"""
    print("[cyan]ℹ️  Current session info:[/cyan]")
    print("[yellow]🚧 Command scaffolded - implementation pending[/yellow]")


@app.command()
def day(
    date: str | None = typer.Argument(
        None, help="Date in YYYY-MM-DD format (defaults to today)"
    ),
):
    """Show timesheet for a specific day"""
    print(f"[blue]📅 Daily timesheet for {date or 'today'}:[/blue]")
    print("[yellow]🚧 Command scaffolded - implementation pending[/yellow]")


@app.command()
def week(
    date: str | None = typer.Argument(
        None, help="Date in YYYY-MM-DD format (defaults to current week)"
    ),
):
    """Show timesheet for a specific week"""
    print(f"[blue]📊 Weekly timesheet for week containing {date or 'today'}:[/blue]")
    print("[yellow]🚧 Command scaffolded - implementation pending[/yellow]")


@app.command()
def month(
    date: str | None = typer.Argument(
        None, help="Date in YYYY-MM format (defaults to current month)"
    ),
):
    """Show timesheet for a specific month"""
    print(f"[blue]📈 Monthly timesheet for {date or 'current month'}:[/blue]")
    print("[yellow]🚧 Command scaffolded - implementation pending[/yellow]")


if __name__ == "__main__":
    app()
