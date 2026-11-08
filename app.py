import json
import os
import sys
import threading
import time
import customtkinter as ctk
from pynput import keyboard
import pystray
from PIL import Image, ImageDraw

# Configuration du thème global
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

if getattr(sys, "frozen", False):
    APP_DIR = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "FortniteChestTracker")
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(APP_DIR, exist_ok=True)
SETTINGS_FILE = os.path.join(APP_DIR, "settings.json")

def get_icon_path():
    if getattr(sys, "frozen", False):
        base = getattr(sys, "_MEIPASS", APP_DIR)
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "icon.ico")

TRANSLATIONS = {
    "en": {
        "open_chests": "Chests opened",
        "key_label": "Bound key :",
        "settings_title": "Settings",
        "first_launch_title": "First Launch - Calibration",
        "key_prompt": "Open key (e.g.: e) :",
        "count_prompt": "Current number of chests :",
        "language_prompt": "Language :",
        "save": "Save",
        "tray_open": "Ouvrir",
        "tray_quit": "Quitter",
    },
    "fr": {
        "open_chests": "Coffres ouverts",
        "key_label": "Touche attribuée :",
        "settings_title": "Paramètres",
        "first_launch_title": "Premier Lancement - Calibration",
        "key_prompt": "Touche d'ouverture (ex: e) :",
        "count_prompt": "Nombre actuel de coffres :",
        "language_prompt": "Langue :",
        "save": "Valider",
        "tray_open": "Ouvrir",
        "tray_quit": "Quitter",
    },
}

class ChestTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Fortnite Chest Tracker")
        icon_path = get_icon_path()
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)
        self.geometry("340x440")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.configure(fg_color="#140001")

        self.settings = self.load_settings()
        self.press_time = None
        self.is_held_counted = False
        self.stop_timer = False
        self.quit_requested = False
        self.tray_icon = None

        self.create_widgets()
        self.start_keyboard_listener()
        self.start_tray_icon()

        # Fermer la fenêtre = masquer dans la zone de notification
        self.protocol("WM_DELETE_WINDOW", self.hide_to_tray)

        if self.settings.get("first_launch", True):
            self.open_settings(is_first=True)

    def t(self, key):
        lang = self.settings.get("language", "en")
        return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)

    def _create_tray_image(self):
        img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle([4, 4, 60, 60], radius=14, fill="#1E0004", outline="#FFC92C", width=3)
        draw.text((32, 32), "F", fill="#FFC92C", anchor="mm")
        return img

    def start_tray_icon(self):
        def show_window():
            self.after(0, self.show_window)

        def quit_app():
            self.after(0, self.quit_app)

        menu = pystray.Menu(
            pystray.MenuItem(lambda item: self.t("tray_open"), show_window, default=True),
            pystray.MenuItem(lambda item: self.t("tray_quit"), quit_app),
        )
        icon_path = get_icon_path()
        if os.path.exists(icon_path):
            icon_image = Image.open(icon_path)
        else:
            icon_image = self._create_tray_image()
        self.tray_icon = pystray.Icon("FortniteChestTracker", icon_image, "Fortnite Chest Tracker", menu)
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def hide_to_tray(self):
        self.withdraw()

    def show_window(self):
        self.deiconify()
        self.lift()
        self.focus_force()

    def quit_app(self):
        self.quit_requested = True
        if self.tray_icon is not None:
            try:
                self.tray_icon.stop()
            except Exception:
                pass
        self.destroy()

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"key": "e", "chests_opened": 0, "first_launch": True, "language": "en"}

    def save_settings_to_disk(self):
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=4)

    def create_widgets(self):
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=15)

        title_lbl = ctk.CTkLabel(header_frame, text="FORTNITE TRACKER", text_color="#7A6E70", font=("Segoe UI", 11, "bold"))
        title_lbl.pack(side="left")

        btn_gear = ctk.CTkButton(header_frame, text="⚙", width=35, height=35, fg_color="#1E0004", hover_color="#2D0008", text_color="#7A6E70", font=("Segoe UI", 14), command=self.open_settings)
        btn_gear.pack(side="right")

        # Compteur Central
        center_frame = ctk.CTkFrame(self, fg_color="transparent")
        center_frame.pack(expand=True)

        self.count_lbl = ctk.CTkLabel(center_frame, text=str(self.settings["chests_opened"]), text_color="#FFC92C", font=("Segoe UI", 65, "bold"))
        self.count_lbl.pack()

        self.sub_lbl = ctk.CTkLabel(center_frame, text=self.t("open_chests"), text_color="#B0A4A6", font=("Segoe UI", 12))
        self.sub_lbl.pack(pady=(0, 10))

        # Footer Touche
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.pack(fill="x", padx=20, pady=20)

        self.key_label = ctk.CTkLabel(footer_frame, text=self.t("key_label"), text_color="#B0A4A6", font=("Segoe UI", 11))
        self.key_label.pack(anchor="w")
        
        self.key_badge = ctk.CTkLabel(footer_frame, text=self.settings["key"].upper(), fg_color="#1E0004", text_color="#FFC92C", font=("Segoe UI", 13, "bold"), corner_radius=6, width=50, height=30)
        self.key_badge.pack(anchor="w", pady=5)

    def open_settings(self, is_first=False):
        win = ctk.CTkToplevel(self)
        win.title(self.t("settings_title"))
        win.geometry("300x360")
        win.resizable(False, False)
        win.attributes("-topmost", True)
        win.grab_set()
        win.configure(fg_color="#140001")

        ctk.CTkLabel(win, text=self.t("first_launch_title") if is_first else self.t("settings_title"), text_color="#FFC92C", font=("Segoe UI", 12, "bold")).pack(pady=20)

        ctk.CTkLabel(win, text=self.t("key_prompt"), text_color="#B0A4A6", font=("Segoe UI", 11)).pack(anchor="w", padx=25)
        key_entry = ctk.CTkEntry(win, fg_color="#1E0004", border_color="#2D0008", text_color="#FFF", font=("Segoe UI", 12))
        key_entry.insert(0, self.settings["key"])
        key_entry.pack(fill="x", padx=25, pady=5)

        ctk.CTkLabel(win, text=self.t("count_prompt"), text_color="#B0A4A6", font=("Segoe UI", 11)).pack(anchor="w", padx=25)
        count_entry = ctk.CTkEntry(win, fg_color="#1E0004", border_color="#2D0008", text_color="#FFF", font=("Segoe UI", 12))
        count_entry.insert(0, str(self.settings["chests_opened"]))
        count_entry.pack(fill="x", padx=25, pady=5)

        ctk.CTkLabel(win, text=self.t("language_prompt"), text_color="#B0A4A6", font=("Segoe UI", 11)).pack(anchor="w", padx=25)
        language_names = {"en": "English", "fr": "Français"}
        lang_menu = ctk.CTkOptionMenu(
            win,
            values=["English", "Français"],
            fg_color="#1E0004",
            button_color="#2D0008",
            button_hover_color="#3A0010",
            text_color="#FFF",
            font=("Segoe UI", 12),
            command=lambda v: None,
        )
        lang_menu.set(language_names.get(self.settings.get("language", "en"), "English"))
        lang_menu.pack(fill="x", padx=25, pady=5)

        def save():
            new_key = key_entry.get().strip().lower()
            try:
                new_count = int(count_entry.get().strip())
            except ValueError:
                new_count = self.settings["chests_opened"]

            if new_key:
                self.settings["key"] = new_key
            self.settings["chests_opened"] = new_count
            self.settings["language"] = "fr" if lang_menu.get() == "Français" else "en"
            self.settings["first_launch"] = False

            self.save_settings_to_disk()
            self.count_lbl.configure(text=str(self.settings["chests_opened"]))
            self.key_badge.configure(text=self.settings["key"].upper())
            self.sub_lbl.configure(text=self.t("open_chests"))
            self.key_label.configure(text=self.t("key_label"))
            win.destroy()

        btn_save = ctk.CTkButton(win, text=self.t("save"), fg_color="#FFC92C", hover_color="#E0B327", text_color="#140001", font=("Segoe UI", 12, "bold"), command=save)
        btn_save.pack(fill="x", padx=25, pady=20)

    def increment_chest(self):
        self.settings["chests_opened"] += 1
        self.save_settings_to_disk()
        # Sécurité thread-principal pour l'UI
        self.after(0, lambda: self.count_lbl.configure(text=str(self.settings["chests_opened"])))

    def start_keyboard_listener(self):
        def get_char(key):
            try:
                if hasattr(key, 'char') and key.char:
                    return key.char.lower()
                if hasattr(key, 'name'):
                    return key.name.lower()
            except Exception:
                pass
            return str(key).lower().replace("key.", "")

        def on_press(key):
            target_key = self.settings.get("key", "e").lower()
            if get_char(key) == target_key:
                if self.press_time is None:
                    self.press_time = time.time()
                    self.is_held_counted = False
                    self.stop_timer = False
                    threading.Thread(target=self._check_hold, daemon=True).start()

        def on_release(key):
            target_key = self.settings.get("key", "e").lower()
            if get_char(key) == target_key:
                self.press_time = None
                self.stop_timer = True
                self.is_held_counted = False

        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.daemon = True
        listener.start()

    def _check_hold(self):
        hold_duration = 0.6
        while not self.stop_timer and self.press_time is not None:
            if time.time() - self.press_time >= hold_duration:
                if not self.is_held_counted:
                    self.increment_chest()
                    self.is_held_counted = True
                break
            time.sleep(0.02)

if __name__ == "__main__":
    app = ChestTrackerApp()
    app.mainloop()