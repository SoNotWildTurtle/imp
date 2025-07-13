from pathlib import Path
import json
import time

BASE_DIR = Path(__file__).resolve().parents[1]
PROFILE_FILE = BASE_DIR / "config" / "imp-general-intelligences.json"
CONFIG_DIR = BASE_DIR / "config" / "gi"
BUILD_LOG = BASE_DIR / "logs" / "imp-gi-build-log.json"


def load_profiles():
    if PROFILE_FILE.exists():
        with open(PROFILE_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def save_log(entry):
    logs = []
    if BUILD_LOG.exists():
        with open(BUILD_LOG, "r") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
    logs.append(entry)
    with open(BUILD_LOG, "w") as f:
        json.dump(logs, f, indent=4)


def build_intelligence():
    profiles = load_profiles()
    if not profiles:
        print("No profiles available. Run the GI builder first.")
        return
    for i, p in enumerate(profiles, 1):
        print(f"{i}. {p['name']}: {p.get('description','')}")
    choice = input("Select profile number: ").strip()
    try:
        idx = int(choice) - 1
        profile = profiles[idx]
    except Exception:
        print("Invalid selection")
        return

    CONFIG_DIR.mkdir(exist_ok=True)
    config_path = CONFIG_DIR / f"{profile['name']}.json"
    config = {
        "name": profile["name"],
        "description": profile.get("description", ""),
        "skills": profile.get("skills", []),
        "personality": profile.get("personality", []),
        "conversation_style": profile.get("conversation_style", ""),
        "focus_area": profile.get("focus_area", ""),
        "autonomy": profile.get("autonomy", ""),
        "learning_style": profile.get("learning_style", ""),
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    with open(config_path, "w") as f:
        json.dump(config, f, indent=4)
    save_log({"timestamp": config["created"], "profile": profile["name"]})
    print(f"[+] Built intelligence config at {config_path}")


if __name__ == "__main__":
    build_intelligence()
