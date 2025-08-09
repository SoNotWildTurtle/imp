from pathlib import Path
import json
import time
import importlib.util
import sys

BASE_DIR = Path(__file__).resolve().parents[1]
CONFIG_DIR = BASE_DIR / "config" / "gi"
SNAP_FILE = BASE_DIR / "logs" / "imp-gi-snapshots.json"
VERIFIER = BASE_DIR / "security" / "imp-heavy-identity-verifier.py"

spec = importlib.util.spec_from_file_location("heavy", VERIFIER)
heavy = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(heavy)
    verify_user = heavy.verify_user
except Exception:
    def verify_user():
        print("⚠️ Verification unavailable.")
        return False

def load_snapshots():
    if SNAP_FILE.exists():
        with open(SNAP_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_snapshots(data):
    with open(SNAP_FILE, "w") as f:
        json.dump(data, f, indent=4)

def snapshot_config(name: str):
    config_path = CONFIG_DIR / f"{name}.json"
    if not config_path.exists():
        print(f"[!] Config not found for {name}")
        return
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except json.JSONDecodeError:
        print("[!] Invalid config file")
        return
    data = load_snapshots()
    data.append({
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "name": name,
        "config": config,
    })
    save_snapshots(data)
    print(f"[+] Snapshot saved for {name}")

def list_snapshots(name: str | None = None):
    data = load_snapshots()
    if name:
        data = [d for d in data if d.get("name") == name]
    for d in data:
        print(f"{d['timestamp']} [{d['name']}]")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 imp-gi-snapshot.py <name> | list [<name>]")
    elif sys.argv[1] == "list":
        name = sys.argv[2] if len(sys.argv) > 2 else None
        list_snapshots(name)
    else:
        if verify_user():
            snapshot_config(sys.argv[1])
