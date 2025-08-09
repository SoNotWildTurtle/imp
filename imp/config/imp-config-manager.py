"""Interactive wrapper for configuration management."""

from imp.managers import config_manager


def load_config(name):
    return config_manager.load_config(name)


def modify_config(name, key, value):
    config_manager.modify_config(name, key, value)
    print(f"✅ Updated {name} -> {key}: {value}")


if __name__ == "__main__":
    action = input(
        "Modify config (format: category key value) or press Enter to skip: "
    )
    if action:
        parts = action.split(" ", 2)
        if len(parts) == 3:
            modify_config(parts[0], parts[1], parts[2])
