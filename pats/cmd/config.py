"""Config command for paTS"""

import typer
from rich import print

from pats.config import load_config, set_excluded_projects

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

        print("[bold]📋 Current Configuration:[/bold]")
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


def config_main():
    """Main config command (acts as group)"""
    app()


if __name__ == "__main__":
    app()
