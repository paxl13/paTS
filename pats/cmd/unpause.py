"""Unpause command for paTS"""

from rich import print

from pats.database import remove_last_session_end_time


def unpause():
    """Remove end time from last session to resume without considering the pause"""

    if remove_last_session_end_time():
        print("[green]✓[/green] Unpaused - removed end time from last session")
    else:
        print("[red]✗[/red] No completed session found to unpause")
