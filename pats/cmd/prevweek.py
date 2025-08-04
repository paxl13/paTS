"""Previous week command for paTS"""

from datetime import datetime, timedelta

import typer
from rich import print

from pats.database import get_entries_for_week, get_week_range
from pats.display_utils import display_entries_grouped_by_day


def prevweek(
    weeks_back: int = typer.Argument(
        1, help="Number of weeks back (1 = last week, 2 = two weeks ago, etc.)"
    ),
):
    """Show timesheet for previous weeks"""
    try:
        if weeks_back < 1:
            print("[red]❌ Error: Number of weeks back must be at least 1[/red]")
            return

        # Calculate the target date (N weeks back from today)
        today = datetime.now().date()
        target_date = today - timedelta(weeks=weeks_back)

        # Convert to datetime for compatibility with existing functions
        target_datetime = datetime.combine(target_date, datetime.min.time())

        # Get entries for the calculated week
        target_date_str = target_date.strftime("%Y-%m-%d")
        entries = get_entries_for_week(target_date_str)

        # Format the week range for display
        start_week, end_week = get_week_range(target_datetime)
        week_display = (
            f"{start_week.strftime('%Y-%m-%d')} to {end_week.strftime('%Y-%m-%d')}"
        )

        # Create descriptive title
        if weeks_back == 1:
            week_desc = "Last Week"
        elif weeks_back == 2:
            week_desc = "Two Weeks Ago"
        elif weeks_back == 3:
            week_desc = "Three Weeks Ago"
        else:
            week_desc = f"{weeks_back} Weeks Ago"

        title = f"📊 Weekly Timesheet - {week_desc} ({week_display})"
        display_entries_grouped_by_day(entries, title)

    except ValueError as e:
        print(f"[red]❌ Error: {e}[/red]")
        print("[dim]Usage: paTS prevweek [weeks_back][/dim]")
