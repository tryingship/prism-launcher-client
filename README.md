# Prism Launcher Client

A third-party launcher for Prism Launcher with a custom UI for managing and launching Minecraft instances on macOS.

## Features

- 🎮 Download and manage Minecraft game instances
- 🚀 Launch Minecraft with Prism Launcher integration
- ⚙️ Create new game instances
- 🎨 Modern custom UI
- 📦 Instance management and configuration
- 🔄 Auto-detection of Prism Launcher installations

## Requirements

- macOS 10.12 or later
- Python 3.8 or higher
- Prism Launcher installed on your system

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/tryingship/prism-launcher-client.git
cd prism-launcher-client
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python main.py
```

## Usage

### Starting the Launcher

1. Run `python main.py` from the project directory
2. The launcher will automatically detect your Prism Launcher installation

### Managing Instances

**View Instances:**
- The main window displays all your existing Prism Launcher instances
- Click on any instance to view its details

**Create a New Instance:**
1. Click the "New Instance" button
2. Enter instance name and select game version
3. Configure Java settings and memory allocation
4. Click "Create"

**Launch Minecraft:**
1. Select an instance from the list
2. Click "Launch" button
3. Minecraft will start with the selected instance

**Delete Instance:**
1. Right-click on an instance
2. Select "Delete" to remove it

## Project Structure

```
prism-launcher-client/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── src/
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── main_window.py  # Main UI window
│   │   ├── create_instance.py  # Instance creation dialog
│   │   └── styles.py       # UI styling
│   ├── core/
│   │   ├── __init__.py
│   │   ├── prism_manager.py    # Prism Launcher integration
│   │   ├── instance_manager.py # Instance management
│   │   └── launcher.py     # Minecraft launcher
│   └── utils/
│       ├── __init__.py
│       ├── config.py       # Configuration management
│       ├── logger.py       # Logging utility
│       └── paths.py        # Path utilities
└── config/
    └── settings.json       # User settings
```

## Configuration

Configuration is stored in `config/settings.json`. You can manually edit this file or use the launcher's settings dialog.

### Example Configuration

```json
{
  "prism_launcher_path": "/Applications/Prism Launcher.app",
  "java_path": "/usr/libexec/java_home",
  "memory_min": "512M",
  "memory_max": "2048M",
  "theme": "light"
}
```

## Troubleshooting

### Prism Launcher Not Detected
- Ensure Prism Launcher is installed in the Applications folder
- Check the settings dialog and manually set the Prism Launcher path

### Minecraft Won't Launch
- Verify Java is installed: `java -version`
- Check memory allocation settings (ensure max > min)
- Review logs in the Help menu

### Permission Denied Errors
- On macOS, you may need to grant the app permissions:
  ```bash
  chmod +x main.py
  ```

## Development

### Running in Development Mode

```bash
python -m src.main --debug
```

### Running Tests

```bash
python -m pytest tests/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This is a third-party launcher not affiliated with Prism Launcher or Minecraft. Use at your own risk.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.
