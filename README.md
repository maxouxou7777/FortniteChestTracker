<div align="center">

# Fortnite Chest Tracker

<img src="icon.ico" alt="Chest Tracker Icon" width="128">

A simple and lightweight chest counter for Fortnite. Track your chest openings with a customizable hotkey.

</div>

---

## Security Notice

**⚠️ Antivirus Warning**

Some antivirus software may flag this executable as a threat. This is a **false positive** because:

- The code is **100% open source** - you can review every line
- The executable is built automatically by **GitHub Actions** on their servers
- No third-party binaries or obfuscated code are included
- You can build it yourself from source (see Building section below)

If you're concerned, always verify the source code and build it yourself.

---

## Features

- **Custom Hotkey** - Bind any key to increment the counter
- **System Tray** - Minimize to tray with quick access menu
- **Persistent Settings** - Your count and preferences are saved automatically
- **Multi-language** - English and French support
- **Dark Theme** - Fortnite-inspired UI with gold accents

## Download

<div align="center">

Get the latest release (Windows executable) from the [Releases](https://github.com/maxouxou7777/FortniteChestTracker/releases) page.

[![Download Latest](https://img.shields.io/badge/Download-v1.0.0-blue?style=for-the-badge&logo=github)](https://github.com/maxouxou7777/FortniteChestTracker/releases/latest)

</div>

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

MIT License - feel free to use, modify, and distribute.

---

<div align="center">

Made with AI for the Fortnite community

[GitHub](https://github.com/maxouxou7777/FortniteChestTracker) • [Releases](https://github.com/maxouxou7777/FortniteChestTracker/releases) • [Issues](https://github.com/maxouxou7777/FortniteChestTracker/issues)

</div>
