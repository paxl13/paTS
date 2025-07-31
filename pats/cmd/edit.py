"""Edit command for paTS"""

from typing import Annotated

import typer
from rich import print

from pats.database import edit_first_entry


def edit(
    args: Annotated[
        list[str], typer.Argument(help="Description words, or 'ProjectName:desc'")
    ] = None,
):
    """Edit the first (most recent) entry in the timesheet

    Usage:
    - paTS edit new description here     (updates description only)
    - paTS edit ProjectName:new description here   (updates both)
    """

    if not args:
        print("[yellow]![/yellow] No arguments provided - nothing to update")
        return

    project_update = None
    desc_update = None

    # Join all arguments first
    full_text = " ".join(args)

    # Check if it contains a colon (project:description format)
    if ":" in full_text:
        # Split on first colon only
        project_update, desc_update = full_text.split(":", 1)
        project_update = project_update.strip()
        desc_update = desc_update.strip()
    else:
        # All text is description
        desc_update = full_text

    if edit_first_entry(project_update, desc_update if desc_update else None):
        changes = []
        if project_update:
            changes.append(f"project: '{project_update}'")
        if desc_update:
            changes.append(f"description: '{desc_update}'")

        if changes:
            print(f"[green]✓[/green] Updated first entry - {', '.join(changes)}")
        else:
            print("[yellow]![/yellow] No changes made - arguments were empty")
    else:
        print("[red]✗[/red] No entries found to edit")
