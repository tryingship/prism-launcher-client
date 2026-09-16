"""Logging Setup for Prism Launcher Client"""

import logging
import sys
from pathlib import Path


def setup_logging(debug: bool = False) -> None:
    """Setup application logging."""
    log_level = logging.DEBUG if debug else logging.INFO
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Create logs directory
    log_dir = Path.home() / ".prism-launcher-client" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "app.log"
    
    # Configure logging
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger()
    logger.info(f"Logging initialized (level: {logging.getLevelName(log_level)})")
