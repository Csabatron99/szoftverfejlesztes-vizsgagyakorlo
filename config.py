import os
import sys


def _resource_dir() -> str:
    """Read-only bundled files (questions.json).
    When frozen: sys._MEIPASS (temp extraction dir for --onefile, app dir for --onedir).
    When normal: the directory of this file."""
    if getattr(sys, "frozen", False):
        return sys._MEIPASS  # type: ignore[attr-defined]
    return os.path.dirname(os.path.abspath(__file__))


def _user_data_dir() -> str:
    """Writable user data (stats.json).
    Always sits next to the running executable so stats persist across runs."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

# --- App ---
APP_TITLE = "Szoftverfejlesztés Vizsgagyakorló"
APP_WIDTH = 1150
APP_HEIGHT = 800

# --- customtkinter ---
APPEARANCE_MODE = "dark"
COLOR_THEME = "blue"

# --- Colors ---
PRIMARY_COLOR   = "#1f538d"
SECONDARY_COLOR = "#2d6da3"
SUCCESS_COLOR   = "#2d8a4e"
ERROR_COLOR     = "#c0392b"
WARNING_COLOR   = "#d68910"
TEXT_SECONDARY  = "#a0a0b0"

# --- Fonts ---
FONT_TITLE    = ("Segoe UI", 32, "bold")
FONT_SUBTITLE = ("Segoe UI", 19)
FONT_BODY     = ("Segoe UI", 15)
FONT_SMALL    = ("Segoe UI", 13)
FONT_BUTTON   = ("Segoe UI", 15, "bold")
FONT_CODE     = ("Consolas", 13)

# --- Quiz modes ---
QUIZ_MODES = {
    "quick":    {"name": "Gyors teszt",            "count": 10,   "time_limit": None},
    "normal":   {"name": "Normál teszt",            "count": 25,   "time_limit": None},
    "full":     {"name": "Teljes ZH szimuláció",   "count": 50,   "time_limit": 90},
    "category": {"name": "Kategória teszt",         "count": None, "time_limit": None},
    "mistakes": {"name": "Hibás kérdések",          "count": None, "time_limit": None},
}

# --- Data paths ---
DATA_DIR       = os.path.join(_resource_dir(), "data")
QUESTIONS_FILE = os.path.join(_resource_dir(), "data", "questions.json")
STATS_FILE     = os.path.join(_user_data_dir(), "data", "stats.json")
