"""Minecraft Launcher for Prism Launcher Client"""

import subprocess
import logging
import os
from pathlib import Path
from typing import Optional

from utils.config import Config
from utils.paths import get_instances_path

logger = logging.getLogger(__name__)


class MinecraftLauncher:
    """Launches Minecraft instances via Prism Launcher."""
    
    def __init__(self, config: Config):
        """Initialize Minecraft Launcher."""
        self.config = config
        self.instances_path = get_instances_path()
    
    def launch(self, instance_name: str) -> bool:
        """Launch a Minecraft instance."""
        try:
            instance_path = self.instances_path / instance_name
            
            if not instance_path.exists():
                raise FileNotFoundError(f"Instance not found: {instance_name}")
            
            # Get instance configuration
            config_path = instance_path / "instance.cfg"
            config = self._parse_config(config_path)
            
            # Prepare launch command
            java_path = config.get('JavaPath', '/usr/libexec/java_home')
            java_args = config.get('JavaArgs', '-Xmx2048m -Xms512m')
            
            # Build launch command
            cmd = [
                java_path,
                '-jar',
                str(instance_path / 'minecraft_server.jar'),
                'nogui'
            ]
            
            # Add Java arguments
            cmd = java_args.split() + cmd
            
            logger.info(f"Launching instance: {instance_name}")
            logger.info(f"Command: {' '.join(cmd)}")
            
            # Launch in background
            subprocess.Popen(
                cmd,
                cwd=str(instance_path),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            
            logger.info(f"Instance launched: {instance_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to launch instance: {e}")
            raise
    
    def _parse_config(self, config_path: Path) -> dict:
        """Parse instance configuration file."""
        config = {}
        
        try:
            if config_path.exists():
                with open(config_path, 'r') as f:
                    for line in f:
                        if '=' in line and not line.startswith('#'):
                            key, value = line.strip().split('=', 1)
                            config[key] = value
        except Exception as e:
            logger.error(f"Failed to parse config: {e}")
        
        return config
