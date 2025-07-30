"""Month command for paTS"""

import typer
from rich import print

from pats.database import get_entries_for_month, parse_date_input
from pats.display_utils import display_entries_table


def month(
    date: str | None = typer.Argument(
        None, help="Date in YYYY-MM format (defaults to current month)"
    ),
):
    """Show timesheet for a specific month"""
    try:
        # Get entries for the specified month
        entries = get_entries_for_month(date)

        # Format the month for display
        if date:
            target_date = parse_date_input(date, "month")
            month_display = target_date.strftime("%Y-%m")
            title = f"📈 Monthly Timesheet - {month_display}"
        else:
            target_date = parse_date_input(None, "month")
            month_display = target_date.strftime("%Y-%m")
            title = f"📈 Monthly Timesheet - {month_display}"

        display_entries_table(entries, title)

    except ValueError as e:
        print(f"[red]❌ Error: {e}[/red]")
        print("[dim]Expected format: YYYY-MM (e.g., 2024-07)[/dim]")
