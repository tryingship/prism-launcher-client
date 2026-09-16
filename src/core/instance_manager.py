"""Instance Manager for Prism Launcher Client"""

import json
import logging
import shutil
from pathlib import Path
from typing import List, Dict, Optional

from utils.config import Config
from utils.paths import get_instances_path

logger = logging.getLogger(__name__)


class InstanceManager:
    """Manages Minecraft instances."""
    
    def __init__(self, config: Config):
        """Initialize Instance Manager."""
        self.config = config
        self.instances_path = get_instances_path()
    
    def get_instances(self) -> List[Dict]:
        """Get all available instances."""
        instances = []
        
        if not self.instances_path.exists():
            logger.warning(f"Instances path does not exist: {self.instances_path}")
            return instances
        
        try:
            for instance_dir in self.instances_path.iterdir():
                if instance_dir.is_dir():
                    instance_info = self._get_instance_info(instance_dir)
                    if instance_info:
                        instances.append(instance_info)
            
            logger.info(f"Found {len(instances)} instances")
            return sorted(instances, key=lambda x: x['name'])
        except Exception as e:
            logger.error(f"Failed to get instances: {e}")
            return instances
    
    def _get_instance_info(self, instance_dir: Path) -> Optional[Dict]:
        """Get information about an instance."""
        try:
            config_path = instance_dir / "instance.cfg"
            
            # Parse instance config
            config = {}
            if config_path.exists():
                with open(config_path, 'r') as f:
                    for line in f:
                        if '=' in line and not line.startswith('#'):
                            key, value = line.strip().split('=', 1)
                            config[key] = value
            
            return {
                'name': instance_dir.name,
                'path': str(instance_dir),
                'config': config,
            }
        except Exception as e:
            logger.error(f"Failed to get instance info for {instance_dir.name}: {e}")
            return None
    
    def create_instance(self, instance_data: Dict) -> bool:
        """Create a new instance."""
        try:
            name = instance_data.get('name')
            version = instance_data.get('version')
            min_mem = instance_data.get('min_memory', '512')
            max_mem = instance_data.get('max_memory', '2048')
            java_path = instance_data.get('java_path', '/usr/libexec/java_home')
            
            instance_path = self.instances_path / name
            instance_path.mkdir(parents=True, exist_ok=True)
            
            # Create instance.cfg
            config_path = instance_path / "instance.cfg"
            config_content = f"""# Prism Launcher Instance Configuration
name={name}
GameType=release
GameVersion={version}
JavaPath={java_path}
JavaArgs=-Xmx{max_mem}m -Xms{min_mem}m
PreLaunchCommand=
PostExitCommand=
RenderDistance=16"""
            
            with open(config_path, 'w') as f:
                f.write(config_content)
            
            logger.info(f"Created instance: {name}")
            return True
        except Exception as e:
            logger.error(f"Failed to create instance: {e}")
            raise
    
    def delete_instance(self, instance_name: str) -> bool:
        """Delete an instance."""
        try:
            instance_path = self.instances_path / instance_name
            if instance_path.exists():
                shutil.rmtree(instance_path)
                logger.info(f"Deleted instance: {instance_name}")
                return True
            else:
                logger.warning(f"Instance not found: {instance_name}")
                return False
        except Exception as e:
            logger.error(f"Failed to delete instance: {e}")
            raise
    
    def update_instance(self, instance_name: str, data: Dict) -> bool:
        """Update instance configuration."""
        try:
            instance_path = self.instances_path / instance_name
            config_path = instance_path / "instance.cfg"
            
            if not config_path.exists():
                logger.error(f"Instance config not found: {config_path}")
                return False
            
            # Read current config
            config = {}
            with open(config_path, 'r') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        config[key] = value
            
            # Update with new data
            config.update(data)
            
            # Write updated config
            with open(config_path, 'w') as f:
                for key, value in config.items():
                    f.write(f"{key}={value}\n")
            
            logger.info(f"Updated instance: {instance_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to update instance: {e}")
            raise
