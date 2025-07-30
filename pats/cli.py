"""Main CLI interface for paTS (Python Timesheet System)"""

import typer

from pats.cmd.day import day
from pats.cmd.display import display
from pats.cmd.info import info
from pats.cmd.month import month
from pats.cmd.start import start
from pats.cmd.stop import stop
from pats.cmd.week import week

app = typer.Typer(help="paTS - Python Timesheet System")

# Register commands
app.command()(start)
app.command()(stop)
app.command()(info)
app.command()(display)
app.command()(day)
app.command()(week)
app.command()(month)


if __name__ == "__main__":
    app()
