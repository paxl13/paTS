"""Main CLI interface for paTS (Python Timesheet System)"""

import typer

from pats.cmd.backup import backup
from pats.cmd.day import day
from pats.cmd.delete import del_
from pats.cmd.display import display
from pats.cmd.edit import edit
from pats.cmd.info import info
from pats.cmd.month import month
from pats.cmd.restore import restore
from pats.cmd.resume import resume
from pats.cmd.start import start
from pats.cmd.stop import stop
from pats.cmd.unpause import unpause
from pats.cmd.week import week

app = typer.Typer(help="paTS - Python Timesheet System", invoke_without_command=True)


@app.callback()
def default_command(ctx: typer.Context):
    """Show timesheet for today (default command). Use 'paTS day [date]' for dates."""
    if ctx.invoked_subcommand is None:
        # No subcommand was called, run day command as default with no arguments
        day(None)


# Register commands
app.command()(start)
app.command()(stop)
app.command()(info)
app.command()(display)
app.command()(day)
app.command()(week)
app.command()(month)
app.command()(backup)
app.command()(restore)
app.command()(resume)
app.command()(unpause)
app.command("del")(del_)
app.command()(edit)


if __name__ == "__main__":
    app()
