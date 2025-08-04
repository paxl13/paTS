"""Display utilities for paTS commands"""

from datetime import datetime

from rich import print
from rich.console import Console
from rich.table import Table

from pats.database import combine_time_date_to_datetime, get_active_session


def format_time_display(
    time_str: str, date_str: str = "", show_date: bool = True
) -> str:
    """Format time and date strings for display"""
    if not time_str:
        return "[yellow]Active[/yellow]"

    if show_date and date_str:
        # Convert DD-MM-YYYY to YYYY-MM-DD for display
        try:
            date_parts = date_str.split("-")
            formatted_date = f"{date_parts[2]}-{date_parts[1]}-{date_parts[0]}"
            return f"{formatted_date} {time_str}"
        except (IndexError, ValueError):
            return f"{date_str} {time_str}"
    else:
        return time_str


def calculate_duration_seconds(entry: dict[str, str]) -> int:
    """Calculate duration for an entry in seconds"""
    start_time = entry.get("startTime", "")
    end_time = entry.get("endTime", "")
    date_str = entry.get("date", "")

    if not start_time or not date_str:
        return 0

    try:
        start_dt = combine_time_date_to_datetime(start_time, date_str)
        if start_dt is None:
            return 0

        if not end_time:
            # Calculate duration from start to now (active session)
            now_dt = datetime.now().astimezone()
            duration = now_dt - start_dt
        else:
            # Calculate duration between start and end
            end_dt = combine_time_date_to_datetime(end_time, date_str)
            if end_dt is None:
                return 0
            duration = end_dt - start_dt

        return int(duration.total_seconds())
    except (ValueError, TypeError):
        return 0


