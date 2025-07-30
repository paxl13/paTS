"""Display command for paTS"""

from datetime import datetime

from rich import print
from rich.console import Console
from rich.table import Table

from pats.database import get_active_session, read_entries


def format_datetime(iso_string: str) -> str:
    """Format ISO datetime string for display"""
    if not iso_string:
        return "[yellow]Active[/yellow]"

    try:
        dt = datetime.fromisoformat(iso_string)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return iso_string


def calculate_duration(start_time: str, end_time: str) -> str:
    """Calculate duration between start and end times"""
    if not start_time:
        return "-"

    if not end_time:
        # Calculate duration from start to now
        start_dt = datetime.fromisoformat(start_time)
        now_dt = datetime.now().astimezone()
        duration = now_dt - start_dt
    else:
        try:
            start_dt = datetime.fromisoformat(start_time)
            end_dt = datetime.fromisoformat(end_time)
            duration = end_dt - start_dt
        except ValueError:
            return "-"

    # Format duration as hours:minutes
    total_seconds = int(duration.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    if hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"


def display():
    """Display timesheet data in a table format"""
    console = Console()
    entries = read_entries()

    if not entries:
        print("[yellow]📋 No timesheet entries found[/yellow]")
        print("[dim]Use 'paTS start [project]' to begin tracking time[/dim]")
        return

    # Create the table
    table = Table(
        title="📊 Timesheet Entries", show_header=True, header_style="bold magenta"
    )
    table.add_column("Start Time", style="cyan", width=20)
    table.add_column("End Time", style="cyan", width=20)
    table.add_column("Duration", style="green", width=10)
    table.add_column("Project", style="blue", width=20)
    table.add_column("Description", style="white", width=30)

    # Get active session for highlighting
    active_session = get_active_session()

    # Add rows to the table
    for entry in entries:
        start_formatted = format_datetime(entry["startDateTime"])
        end_formatted = format_datetime(entry["endDateTime"])
        duration = calculate_duration(entry["startDateTime"], entry["endDateTime"])
        project = entry["project"] or "[dim]No project[/dim]"
        description = entry["description"] or "[dim]No description[/dim]"

        # Highlight active session
        if active_session and entry == active_session:
            table.add_row(
                f"[bold]{start_formatted}[/bold]",
                f"[bold yellow]{end_formatted}[/bold yellow]",
                f"[bold green]{duration}[/bold green]",
                f"[bold]{project}[/bold]",
                f"[bold]{description}[/bold]",
            )
        else:
            table.add_row(
                start_formatted, end_formatted, duration, project, description
            )

    console.print(table)

    # Show summary
    total_entries = len(entries)
    active_count = 1 if active_session else 0
    completed_count = total_entries - active_count

    print(
        f"\n[dim]Total entries: {total_entries} | "
        f"Completed: {completed_count} | "
        f"Active: {active_count}[/dim]"
    )
