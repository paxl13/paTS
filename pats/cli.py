"""Main CLI interface for paTS (Python Timesheet System)"""

from typing import Any

import typer

from pats.cmd.backup import backup
from pats.cmd.day import day
from pats.cmd.delete import del_
from pats.cmd.display import display
from pats.cmd.edit import edit
from pats.cmd.info import info
from pats.cmd.month import month
from pats.cmd.prevweek import prevweek
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


cmds: dict[Any, list[str]] = {
    start: [],
    stop: [],
    info: [],
    display: [],
    day: [],
    week: [],
    prevweek: [],
    month: [],
    backup: [],
    restore: [],
    resume: [],
    unpause: [],
    del_: ["del"],
    edit: ["e"],
}

for fn, names in cmds.items():
    app.command()(fn)
    for n in names:
        app.command(n)(fn)


if __name__ == "__main__":
    app()
