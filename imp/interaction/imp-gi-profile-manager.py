from pathlib import Path
import json
import sys
import importlib.util

BASE_DIR = Path(__file__).resolve().parents[1]
HEAVY_VERIFIER = BASE_DIR / "security" / "imp-heavy-identity-verifier.py"
spec = importlib.util.spec_from_file_location("heavy", HEAVY_VERIFIER)
heavy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(heavy)
verify_user = heavy.verify_user

PROFILE_FILE = BASE_DIR / "config" / "imp-general-intelligences.json"

def load_profiles():
    if PROFILE_FILE.exists():
        with open(PROFILE_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_profiles(data):
    with open(PROFILE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def list_profiles():
    profiles = load_profiles()
    if not profiles:
        print("No profiles defined.")
        return
    for p in profiles:
        print(f"- {p.get('name')}: {p.get('description','')}")

def remove_profile(name: str):
    profiles = load_profiles()
    remaining = [p for p in profiles if p.get('name') != name]
    if len(remaining) == len(profiles):
        print("Profile not found.")
        return
    save_profiles(remaining)
    print(f"[+] Removed profile {name}")


def update_profile(name: str, field: str, value: str):
    profiles = load_profiles()
    for p in profiles:
        if p.get("name") == name:
            if field in {"skills", "personality"}:
                p[field] = [v.strip() for v in value.split(',') if v.strip()]
            else:
                p[field] = value
            save_profiles(profiles)
            print(f"[+] Updated {field} for {name}")
            return
    print("Profile not found.")


def main():
    if len(sys.argv) < 2:
        print("Usage: gi-profile-manager.py [list|remove <name>|update <name> <field> <value>]")
        return
    if not verify_user():
        return
    cmd = sys.argv[1]
    if cmd == "list":
        list_profiles()
    elif cmd == "remove" and len(sys.argv) > 2:
        remove_profile(sys.argv[2])
    elif cmd == "update" and len(sys.argv) > 4:
        update_profile(sys.argv[2], sys.argv[3], " ".join(sys.argv[4:]))
    else:
        print("Usage: gi-profile-manager.py [list|remove <name>|update <name> <field> <value>]")

if __name__ == "__main__":
    main()
