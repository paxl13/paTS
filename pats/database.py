"""CSV database utilities for paTS timesheet tracking"""

import csv
from datetime import datetime, timedelta
from pathlib import Path

# CSV file location in user's home directory
DATABASE_FILE = Path.home() / ".pats" / "timesheet.csv"
CSV_HEADERS = ["startTime", "endTime", "date", "project", "description"]


def ensure_database_exists() -> None:
    """Ensure the database directory and file exist with proper headers"""
    DATABASE_FILE.parent.mkdir(exist_ok=True)

    if not DATABASE_FILE.exists():
        with DATABASE_FILE.open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(CSV_HEADERS)


def get_current_time() -> str:
    """Get current time in HH:MM format"""
    return datetime.now().strftime("%H:%M")


def get_current_date() -> str:
    """Get current date in DD-MM-YYYY format"""
    return datetime.now().strftime("%d-%m-%Y")


def parse_datetime_to_time_date(iso_datetime: str) -> tuple[str, str]:
    """Convert ISO datetime string to (time, date) tuple"""
    if not iso_datetime:
        return "", ""

    try:
        dt = datetime.fromisoformat(iso_datetime)
        time_str = dt.strftime("%H:%M")
        date_str = dt.strftime("%d-%m-%Y")
        return time_str, date_str
    except ValueError:
        return "", ""


def combine_time_date_to_datetime(time_str: str, date_str: str) -> datetime:
    """Combine time and date strings into datetime object"""
    if not time_str or not date_str:
        return None

    try:
        # Parse date in DD-MM-YYYY format
        date_parts = date_str.split("-")
        day, month, year = int(date_parts[0]), int(date_parts[1]), int(date_parts[2])

        # Parse time in HH:MM or HH:MM:SS format (support both for migration)
        time_parts = time_str.split(":")
        hour = int(time_parts[0])
        minute = int(time_parts[1])
        second = int(time_parts[2]) if len(time_parts) > 2 else 0

        # Create datetime with local timezone
        dt = datetime(year, month, day, hour, minute, second)
        return dt.replace(tzinfo=datetime.now().astimezone().tzinfo)
    except (ValueError, IndexError):
        return None


def migrate_time_format() -> None:
    """Migrate database from hh:mm:ss to hh:mm time format.

    Converts existing startTime and endTime fields from HH:MM:SS to HH:MM format.
    """
    if not DATABASE_FILE.exists():
        return

    # Read existing data
    with DATABASE_FILE.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        entries = list(reader)

    # Check if migration is needed (look for entries with seconds)
    needs_migration = False
    for entry in entries:
        start_time = entry.get("startTime", "")
        end_time = entry.get("endTime", "")

        # Check if any time has seconds (contains two colons)
        if start_time.count(":") == 2 or end_time.count(":") == 2:
            needs_migration = True
            break

    if not needs_migration:
        return  # Already migrated or no data

    print("🔄 Migrating time format from hh:mm:ss to hh:mm...")

    # Convert entries to new format
    migrated_count = 0
    for entry in entries:
        start_time = entry.get("startTime", "")
        end_time = entry.get("endTime", "")

        # Convert startTime if it has seconds
        if start_time and start_time.count(":") == 2:
            try:
                parts = start_time.split(":")
                entry["startTime"] = f"{parts[0]}:{parts[1]}"
                migrated_count += 1
            except (IndexError, ValueError):
                pass  # Keep original if parsing fails

        # Convert endTime if it has seconds
        if end_time and end_time.count(":") == 2:
            try:
                parts = end_time.split(":")
                entry["endTime"] = f"{parts[0]}:{parts[1]}"
            except (IndexError, ValueError):
                pass  # Keep original if parsing fails

    # Write converted data
    with DATABASE_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
        writer.writeheader()
        writer.writerows(entries)

    print(f"✅ Migrated time format for {migrated_count} time entries")


def migrate_database_format() -> None:
    """Migrate database from old format to new format.

    Converts (startDateTime, endDateTime) to (startTime, endTime, date).
    """
    if not DATABASE_FILE.exists():
        return

    # Read existing data
    with DATABASE_FILE.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        old_entries = list(reader)

    # Check if migration is needed (look for old column names)
    if not old_entries or "startDateTime" not in old_entries[0]:
        return  # Already migrated or empty file

    print("🔄 Migrating database format...")

    # Convert entries to new format
    new_entries = []
    for entry in old_entries:
        start_time, start_date = parse_datetime_to_time_date(
            entry.get("startDateTime", "")
        )
        end_time, end_date = parse_datetime_to_time_date(entry.get("endDateTime", ""))

        # For entries that span multiple days, we'll use the start date
        # This is a simplification - in reality, we might want to split such entries
        date_to_use = start_date if start_date else end_date

        new_entry = {
            "startTime": start_time,
            "endTime": end_time,
            "date": date_to_use,
            "project": entry.get("project", ""),
            "description": entry.get("description", ""),
        }
        new_entries.append(new_entry)

    # Write converted data with new headers
    with DATABASE_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
        writer.writeheader()
        writer.writerows(new_entries)

    print(f"✅ Migrated {len(new_entries)} entries to new format")


def read_entries() -> list[dict[str, str]]:
    """Read all entries from CSV file, ordered from most recent to oldest"""
    ensure_database_exists()
    migrate_database_format()  # Ensure datetime migration is done first
    migrate_time_format()  # Ensure time format migration is done second

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
    """Get the currently active session (entry with no endTime)"""
    entries = read_entries()

    for entry in entries:
        if not entry["endTime"]:  # Empty endTime means active session
            return entry

    return None


def get_previous_session() -> dict[str, str] | None:
    """Get the last completed session (entry with endTime)"""
    entries = read_entries()

    for entry in entries:
        if entry["endTime"]:  # Has endTime means completed session
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

    # Find the first entry with an endTime (most recent completed session)
    for entry in entries:
        if entry["endTime"]:  # Found completed session
            entry["endTime"] = ""  # Remove end time
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

    # Create new entry with current time and date
    new_entry = {
        "startTime": get_current_time(),
        "endTime": "",  # Empty until stopped
        "date": get_current_date(),
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
        if not entry["endTime"]:  # Found active session
            entry["endTime"] = get_current_time()
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
        if not entry["date"] or not entry["startTime"]:
            continue

        try:
            # Combine date and startTime to create datetime for comparison
            entry_datetime = combine_time_date_to_datetime(
                entry["startTime"], entry["date"]
            )
            if entry_datetime is None:
                continue

            # Entry is in range if it starts within the date range
            if start_date <= entry_datetime <= end_date:
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
