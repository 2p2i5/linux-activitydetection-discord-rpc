"""profiles.py
Loads/saves Rich Presence profiles from
~/.config/discord-rpc-linux/profiles.json"""

import json
import os
from typing import Dict, Any

CONFIG_DIR = os.path.expanduser("~/.config/discord-rpc-linux")
PROFILES_FILE = os.path.join(CONFIG_DIR, "profiles.json")

DEFAULT_PROFILE: Dict[str, Any] = {
    "client_id": "",
    "details": "",
    "state": "",
    "large_image": "",
    "large_text": "",
    "small_image": "",
    "small_text": "",
    "show_timestamp": False,
    "button1_label": "",
    "button1_url": "",
    "button2_label": "",
    "button2_url": "",
}


def _ensure_config_dir():
    os.makedirs(CONFIG_DIR, exist_ok=True)


def load_all() -> Dict[str, Dict[str, Any]]:
    _ensure_config_dir()
    if not os.path.exists(PROFILES_FILE):
        return {}
    try:
        with open(PROFILES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_all(profiles: Dict[str, Dict[str, Any]]):
    _ensure_config_dir()
    with open(PROFILES_FILE, "w", encoding="utf-8") as f:
        json.dump(profiles, f, indent=2, ensure_ascii=False)
# mkv mkv mkv mkv

def save_profile(name: str, data: Dict[str, Any]):
    profiles = load_all()
    profiles[name] = data
    save_all(profiles)


def delete_profile(name: str):
    profiles = load_all()
    if name in profiles:
        del profiles[name]
        save_all(profiles)


def new_profile() -> Dict[str, Any]:
    return dict(DEFAULT_PROFILE)
