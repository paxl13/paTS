"""Start command for paTS"""

from typing import Annotated

import typer
from rich import print

from pats.database import get_active_session, get_last_session, start_new_session


def start(
    args: Annotated[
        list[str], typer.Argument(help="Description words, or 'ProjectName:desc'")
    ] = None,
):
    """Start tracking time for a project

    Usage:
    - paTS start new task description     (uses project from last session)
    - paTS start ProjectName:new task description   (sets both project and description)
    """

    project = ""
    description = ""

    # Get project from last session (active or most recent)
    last_session = get_last_session()
    if last_session:
        project = last_session["project"] or ""

    if args:
        # Join all arguments first
        full_text = " ".join(args)

        # Check if it contains a colon (project:description format)
        if ":" in full_text:
            # Split on first colon only
            project, description = full_text.split(":", 1)
            project = project.strip()
            description = description.strip()
        else:
            # All text is description, keep project from last session
            description = full_text

    # Check for active session and auto-stop if needed
    active_session = get_active_session()
    if active_session:
        print("[yellow]⏹️  Stopping active session...[/yellow]")
        print(f"[dim]Previous: {active_session['project'] or 'No project'}[/dim]")

    # Start new session
    start_new_session(project, description)

    print("[green]⏱️  Started time tracking![/green]")
    if project:
        print(f"[blue]Project:[/blue] {project}")
    if description:
        print(f"[blue]Description:[/blue] {description}")

    print("[dim]💾 Session saved to ~/.pats/timesheet.csv[/dim]")
