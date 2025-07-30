"""Start command for paTS"""

import typer
from rich import print

from pats.database import get_active_session, start_new_session


def start(
    project: str | None = typer.Argument(None, help="Project name to start tracking"),
    description: str | None = typer.Option(
        None, "--desc", "-d", help="Description of the work"
    ),
):
    """Start tracking time for a project"""
    # Check for active session and auto-stop if needed
    active_session = get_active_session()
    if active_session:
        print("[yellow]⏹️  Stopping active session...[/yellow]")
        print(f"[dim]Previous: {active_session['project'] or 'No project'}[/dim]")

    # Start new session
    start_new_session(project or "", description or "")

    print("[green]⏱️  Started time tracking![/green]")
    if project:
        print(f"[blue]Project:[/blue] {project}")
    if description:
        print(f"[blue]Description:[/blue] {description}")

    print("[dim]💾 Session saved to ~/.pats/timesheet.csv[/dim]")
