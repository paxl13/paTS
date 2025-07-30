"""Display command for paTS"""

from pats.database import read_entries
from pats.display_utils import display_entries_table


def display():
    """Display timesheet data in a table format"""
    entries = read_entries()
    display_entries_table(entries, "📊 Timesheet Entries")
