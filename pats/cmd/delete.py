"""Delete command for paTS"""

from rich import print

from pats.database import delete_first_entry


def del_():
    """Delete the first (most recent) entry from the timesheet"""

    if delete_first_entry():
        print("[green]✓[/green] Deleted first entry from timesheet")
    else:
        print("[red]✗[/red] No entries found to delete")
