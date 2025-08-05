"""Configuration management for paTS"""

import json
from pathlib import Path
from typing import Any


def get_config_path() -> Path:
    """Get the path to the configuration file"""
    return Path.home() / ".pats" / "config.json"


def load_config() -> dict[str, Any]:
    """Load configuration from file, return default if file doesn't exist"""
    config_path = get_config_path()

    if not config_path.exists():
        return get_default_config()

    try:
        with open(config_path, encoding="utf-8") as f:
            config = json.load(f)
            # Merge with defaults to ensure all keys exist
            default_config = get_default_config()
            default_config.update(config)
            return default_config
    except (OSError, json.JSONDecodeError):
        return get_default_config()


def save_config(config: dict[str, Any]) -> None:
    """Save configuration to file"""
    config_path = get_config_path()

    # Ensure the directory exists
    config_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, sort_keys=True)
    except OSError as e:
        raise OSError(f"Failed to save configuration: {e}") from e


def get_default_config() -> dict[str, Any]:
    """Get default configuration"""
    return {"excluded_projects": []}


def get_excluded_projects() -> list[str]:
    """Get list of projects to exclude from totals"""
    config = load_config()
    return config.get("excluded_projects", [])


def set_excluded_projects(projects: list[str]) -> None:
    """Set list of projects to exclude from totals"""
    config = load_config()
    config["excluded_projects"] = projects
    save_config(config)
