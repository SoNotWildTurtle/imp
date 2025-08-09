from pathlib import Path
import json
import sys
import time
import importlib.util

BASE_DIR = Path(__file__).resolve().parents[1]
ALIAS_FILE = BASE_DIR / "config" / "imp-gi-aliases.json"
COMM_LOG = BASE_DIR / "logs" / "imp-gi-comm-log.json"

HEAVY_VERIFIER = BASE_DIR / "security" / "imp-heavy-identity-verifier.py"
spec = importlib.util.spec_from_file_location("heavy", HEAVY_VERIFIER)
heavy = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(heavy)
    verify_user = heavy.verify_user
except Exception:
    def verify_user():
        print("⚠️ Verification unavailable.")
        return False


def load_aliases():
    if ALIAS_FILE.exists():
        with open(ALIAS_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}


def save_log(entry):
    logs = []
    if COMM_LOG.exists():
        with open(COMM_LOG, "r") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
    logs.append(entry)
    with open(COMM_LOG, "w") as f:
        json.dump(logs, f, indent=4)


def checkin(alias: str, message: str):
    aliases = load_aliases()
    if alias not in aliases:
        print("🚫 Unknown alias")
        return
    save_log({
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "alias": alias,
        "message": message,
    })
    print("[+] Check-in recorded.")


def request_evolution(alias: str, message: str):
    aliases = load_aliases()
    if alias not in aliases:
        print("🚫 Unknown alias")
        return
    if not verify_user():
        return
    save_log({
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "alias": alias,
        "evolution_request": message,
    })
    print("[+] Evolution request logged.")


def main():
    if len(sys.argv) < 4:
        print("Usage: gi-communicator.py [checkin|request-evolution] <alias> <message>")
        return
    cmd = sys.argv[1]
    alias = sys.argv[2]
    message = " ".join(sys.argv[3:])
    if cmd == "checkin":
        checkin(alias, message)
    elif cmd == "request-evolution":
        request_evolution(alias, message)
    else:
        print("Usage: gi-communicator.py [checkin|request-evolution] <alias> <message>")


if __name__ == "__main__":
    main()
