# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

paTS (Python Timesheet System) is a command-line timesheet tracker built with Python 3.12+, using uv for package management, Typer for CLI framework, and Rich for terminal output.

## Development Commands

### Environment Setup
```bash
# Install dependencies and sync project
uv sync
```

### Running the Application
```bash
# Run CLI commands
uv run paTS --help
uv run paTS start "Project Name" description text here
uv run paTS stop
uv run paTS info
uv run paTS day [date]
uv run paTS week [date]  
uv run paTS month [date]
uv run paTS backup [path]
uv run paTS restore [path] [--force]

# Alternative entry point (both work)
uv run pats --help
```

### Code Quality
```bash
# Format code
uv run ruff format .

# Check formatting (dry run)
uv run ruff format --diff .

# Lint code
uv run ruff check .

# Auto-fix linting issues
uv run ruff check --fix .

# Run all quality checks
uv run ruff check --fix . && uv run ruff format .
```

### Testing Protocol

**CRITICAL: Before ANY testing or experimentation with the application, you MUST follow this protocol:**

1. **ALWAYS backup first**: `uv run paTS backup`
2. **Perform your testing/changes**
3. **ALWAYS restore after**: `uv run paTS restore --force`

This ensures that user data is preserved and testing doesn't corrupt the actual timesheet database. The backup/restore cycle is mandatory for any operations that might modify the CSV database.

```bash
# Required testing workflow
uv run paTS backup                    # MANDATORY before testing
# ... perform your tests here ...
uv run paTS restore --force           # MANDATORY after testing
```

## Architecture

### CLI Structure
The CLI uses a modular command architecture:

- **`pats/cli.py`** - Main CLI entry point that imports and registers all commands
- **`pats/cmd/`** - Individual command modules, each containing a single command function
- **Command Registration** - Commands are registered via `app.command()(function_name)` pattern

### Adding New Commands
1. Create new file in `pats/cmd/` (e.g., `new_command.py`)
2. Define function with Typer decorators for arguments/options
3. Import function in `pats/cli.py`
4. Register with `app.command()(new_command)`

### Key Dependencies
- **Typer** - CLI framework with automatic help generation
- **Rich** - Terminal styling and colors (used via `from rich import print`)
- **Python 3.12+** - Uses modern type hints (`str | None` instead of `Optional[str]`)

### Configuration
- **Package Management**: uv (configured in `pyproject.toml`)
- **Code Quality**: Ruff linting and formatting (88 char line length, Black-compatible)
- **Build System**: Hatchling
- **Entry Points**: Both `paTS` and `pats` commands available

### Current Implementation Status
All commands are fully implemented and functional:
- **start** - Start time tracking with project and description support
- **stop** - Stop active time tracking sessions  
- **info** - Show current session info (optimized for tmux status bar)
- **day/week/month** - Display filtered timesheet entries with date ranges
- **display** - Show all timesheet entries
- **backup/restore** - Data backup and restoration functionality

The CLI framework uses a modular command architecture with proper error handling and rich terminal output.