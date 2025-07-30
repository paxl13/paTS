"""Stop command for paTS"""

from rich import print

from pats.database import get_active_session, stop_active_session


def stop():
    """Stop the current time tracking session"""
    # Check if there's an active session
    active_session = get_active_session()
    if not active_session:
        print("[yellow]⚠️  No active time tracking session found[/yellow]")
        print("[dim]Use 'paTS start [project]' to begin tracking time[/dim]")
        return

    # Stop the active session
    success = stop_active_session()
    if success:
        print("[red]⏹️  Stopped time tracking![/red]")
        project = active_session["project"]
        description = active_session["description"]

        if project:
            print(f"[blue]Project:[/blue] {project}")
        if description:
            print(f"[blue]Description:[/blue] {description}")

        print("[dim]💾 Session completed and saved to ~/.pats/timesheet.csv[/dim]")
    else:
        print("[red]❌ Failed to stop session[/red]")
