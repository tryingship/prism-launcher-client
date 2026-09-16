#!/usr/bin/env python3
"""
Prism Launcher Client - Main Entry Point

A third-party launcher for Prism Launcher with custom UI for managing
and launching Minecraft instances on macOS.
"""

import sys
import os
import logging
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

from ui.main_window import MainWindow
from utils.logger import setup_logging
from utils.config import Config


def main():
    """Main entry point for the application."""
    # Setup logging
    debug = '--debug' in sys.argv
    setup_logging(debug=debug)
    logger = logging.getLogger(__name__)
    
    logger.info("Starting Prism Launcher Client")
    
    # Load or create configuration
    try:
        config = Config()
        config.load()
        logger.info(f"Configuration loaded from {config.config_path}")
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        config = Config()
    
    # Create and run the main window
    try:
        app = MainWindow(config)
        app.run()
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
