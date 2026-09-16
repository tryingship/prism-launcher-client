"""Configuration Management for Prism Launcher Client"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class Config:
    """Manages application configuration."""
    
    DEFAULT_CONFIG = {
        'prism_launcher_path': '/Applications/Prism Launcher.app',
        'java_path': '/usr/libexec/java_home',
        'memory_min': '512M',
        'memory_max': '2048M',
        'theme': 'light',
    }
    
    def __init__(self, config_dir: Optional[Path] = None):
        """Initialize configuration."""
        if config_dir is None:
            config_dir = Path.home() / ".prism-launcher-client"
        
        self.config_dir = Path(config_dir)
        self.config_path = self.config_dir / "settings.json"
        self.data = self.DEFAULT_CONFIG.copy()
    
    def load(self) -> None:
        """Load configuration from file."""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    loaded = json.load(f)
                    self.data.update(loaded)
                logger.info(f"Configuration loaded from {self.config_path}")
            else:
                self.save()
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
    
    def save(self) -> None:
        """Save configuration to file."""
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(self.data, f, indent=2)
            logger.info(f"Configuration saved to {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.data.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        self.data[key] = value
        self.save()
    
    def __getitem__(self, key: str) -> Any:
        """Get configuration value using bracket notation."""
        return self.data[key]
    
    def __setitem__(self, key: str, value: Any) -> None:
        """Set configuration value using bracket notation."""
        self.set(key, value)
