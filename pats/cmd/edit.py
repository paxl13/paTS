"""Edit command for paTS"""

from typing import Annotated

import typer
from rich import print

from pats.database import edit_first_entry


def edit(
    project: Annotated[str, typer.Argument(help="New project name")] = "",
    description: Annotated[
        list[str], typer.Argument(help="New description words")
    ] = None,
):
    """Edit the first (most recent) entry in the timesheet"""

    # Join description words into a single string
    desc_str = " ".join(description) if description else ""

    # Only update fields that are provided (non-empty)
    project_update = project if project else None
    desc_update = desc_str if desc_str else None

    if edit_first_entry(project_update, desc_update):
        changes = []
        if project_update:
            changes.append(f"project: '{project_update}'")
        if desc_update:
            changes.append(f"description: '{desc_update}'")

        if changes:
            print(f"[green]✓[/green] Updated first entry - {', '.join(changes)}")
        else:
            print(
                "[yellow]![/yellow] No changes made - "
                "both project and description were empty"
            )
    else:
        print("[red]✗[/red] No entries found to edit")
