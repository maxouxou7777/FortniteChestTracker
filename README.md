# Fortnite Chest Tracker

A simple and lightweight chest counter for Fortnite. Track your chest openings with a customizable hotkey.

## Features

- **Custom Hotkey** - Bind any key to increment the counter
- **System Tray** - Minimize to tray with quick access menu
- **Persistent Settings** - Your count and preferences are saved automatically
- **Multi-language** - English and French support
- **Dark Theme** - Fortnite-inspired UI with gold accents

## Download

Get the latest release (Windows executable) from the [Releases](https://github.com/maxouxou7777/FortniteChestTracker/releases) page.

## Usage

1. Run `app.exe`
2. On first launch, configure your hotkey (default: `F`)
3. Press your bound key in-game to increment the counter
4. Click the gear icon ⚙ to change settings anytime

## Building from Source

```bash
pip install -r requirements.txt
python app.py
```

Or build the executable:

```bash
pip install pyinstaller
python -m PyInstaller --noconfirm --onefile --windowed --uac-admin --icon icon.ico --add-data "icon.ico;." --hidden-import pystray._win32 app.py
```

## Requirements

- Python 3.12+
- Windows 10/11
- customtkinter
- pynput
- pystray
- pillow

## License

MIT
