from pathlib import Path
import json
import time
import importlib.util

BASE_DIR = Path(__file__).resolve().parents[1]
COMM_LOG = BASE_DIR / "logs" / "imp-gi-comm-log.json"
PLAN_FILE = BASE_DIR / "logs" / "imp-gi-evolution-plans.json"
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


def load_comm_logs():
    if COMM_LOG.exists():
        with open(COMM_LOG, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def generate_plans():
    logs = load_comm_logs()
    plans = {}
    for entry in logs:
        alias = entry.get("alias")
        if not alias:
            continue
        req = entry.get("evolution_request")
        if req:
            plans.setdefault(alias, []).append(req)
    with open(PLAN_FILE, "w") as f:
        json.dump({"timestamp": time.strftime("%Y-%m-%d %H:%M:%S"), "plans": plans}, f, indent=4)
    print("[+] Evolution plans updated.")


def main():
    if not verify_user():
        return
    generate_plans()


if __name__ == "__main__":
    main()
