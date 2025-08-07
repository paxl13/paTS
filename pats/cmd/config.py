"""Config command for paTS"""

import typer
from rich import print

from pats.config import (
    load_config,
    set_daily_goal_hours,
    set_excluded_projects,
    set_weekly_goal_hours,
)

app = typer.Typer(help="Manage paTS configuration")


@app.command("set-excluded-projects")
def set_excluded_projects_cmd(projects: list[str]):
    """Set projects to exclude from total time calculations"""
    try:
        set_excluded_projects(projects)
        if projects:
            projects_str = ", ".join(f"'{p}'" for p in projects)
            print(f"[green]✅ Excluded projects set to: {projects_str}[/green]")
        else:
            print("[green]✅ Excluded projects list cleared[/green]")
    except Exception as e:
        print(f"[red]❌ Error setting excluded projects: {e}[/red]")


@app.command()
def show():
    """Show current configuration"""
    try:
        config = load_config()
        excluded_projects = config.get("excluded_projects", [])
        daily_goal = config.get("daily_goal_hours", 8.0)
        weekly_goal = config.get("weekly_goal_hours", 40.0)

        print("[bold]📋 Current Configuration:[/bold]")
        print()

        print("[bold]Time Goals:[/bold]")
        print(f"  Daily Goal: [blue]{daily_goal}h[/blue]")
        print(f"  Weekly Goal: [blue]{weekly_goal}h[/blue]")
        print()

        if excluded_projects:
            print("[bold]Excluded Projects:[/bold]")
            for project in excluded_projects:
                print(f"  • [red]{project}[/red]")
        else:
            print("[dim]No projects excluded from totals[/dim]")

    except Exception as e:
        print(f"[red]❌ Error loading configuration: {e}[/red]")


@app.command()
def clear_excluded_projects():
    """Clear all excluded projects"""
    try:
        set_excluded_projects([])
        print("[green]✅ Excluded projects list cleared[/green]")
    except Exception as e:
        print(f"[red]❌ Error clearing excluded projects: {e}[/red]")


@app.command("set-daily-goal")
def set_daily_goal_cmd(hours: float):
    """Set daily time goal in hours"""
    try:
        if hours <= 0:
            print("[red]❌ Daily goal must be greater than 0[/red]")
            return

        set_daily_goal_hours(hours)
        print(f"[green]✅ Daily goal set to: {hours}h[/green]")
    except Exception as e:
        print(f"[red]❌ Error setting daily goal: {e}[/red]")


@app.command("set-weekly-goal")
def set_weekly_goal_cmd(hours: float):
    """Set weekly time goal in hours"""
    try:
        if hours <= 0:
            print("[red]❌ Weekly goal must be greater than 0[/red]")
            return

        set_weekly_goal_hours(hours)
        print(f"[green]✅ Weekly goal set to: {hours}h[/green]")
    except Exception as e:
        print(f"[red]❌ Error setting weekly goal: {e}[/red]")


def config_main():
    """Main config command (acts as group)"""
    app()


if __name__ == "__main__":
    app()
