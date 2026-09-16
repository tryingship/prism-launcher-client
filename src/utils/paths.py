"""Path Utilities for Prism Launcher Client"""

from pathlib import Path
from typing import Optional


def get_prism_path() -> Path:
    """Get Prism Launcher installation path."""
    # Default macOS path
    default_path = Path("/Applications/Prism Launcher.app")
    if default_path.exists():
        return default_path
    
    # Try alternative location
    alt_path = Path.home() / "Applications" / "Prism Launcher.app"
    if alt_path.exists():
        return alt_path
    
    return default_path


def get_instances_path() -> Path:
    """Get Prism Launcher instances directory path."""
    # Standard Prism Launcher instances location
    prism_data_path = Path.home() / "Library" / "Application Support" / "PrismLauncher" / "instances"
    return prism_data_path


def get_config_dir() -> Path:
    """Get application configuration directory."""
    config_dir = Path.home() / ".prism-launcher-client"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir
