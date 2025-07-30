# paTS - Python Timesheet System

A fast and intuitive command-line timesheet tracker built with Python.

## Features

- Start and stop time tracking sessions
- View timesheets by day, week, or month
- Project-based time tracking with descriptions
- Beautiful terminal output with colors and emojis

## Installation

This project uses [uv](https://docs.astral.sh/uv/) for fast Python package management.

### Development Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd paTS
```

2. Install dependencies and the project:
```bash
uv sync
```

### Global Installation

To use `paTS` from anywhere on your system (like `npm link`):

```bash
# Install globally as an editable tool
uv tool install --editable .
```

Now you can use `paTS` from any directory:
```bash
cd ~/anywhere
paTS start "My Project"
paTS info
```

### Uninstall

To remove the global installation:
```bash
uv tool uninstall pats
```

## Usage

### Available Commands

- `paTS start [project] --desc "description"` - Start tracking time for a project
- `paTS stop` - Stop the current time tracking session
- `paTS info` - Show current session information
- `paTS day [date]` - Show timesheet for a specific day
- `paTS week [date]` - Show timesheet for a specific week  
- `paTS month [date]` - Show timesheet for a specific month

### Examples

```bash
# Start tracking time for a project
paTS start "My Project" --desc "Working on feature X"

# Stop tracking
paTS stop

# View today's timesheet
paTS day

# View specific date  
paTS day 2024-01-15

# View current session info (great for tmux status bar)
paTS info

# View all entries
paTS display

# View this week's entries
paTS week

# View this month's entries
paTS month
```

**Note**: If not globally installed, prefix commands with `uv run` (e.g., `uv run paTS start`)

## Development

### Code Quality

This project uses [Ruff](https://docs.astral.sh/ruff/) for lightning-fast linting and formatting.

#### Format Code
```bash
# Format all Python files
uv run ruff format .

# Check what would be formatted (dry run)
uv run ruff format --diff .
```

#### Lint Code
```bash
# Check for linting issues
uv run ruff check .

# Auto-fix linting issues
uv run ruff check --fix .
```

#### Run All Quality Checks
```bash
# Run linting and formatting in one go
uv run ruff check --fix . && uv run ruff format .
```

### Configuration

- **Project config**: `pyproject.toml`
- **Ruff settings**: Configured in `pyproject.toml` under `[tool.ruff]`
- **Line length**: 88 characters (Black-compatible)
- **Python version**: 3.12+

## License

MIT License