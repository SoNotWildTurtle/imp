import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_FILES = {
    "personality": ROOT / "config" / "imp-personality.json",
    "permissions": ROOT / "config" / "imp-user-permissions.json",
    "system": ROOT / "config" / "imp-system-settings.json",
    "environment": ROOT / "config" / "imp-environment.json"
}

def load_config(config_name):
    if config_name not in CONFIG_FILES:
        print("⚠️ Invalid configuration name.")
        return None

    with open(CONFIG_FILES[config_name], "r") as f:
        return json.load(f)

def modify_config(config_name, key, value):
    config = load_config(config_name)
    if config is None:
        return

    keys = key.split(".")
    target = config

    for k in keys[:-1]:
        target = target.setdefault(k, {})

    target[keys[-1]] = value

    with open(CONFIG_FILES[config_name], "w") as f:
        json.dump(config, f, indent=4)

    print(f"✅ Updated {config_name} -> {key}: {value}")

action = input(
    "Modify config (format: category key value) or press Enter to skip: "
)
if action:
    parts = action.split(" ", 2)
    if len(parts) == 3:
        modify_config(parts[0], parts[1], parts[2])
