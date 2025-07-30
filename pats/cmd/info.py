"""Info command for paTS"""

from datetime import datetime

from pats.database import get_active_session


def calculate_compact_duration(start_time: str) -> str:
    """Calculate duration in compact format for status bar"""
    try:
        start_dt = datetime.fromisoformat(start_time)
        now_dt = datetime.now().astimezone()
        duration = now_dt - start_dt

        total_seconds = int(duration.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        if hours > 0:
            return f"{hours}h{minutes}m"
        else:
            return f"{minutes}m"
    except (ValueError, TypeError):
        return "0m"


def truncate_text(text: str, max_length: int) -> str:
    """Truncate text to fit within max length"""
    if len(text) <= max_length:
        return text
    return text[: max_length - 1] + "…"


def info():
    """Show current tracking session information (compact format for tmux)"""
    active_session = get_active_session()

    if not active_session:
        print("⏸")
        return

    # Get project and description
    project = active_session.get("project", "").strip()
    description = active_session.get("description", "").strip()

    # Calculate duration
    duration = calculate_compact_duration(active_session.get("startDateTime", ""))

    # Build compact display
    if project and description:
        # Show both project and description, truncated
        task_info = f"{project}: {description}"
        task_info = truncate_text(task_info, 25)  # Leave room for duration
    elif project:
        # Show just project
        task_info = truncate_text(project, 25)
    elif description:
        # Show just description
        task_info = truncate_text(description, 25)
    else:
        # No project or description
        task_info = "Work"

    # Output compact format: ⏱ [task] [duration]
    print(f"⏱ {task_info} {duration}")
