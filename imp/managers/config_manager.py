from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parents[1]

CONFIG_FILES = {
    "personality": BASE_DIR / "config" / "imp-personality.json",
    "permissions": BASE_DIR / "config" / "imp-user-permissions.json",
    "system": BASE_DIR / "config" / "imp-system-settings.json",
    "environment": BASE_DIR / "config" / "imp-environment.json",
}


def load_config(name):
    path = CONFIG_FILES.get(name)
    if not path:
        raise ValueError("Invalid configuration name")
    with open(path, "r") as f:
        return json.load(f)


def save_config(name, data):
    path = CONFIG_FILES.get(name)
    if not path:
        raise ValueError("Invalid configuration name")
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def modify_config(name, key, value):
    config = load_config(name)
    keys = key.split(".")
    target = config
    for k in keys[:-1]:
        target = target.setdefault(k, {})
    target[keys[-1]] = value
    save_config(name, config)
