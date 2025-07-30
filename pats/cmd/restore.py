"""Restore command for paTS"""

import shutil
from pathlib import Path
from typing import Annotated

import typer
from rich import print

from pats.database import DATABASE_FILE


def restore(
    backup_path: Annotated[
        str, typer.Argument(help="Path to backup file to restore")
    ] = "",
    force: Annotated[
        bool, typer.Option("--force", "-f", help="Overwrite without confirmation")
    ] = False,
):
    """Restore timesheet data from a backup file"""
    # Determine backup path
    if backup_path:
        backup_file = Path(backup_path)
    else:
        # Default backup location: same directory as CSV with .backup extension
        backup_file = DATABASE_FILE.with_suffix(".csv.backup")

    # Check if backup file exists
    if not backup_file.exists():
        print(f"[red]❌ Backup file not found: {backup_file}[/red]")
        if not backup_path:
            print("[dim]Try specifying a custom backup path as an argument[/dim]")
        raise typer.Exit(1)

    # Check if current database exists and warn user
    if DATABASE_FILE.exists() and not force:
        print("[yellow]⚠️  Current timesheet database will be overwritten![/yellow]")
        print(f"[dim]Current: {DATABASE_FILE}[/dim]")
        print(f"[dim]Backup:  {backup_file}[/dim]")

        # Show current file info
        current_size = DATABASE_FILE.stat().st_size
        backup_size = backup_file.stat().st_size

        if current_size < 1024:
            current_size_str = f"{current_size} bytes"
        elif current_size < 1024 * 1024:
            current_size_str = f"{current_size / 1024:.1f} KB"
        else:
            current_size_str = f"{current_size / (1024 * 1024):.1f} MB"

        if backup_size < 1024:
            backup_size_str = f"{backup_size} bytes"
        elif backup_size < 1024 * 1024:
            backup_size_str = f"{backup_size / 1024:.1f} KB"
        else:
            backup_size_str = f"{backup_size / (1024 * 1024):.1f} MB"

        print(
            f"[dim]Current size: {current_size_str} | "
            f"Backup size: {backup_size_str}[/dim]"
        )

        confirm = typer.confirm("Are you sure you want to continue?")
        if not confirm:
            print("[dim]Restore cancelled[/dim]")
            return

    try:
        # Ensure the database directory exists
        DATABASE_FILE.parent.mkdir(parents=True, exist_ok=True)

        # Copy the backup file to database location
        shutil.copy2(backup_file, DATABASE_FILE)

        print("[green]✅ Restore completed successfully![/green]")
        print(f"[blue]Backup:[/blue] {backup_file}")
        print(f"[blue]Restored to:[/blue] {DATABASE_FILE}")

        # Show restored file size for confirmation
        size_bytes = DATABASE_FILE.stat().st_size
        if size_bytes < 1024:
            size_str = f"{size_bytes} bytes"
        elif size_bytes < 1024 * 1024:
            size_str = f"{size_bytes / 1024:.1f} KB"
        else:
            size_str = f"{size_bytes / (1024 * 1024):.1f} MB"

        print(f"[dim]Restored size: {size_str}[/dim]")

    except Exception as e:
        print(f"[red]❌ Failed to restore backup: {e}[/red]")
        raise typer.Exit(1) from e
