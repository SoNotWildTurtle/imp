import json
import time
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
CONSENT_FILE = BASE_DIR / "config" / "imp-consent.json"
LOG_FILE = BASE_DIR / "logs" / "imp-safety-log.json"

def has_consent():
    if not CONSENT_FILE.exists():
        return False
    with open(CONSENT_FILE, "r") as f:
        data = json.load(f)
    return data.get("safety_monitor", False)

def log_event(event):
    entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "event": event,
    }
    if LOG_FILE.exists():
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []
    data.append(entry)
    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=4)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--event", default="ping", help="Safety event to record")
    args = parser.parse_args()

    if has_consent():
        log_event(args.event)
        print(f"[+] Logged safety event: {args.event}")
    else:
        print("[!] Safety monitoring not enabled by user consent.")

if __name__ == "__main__":
    main()
