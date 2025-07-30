"""CSV database utilities for paTS timesheet tracking"""

import csv
from datetime import datetime
from pathlib import Path

# CSV file location in user's home directory
DATABASE_FILE = Path.home() / ".pats" / "timesheet.csv"
CSV_HEADERS = ["startDateTime", "endDateTime", "project", "description"]


def ensure_database_exists() -> None:
    """Ensure the database directory and file exist with proper headers"""
    DATABASE_FILE.parent.mkdir(exist_ok=True)

    if not DATABASE_FILE.exists():
        with DATABASE_FILE.open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(CSV_HEADERS)


def get_current_timestamp() -> str:
    """Get current timestamp in ISO 8601 format with local timezone"""
    return datetime.now().astimezone().isoformat()


def read_entries() -> list[dict[str, str]]:
    """Read all entries from CSV file, ordered from most recent to oldest"""
    ensure_database_exists()

    entries = []
    with DATABASE_FILE.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        entries = list(reader)

    return entries


def write_entries(entries: list[dict[str, str]]) -> None:
    """Write all entries to CSV file"""
    ensure_database_exists()

    with DATABASE_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
        writer.writeheader()
        writer.writerows(entries)


def get_active_session() -> dict[str, str] | None:
    """Get the currently active session (entry with no endDateTime)"""
    entries = read_entries()

    for entry in entries:
        if not entry["endDateTime"]:  # Empty endDateTime means active session
            return entry

    return None


def start_new_session(project: str = "", description: str = "") -> None:
    """Start a new time tracking session"""
    entries = read_entries()

    # Stop any active session first
    active_session = get_active_session()
    if active_session:
        stop_active_session()
        entries = read_entries()  # Refresh after stopping

    # Create new entry with current timestamp
    new_entry = {
        "startDateTime": get_current_timestamp(),
        "endDateTime": "",  # Empty until stopped
        "project": project,
        "description": description,
    }

    # Insert at the beginning (most recent first)
    entries.insert(0, new_entry)
    write_entries(entries)


def stop_active_session() -> bool:
    """Stop the currently active session. Returns True if a session was stopped."""
    entries = read_entries()

    for entry in entries:
        if not entry["endDateTime"]:  # Found active session
            entry["endDateTime"] = get_current_timestamp()
            write_entries(entries)
            return True

    return False  # No active session found
