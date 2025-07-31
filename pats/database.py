"""CSV database utilities for paTS timesheet tracking"""

import csv
from datetime import datetime, timedelta
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


def get_previous_session() -> dict[str, str] | None:
    """Get the last active session (entry with no endDateTime)"""
    entries = read_entries()

    for entry in entries:
        if entry["endDateTime"]:  # Empty endDateTime means active session
            return entry

    return None


def get_last_session() -> dict[str, str] | None:
    """Get the most recent session (active or completed)"""
    entries = read_entries()

    if entries:
        return entries[0]  # First entry is most recent

    return None


def remove_last_session_end_time() -> bool:
    """Remove the end time from the last completed session.

    Returns True if a session was modified.
    """
    entries = read_entries()

    # Find the first entry with an endDateTime (most recent completed session)
    for entry in entries:
        if entry["endDateTime"]:  # Found completed session
            entry["endDateTime"] = ""  # Remove end time
            write_entries(entries)
            return True

    return False  # No completed session found


def delete_first_entry() -> dict[str, str] | None:
    """Delete the first entry (most recent) from the CSV.

    Returns the deleted entry if successful, None if no entries found.
    """
    entries = read_entries()

    if entries:
        deleted_entry = entries.pop(0)  # Remove first entry (most recent)
        write_entries(entries)
        return deleted_entry

    return None  # No entries found


def edit_first_entry(
    project: str | None = None, description: str | None = None
) -> bool:
    """Edit the first entry (most recent) in the CSV.

    Returns True if an entry was edited.
    """
    entries = read_entries()

    if entries:
        first_entry = entries[0]

        # Update project if provided
        if project is not None:
            first_entry["project"] = project

        # Update description if provided
        if description is not None:
            first_entry["description"] = description

        write_entries(entries)
        return True

    return False  # No entries found


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


def parse_date_input(date_str: str | None, format_type: str) -> datetime:
    """Parse date input string and return datetime object"""
    if not date_str:
        return datetime.now().astimezone()

    try:
        if format_type == "day":
            # Expect YYYY-MM-DD format
            return datetime.strptime(date_str, "%Y-%m-%d").replace(
                tzinfo=datetime.now().astimezone().tzinfo
            )
        elif format_type == "month":
            # Expect YYYY-MM format
            return datetime.strptime(date_str, "%Y-%m").replace(
                tzinfo=datetime.now().astimezone().tzinfo
            )
        elif format_type == "week":
            # Expect YYYY-MM-DD format (any day in the week)
            return datetime.strptime(date_str, "%Y-%m-%d").replace(
                tzinfo=datetime.now().astimezone().tzinfo
            )
    except ValueError as e:
        expected_format = "YYYY-MM-DD" if format_type != "month" else "YYYY-MM"
        raise ValueError(
            f"Invalid date format. Expected format for {format_type}: {expected_format}"
        ) from e

    return datetime.now().astimezone()


def get_day_range(date: datetime) -> tuple[datetime, datetime]:
    """Get start and end of day for given date"""
    start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = date.replace(hour=23, minute=59, second=59, microsecond=999999)
    return start_of_day, end_of_day


def get_week_range(date: datetime) -> tuple[datetime, datetime]:
    """Get start (Monday) and end (Sunday) of week for given date"""
    # Get Monday of the week (weekday() returns 0 for Monday)
    days_since_monday = date.weekday()
    start_of_week = (date - timedelta(days=days_since_monday)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    end_of_week = (start_of_week + timedelta(days=6)).replace(
        hour=23, minute=59, second=59, microsecond=999999
    )
    return start_of_week, end_of_week


def get_month_range(date: datetime) -> tuple[datetime, datetime]:
    """Get start and end of month for given date"""
    start_of_month = date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Get last day of month
    if date.month == 12:
        next_month = date.replace(year=date.year + 1, month=1, day=1)
    else:
        next_month = date.replace(month=date.month + 1, day=1)

    end_of_month = (next_month - timedelta(days=1)).replace(
        hour=23, minute=59, second=59, microsecond=999999
    )
    return start_of_month, end_of_month


def filter_entries_by_date_range(
    entries: list[dict[str, str]], start_date: datetime, end_date: datetime
) -> list[dict[str, str]]:
    """Filter entries that fall within the given date range"""
    filtered_entries = []

    for entry in entries:
        if not entry["startDateTime"]:
            continue

        try:
            entry_start = datetime.fromisoformat(entry["startDateTime"])

            # Entry is in range if it starts within the date range
            if start_date <= entry_start <= end_date:
                filtered_entries.append(entry)

        except ValueError:
            # Skip entries with invalid timestamps
            continue

    return filtered_entries


def get_entries_for_day(date_str: str | None = None) -> list[dict[str, str]]:
    """Get entries for a specific day"""
    target_date = parse_date_input(date_str, "day")
    start_date, end_date = get_day_range(target_date)
    entries = read_entries()
    return filter_entries_by_date_range(entries, start_date, end_date)


def get_entries_for_week(date_str: str | None = None) -> list[dict[str, str]]:
    """Get entries for a specific week"""
    target_date = parse_date_input(date_str, "week")
    start_date, end_date = get_week_range(target_date)
    entries = read_entries()
    return filter_entries_by_date_range(entries, start_date, end_date)


def get_entries_for_month(date_str: str | None = None) -> list[dict[str, str]]:
    """Get entries for a specific month"""
    target_date = parse_date_input(date_str, "month")
    start_date, end_date = get_month_range(target_date)
    entries = read_entries()
    return filter_entries_by_date_range(entries, start_date, end_date)
