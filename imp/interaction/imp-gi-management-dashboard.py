from pathlib import Path
import json
import importlib.util

BASE_DIR = Path(__file__).resolve().parents[1]
GI_FILE = BASE_DIR / "config" / "imp-general-intelligences.json"
REQUEST_FILE = BASE_DIR / "logs" / "imp-gi-requests.json"
SNAP_FILE = BASE_DIR / "logs" / "imp-gi-snapshots.json"
VERIFIER = BASE_DIR / "security" / "imp-heavy-identity-verifier.py"

spec = importlib.util.spec_from_file_location("heavy", VERIFIER)
heavy = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(heavy)
    verify_user = heavy.verify_user
except Exception:
    def verify_user():
        print("\u26a0\ufe0f Verification unavailable.")
        return False

def _read_json(path):
    if path.exists():
        with open(path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def list_gis():
    data = _read_json(GI_FILE)
    if not data:
        print("No intelligences found.")
        return
    print("Registered Intelligences:")
    for gi in data:
        name = gi.get("name")
        mods = ", ".join(gi.get("modules", []))
        print(f"- {name}: {mods}")

def view_requests():
    reqs = _read_json(REQUEST_FILE)
    if not reqs:
        print("No pending requests.")
        return
    print("Pending Requests:")
    for r in reqs:
        print(f"- {r.get('name')}: {r.get('request')}")

def view_snapshots():
    snaps = _read_json(SNAP_FILE)
    if not snaps:
        print("No snapshots recorded.")
        return
    print("Snapshots:")
    for s in snaps:
        print(f"- {s.get('name')}: {s.get('snapshot', 'config saved')}")

def dashboard():
    while True:
        print("\nGI Management Dashboard")
        print("1) List intelligences")
        print("2) View upgrade requests")
        print("3) View snapshots")
        print("q) Quit")
        choice = input("> ").strip().lower()
        if choice == "1":
            list_gis()
        elif choice == "2":
            view_requests()
        elif choice == "3":
            view_snapshots()
        elif choice == "q":
            break
        else:
            print("Invalid option.")

def main():
    if verify_user():
        dashboard()

if __name__ == "__main__":
    main()
