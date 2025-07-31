"""Week command for paTS"""

import typer
from rich import print

from pats.database import get_entries_for_week, get_week_range, parse_date_input
from pats.display_utils import display_entries_grouped_by_day


def week(
    date: str | None = typer.Argument(
        None, help="Date in YYYY-MM-DD format (defaults to current week)"
    ),
):
    """Show timesheet for a specific week"""
    try:
        # Get entries for the specified week
        entries = get_entries_for_week(date)

        # Format the week range for display
        if date:
            target_date = parse_date_input(date, "week")
        else:
            target_date = parse_date_input(None, "week")

        start_week, end_week = get_week_range(target_date)
        week_display = (
            f"{start_week.strftime('%Y-%m-%d')} to {end_week.strftime('%Y-%m-%d')}"
        )
        title = f"📊 Weekly Timesheet - {week_display}"

        display_entries_grouped_by_day(entries, title)

    except ValueError as e:
        print(f"[red]❌ Error: {e}[/red]")
        print("[dim]Expected format: YYYY-MM-DD (e.g., 2024-07-30)[/dim]")
