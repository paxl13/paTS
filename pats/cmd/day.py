"""Day command for paTS"""

import typer
from rich import print

from pats.database import get_entries_for_day, parse_date_input
from pats.display_utils import display_entries_table


def day(
    date: str | None = typer.Argument(
        None, help="Date in YYYY-MM-DD format (defaults to today)"
    ),
):
    """Show timesheet for a specific day"""
    try:
        # Get entries for the specified day
        entries = get_entries_for_day(date)

        # Format the date for display
        if date:
            target_date = parse_date_input(date, "day")
            date_display = target_date.strftime("%Y-%m-%d")
            title = f"📅 Daily Timesheet - {date_display}"
        else:
            title = "📅 Daily Timesheet - Today"

        display_entries_table(entries, title)

    except ValueError as e:
        print(f"[red]❌ Error: {e}[/red]")
        print("[dim]Expected format: YYYY-MM-DD (e.g., 2024-07-30)[/dim]")
