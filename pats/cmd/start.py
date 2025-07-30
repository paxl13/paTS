"""Start command for paTS"""

from typing import Annotated

import typer
from rich import print

from pats.database import get_active_session, start_new_session


def start(
    project: Annotated[str, typer.Argument(help="Project name")] = "",
    description_words: Annotated[
        list[str], typer.Argument(help="Description words")
    ] = None,
):
    """Start tracking time for a project. Usage: paTS start [project] [desc...]"""
    # Join description words into a single string
    description = " ".join(description_words) if description_words else ""

    # Check for active session and auto-stop if needed
    active_session = get_active_session()
    if active_session:
        print("[yellow]⏹️  Stopping active session...[/yellow]")
        print(f"[dim]Previous: {active_session['project'] or 'No project'}[/dim]")

    # Start new session
    start_new_session(project or "", description)

    print("[green]⏱️  Started time tracking![/green]")
    if project:
        print(f"[blue]Project:[/blue] {project}")
    if description:
        print(f"[blue]Description:[/blue] {description}")

    print("[dim]💾 Session saved to ~/.pats/timesheet.csv[/dim]")