def calculate_duration(entry: dict[str, str]) -> str:
    """Calculate duration for an entry"""
    total_seconds = calculate_duration_seconds(entry)

    if total_seconds == 0:
        return "-"

    # Format duration as hours:minutes
    hours, remainder = divmod(total_seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    if hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"


def format_total_duration(total_seconds: int) -> str:
    """Format total duration seconds into readable format"""
    if total_seconds == 0:
        return "0m"

    hours, remainder = divmod(total_seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    if hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"


def display_entries_table(
    entries: list[dict[str, str]], title: str = "📊 Timesheet Entries"
) -> None:
    """Display entries in a formatted table"""
    console = Console()

    if not entries:
        print("[yellow]📋 No timesheet entries found for the specified period[/yellow]")
        print("[dim]Use 'paTS start [project]' to begin tracking time[/dim]")
        return

    # Check if all entries are from today
    today = datetime.now().strftime("%d-%m-%Y")
    is_today_only = True
    for entry in entries:
        if entry["date"] and entry["date"] != today:
            is_today_only = False
            break

    # Create the table
    table = Table(title=title, show_header=True, header_style="bold magenta")
    start_column_width = 12 if is_today_only else 20
    end_column_width = 12 if is_today_only else 20
    table.add_column("Start Time", style="cyan", width=start_column_width)
    table.add_column("End Time", style="cyan", width=end_column_width)
    table.add_column("Duration", style="green", width=10)
    table.add_column("Project", style="blue", width=20)
    table.add_column("Description", style="white", width=30)

    # Get active session for highlighting
    active_session = get_active_session()

    # Add rows to the table with compacting logic
    prev_project = None
    prev_description = None

    for entry in entries:
        show_date = not is_today_only
        start_formatted = format_time_display(
            entry["startTime"], entry["date"], show_date=show_date
        )
        end_formatted = format_time_display(
            entry["endTime"], entry["date"], show_date=show_date
        )
        duration = calculate_duration(entry)

        # Get current project and description
        current_project = entry["project"] or "[dim]No project[/dim]"
        current_description = entry["description"] or "[dim]No description[/dim]"

        # Compact display: hide if same as previous row
        display_project = current_project if current_project != prev_project else ""
        display_description = (
            current_description if current_description != prev_description else ""
        )

        # Highlight active session
        if active_session and entry == active_session:
            table.add_row(
                f"[bold]{start_formatted}[/bold]",
                f"[bold yellow]{end_formatted}[/bold yellow]",
                f"[bold green]{duration}[/bold green]",
                f"[bold]{display_project}[/bold]",
                f"[bold]{display_description}[/bold]",
            )
        else:
            table.add_row(
                start_formatted,
                end_formatted,
                duration,
                display_project,
                display_description,
            )

        # Update previous values for next iteration
        prev_project = current_project
        prev_description = current_description

    console.print(table)

    # Calculate total time
    total_time_seconds = 0
    for entry in entries:
        entry_duration = calculate_duration_seconds(entry)
        total_time_seconds += entry_duration

    # Show summary
    total_entries = len(entries)
    active_count = 1 if active_session and active_session in entries else 0
    completed_count = total_entries - active_count
    total_time_formatted = format_total_duration(total_time_seconds)

    # Calculate project totals
    project_totals = {}
    for entry in entries:
        project = entry["project"] or "No project"
        entry_duration = calculate_duration_seconds(entry)
        if project in project_totals:
            project_totals[project] += entry_duration
        else:
            project_totals[project] = entry_duration

    # Display project totals
    if project_totals:
        print("\n[bold]Time by Project:[/bold]")
        for project, seconds in sorted(
            project_totals.items(), key=lambda x: x[1], reverse=True
        ):
            formatted_time = format_total_duration(seconds)
            print(f"  [blue]{project}:[/blue] [green]{formatted_time}[/green]")

    print(
        f"\n[dim]Total entries: {total_entries} | "
        f"Completed: {completed_count} | "
        f"Active: {active_count} | "
        f"Total time: [/dim][green]{total_time_formatted}[/green]"
    )


def display_entries_grouped_by_day(
    entries: list[dict[str, str]], title: str = "📊 Weekly Timesheet"
) -> None:
    """Display entries grouped by day"""
    console = Console()

    if not entries:
        print("[yellow]📋 No timesheet entries found for the specified period[/yellow]")
        print("[dim]Use 'paTS start [project]' to begin tracking time[/dim]")
        return

    # Group entries by date
    entries_by_date = {}
    for entry in entries:
        if entry["date"]:
            # Convert DD-MM-YYYY to YYYY-MM-DD for sorting
            try:
                date_parts = entry["date"].split("-")
                if len(date_parts) == 3:
                    sort_key = f"{date_parts[2]}-{date_parts[1]}-{date_parts[0]}"
                    if sort_key not in entries_by_date:
                        entries_by_date[sort_key] = []
                    entries_by_date[sort_key].append(entry)
            except (ValueError, IndexError):
                continue

    # Sort dates
    sorted_dates = sorted(entries_by_date.keys(), reverse=True)

    # Get active session for highlighting
    active_session = get_active_session()

    # Calculate total time across all days
    total_time_seconds = 0
    total_entries_count = 0

    console.print(f"[bold magenta]{title}[/bold magenta]", justify="center")
    print()

    for date_str in sorted_dates:
        day_entries = entries_by_date[date_str]

        # Format day header
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            day_name = date_obj.strftime("%A")
            formatted_date = date_obj.strftime("%B %d, %Y")
            day_header = f"📅 {day_name}, {formatted_date}"
        except ValueError:
            day_header = f"📅 {date_str}"

        # Create table for this day
        table = Table(show_header=True, header_style="bold cyan", width=100)
        table.add_column("Start", style="cyan", width=12)
        table.add_column("End", style="cyan", width=12)
        table.add_column("Duration", style="green", width=10)
        table.add_column("Project", style="blue", width=20)
        table.add_column("Description", style="white", width=30)

        # Calculate daily total
        daily_total_seconds = 0

        # Add rows for this day with compacting logic
        day_prev_project = None
        day_prev_description = None

        for entry in day_entries:
            start_formatted = format_time_display(entry["startTime"], show_date=False)
            end_formatted = format_time_display(entry["endTime"], show_date=False)
            duration = calculate_duration(entry)

            # Get current project and description
            current_project = entry["project"] or "[dim]No project[/dim]"
            current_description = entry["description"] or "[dim]No description[/dim]"

            # Compact display: hide if same as previous row within this day
            display_project = (
                current_project if current_project != day_prev_project else ""
            )
            display_description = (
                current_description
                if current_description != day_prev_description
                else ""
            )

            # Calculate duration for daily total
            entry_duration = calculate_duration_seconds(entry)
            daily_total_seconds += entry_duration

            # Highlight active session
            if active_session and entry == active_session:
                table.add_row(
                    f"[bold]{start_formatted}[/bold]",
                    f"[bold yellow]{end_formatted}[/bold yellow]",
                    f"[bold green]{duration}[/bold green]",
                    f"[bold]{display_project}[/bold]",
                    f"[bold]{display_description}[/bold]",
                )
            else:
                table.add_row(
                    start_formatted,
                    end_formatted,
                    duration,
                    display_project,
                    display_description,
                )

            # Update previous values for next iteration within this day
            day_prev_project = current_project
            day_prev_description = current_description

        # Print left-aligned day header and table
        print(f"[bold blue]{day_header}[/bold blue]")
        console.print(table)

        # Calculate daily project totals
        daily_project_totals = {}
        for entry in day_entries:
            project = entry["project"] or "No project"
            entry_duration = calculate_duration_seconds(entry)
            if project in daily_project_totals:
                daily_project_totals[project] += entry_duration
            else:
                daily_project_totals[project] = entry_duration

        # Print daily project breakdown
        if daily_project_totals:
            project_breakdown = []
            for project, seconds in sorted(
                daily_project_totals.items(), key=lambda x: x[1], reverse=True
            ):
                formatted_time = format_total_duration(seconds)
                project_breakdown.append(f"{project}: {formatted_time}")
            print(f"[dim]  Projects: {' | '.join(project_breakdown)}[/dim]")

        # Print daily summary
        daily_total_formatted = format_total_duration(daily_total_seconds)
        active_count = 1 if active_session and active_session in day_entries else 0
        completed_count = len(day_entries) - active_count

        print(
            f"[dim]Daily total: [/dim][green]{daily_total_formatted}[/green] "
            f"[dim]({len(day_entries)} entries: {completed_count} completed, "
            f"{active_count} active)[/dim]\n"
        )

        # Add to overall totals
        total_time_seconds += daily_total_seconds
        total_entries_count += len(day_entries)

    # Calculate overall project totals
    overall_project_totals = {}
    for entry in entries:
        project = entry["project"] or "No project"
        entry_duration = calculate_duration_seconds(entry)
        if project in overall_project_totals:
            overall_project_totals[project] += entry_duration
        else:
            overall_project_totals[project] = entry_duration

    # Show overall project breakdown
    if overall_project_totals:
        print("[bold]Week Summary by Project:[/bold]")
        for project, seconds in sorted(
            overall_project_totals.items(), key=lambda x: x[1], reverse=True
        ):
            formatted_time = format_total_duration(seconds)
            print(f"  [blue]{project}:[/blue] [green]{formatted_time}[/green]")

    # Show overall summary
    total_time_formatted = format_total_duration(total_time_seconds)
    print(
        f"\n[bold]Total:[/bold] [green]{total_time_formatted}[/green] "
        f"[dim]({total_entries_count} total entries)[/dim]"
    )
