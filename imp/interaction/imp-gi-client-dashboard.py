from pathlib import Path
import json
import time
import importlib.util

BASE_DIR = Path(__file__).resolve().parents[1]
REQUEST_FILE = BASE_DIR / "logs" / "imp-gi-requests.json"
COMM_LOG = BASE_DIR / "logs" / "imp-gi-comm-log.json"
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

def load_requests():
    if REQUEST_FILE.exists():
        with open(REQUEST_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_requests(entries):
    with open(REQUEST_FILE, "w") as f:
        json.dump(entries, f, indent=4)

def append_comm_log(entry):
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

def dashboard():
    print("=== GI Client Dashboard ===")
    print("Review pending requests and forward them to the operator.")
    requests = load_requests()
    if not requests:
        print("No pending requests.")
        return
    remaining = []
    for req in requests:
        ans = input(f"Send request '{req['request']}' from {req['name']} to operator? (y/n) ")
        if ans.lower() == "y":
            append_comm_log({
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "alias": req["name"],
                "evolution_request": req["request"],
            })
            print("[+] Request sent to operator.")
        else:
            remaining.append(req)
            print("[-] Request kept pending.")
    save_requests(remaining)
    print("All requests processed.")

def main():
    if not verify_user():
        return
    dashboard()

if __name__ == "__main__":
    main()
