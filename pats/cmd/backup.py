"""Backup command for paTS"""

import shutil
from pathlib import Path
from typing import Annotated

import typer
from rich import print

from pats.database import DATABASE_FILE


def backup(
    backup_path: Annotated[str, typer.Argument(help="Path to save backup file")] = "",
):
    """Backup timesheet data to a file"""
    # Ensure the database exists
    if not DATABASE_FILE.exists():
        print("[yellow]⚠️  No timesheet database found to backup[/yellow]")
        print(f"[dim]Expected location: {DATABASE_FILE}[/dim]")
        return

    # Determine backup path
    if backup_path:
        backup_file = Path(backup_path)
    else:
        # Default backup location: same directory as CSV with .backup extension
        backup_file = DATABASE_FILE.with_suffix(".csv.backup")

    try:
        # Create backup directory if it doesn't exist
        backup_file.parent.mkdir(parents=True, exist_ok=True)

        # Copy the database file to backup location
        shutil.copy2(DATABASE_FILE, backup_file)

        print("[green]✅ Backup created successfully![/green]")
        print(f"[blue]Source:[/blue] {DATABASE_FILE}")
        print(f"[blue]Backup:[/blue] {backup_file}")

        # Show file size for confirmation
        size_bytes = backup_file.stat().st_size
        if size_bytes < 1024:
            size_str = f"{size_bytes} bytes"
        elif size_bytes < 1024 * 1024:
            size_str = f"{size_bytes / 1024:.1f} KB"
        else:
            size_str = f"{size_bytes / (1024 * 1024):.1f} MB"

        print(f"[dim]Backup size: {size_str}[/dim]")

    except Exception as e:
        print(f"[red]❌ Failed to create backup: {e}[/red]")
        raise typer.Exit(1) from e
