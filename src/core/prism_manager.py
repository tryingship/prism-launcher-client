"""Prism Launcher Manager"""

import json
import logging
from pathlib import Path
from typing import Optional, List, Dict

from utils.config import Config
from utils.paths import get_prism_path, get_instances_path

logger = logging.getLogger(__name__)


class PrismManager:
    """Manages interaction with Prism Launcher."""
    
    def __init__(self, config: Config):
        """Initialize Prism Manager."""
        self.config = config
        self.prism_path = self._detect_prism_path()
        logger.info(f"Prism Launcher path: {self.prism_path}")
    
    def _detect_prism_path(self) -> Path:
        """Detect Prism Launcher installation path."""
        # Check config first
        if self.config.get('prism_launcher_path'):
            path = Path(self.config.get('prism_launcher_path'))
            if path.exists():
                return path
        
        # Default macOS path
        default_path = Path("/Applications/Prism Launcher.app")
        if default_path.exists():
            return default_path
        
        # Try alternative location
        alt_path = Path.home() / "Applications" / "Prism Launcher.app"
        if alt_path.exists():
            return alt_path
        
        logger.warning("Prism Launcher not found in default locations")
        return default_path
    
    def is_installed(self) -> bool:
        """Check if Prism Launcher is installed."""
        return self.prism_path.exists()
    
    def get_instances_path(self) -> Path:
        """Get path to Prism Launcher instances directory."""
        return get_instances_path()
    
    def get_instance_config(self, instance_name: str) -> Optional[Dict]:
        """Get instance configuration."""
        instances_path = self.get_instances_path()
        instance_path = instances_path / instance_name / "instance.cfg"
        
        if not instance_path.exists():
            logger.warning(f"Instance config not found: {instance_path}")
            return None
        
        try:
            config = {}
            with open(instance_path, 'r') as f:
                for line in f:
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        config[key] = value
            return config
        except Exception as e:
            logger.error(f"Failed to read instance config: {e}")
            return None
