"""Resume command for paTS"""

from rich import print

from pats.database import get_previous_session, start_new_session


def resume():
    """Resume tracking time for last tracked project."""

    previous_session = get_previous_session()
    if previous_session:
        project = previous_session["project"] or "Untitled"
        description = previous_session["description"] or ""

        start_new_session(project, description)

        # Display what was resumed
        if description:
            print(f"[green]✓[/green] Resumed: {project} - {description}")
        else:
            print(f"[green]✓[/green] Resumed: {project}")
    else:
        print("[red]✗[/red] No previous session found to resume")
