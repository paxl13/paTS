"""Delete command for paTS"""

import typer
from rich import print

from pats.database import delete_first_entry, read_entries


def del_():
    """Delete the first (most recent) entry from the timesheet"""

    # First, check if there are any entries and show what would be deleted
    entries = read_entries()
    if not entries:
        print("[red]✗[/red] No entries found to delete")
        return

    # Show what will be deleted
    first_entry = entries[0]
    project = first_entry["project"] or "Untitled"
    description = first_entry["description"] or ""

    entry_display = f"{project} - {description}" if description else project

    print(f"[yellow]About to delete:[/yellow] {entry_display}")

    # Ask for confirmation
    confirm = typer.confirm("Are you sure you want to delete this entry?")
    if not confirm:
        print("[blue]✗[/blue] Deletion cancelled")
        return

    # Proceed with deletion
    deleted_entry = delete_first_entry()
    if deleted_entry:
        print(f"[green]✓[/green] Deleted: {entry_display}")
    else:
        print("[red]✗[/red] Failed to delete entry")
