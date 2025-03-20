import os
import json
import time

CONFIG_FILES = {
    "personality": "/root/imp/config/imp-personality.json",
    "permissions": "/root/imp/config/imp-user-permissions.json",
    "system": "/root/imp/config/imp-system-settings.json",
    "environment": "/root/imp/config/imp-environment.json"
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

while True:
    action = input("Modify config (format: category key value) or press Enter to skip: ")
    if action:
        parts = action.split(" ", 2)
        if len(parts) == 3:
            modify_config(parts[0], parts[1], parts[2])
    time.sleep(5)
