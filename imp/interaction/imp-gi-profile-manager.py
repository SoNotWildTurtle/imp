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


def main():
    if len(sys.argv) < 2:
        print("Usage: gi-profile-manager.py [list|remove <name>]")
        return
    if not verify_user():
        return
    cmd = sys.argv[1]
    if cmd == "list":
        list_profiles()
    elif cmd == "remove" and len(sys.argv) > 2:
        remove_profile(sys.argv[2])
    else:
        print("Usage: gi-profile-manager.py [list|remove <name>]")

if __name__ == "__main__":
    main()
