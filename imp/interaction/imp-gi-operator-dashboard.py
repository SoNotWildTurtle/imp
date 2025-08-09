from pathlib import Path
import json
import time
import importlib.util

BASE_DIR = Path(__file__).resolve().parents[1]
REQUEST_FILE = BASE_DIR / "logs" / "imp-gi-requests.json"
DECISION_LOG = BASE_DIR / "logs" / "imp-gi-upgrade-decisions.json"
VERIFIER = BASE_DIR / "security" / "imp-heavy-identity-verifier.py"

SNAPSHOT = BASE_DIR / "interaction" / "imp-gi-snapshot.py"
PLANNER = BASE_DIR / "gi_modules" / "imp-gi-planner.py"
IMPLEMENTER = BASE_DIR / "gi_modules" / "imp-gi-implementation-log.py"

spec = importlib.util.spec_from_file_location("heavy", VERIFIER)
heavy = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(heavy)
    verify_user = heavy.verify_user
except Exception:
    def verify_user():
        print("⚠️ Verification unavailable.")
        return False

spec_s = importlib.util.spec_from_file_location("snap", SNAPSHOT)
snap = importlib.util.module_from_spec(spec_s)
spec_s.loader.exec_module(snap)
snapshot_config = snap.snapshot_config

spec_p = importlib.util.spec_from_file_location("planner", PLANNER)
planner = importlib.util.module_from_spec(spec_p)
spec_p.loader.exec_module(planner)

spec_i = importlib.util.spec_from_file_location("impl", IMPLEMENTER)
impl = importlib.util.module_from_spec(spec_i)
spec_i.loader.exec_module(impl)


def load_requests():
    if REQUEST_FILE.exists():
        with open(REQUEST_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def save_requests(data):
    with open(REQUEST_FILE, "w") as f:
        json.dump(data, f, indent=4)


def save_decision(entry):
    data = []
    if DECISION_LOG.exists():
        with open(DECISION_LOG, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    data.append(entry)
    with open(DECISION_LOG, "w") as f:
        json.dump(data, f, indent=4)


def dashboard():
    requests = load_requests()
    if not requests:
        print("No upgrade requests found.")
        return
    remaining = []
    for req in requests:
        name = req.get("name")
        detail = req.get("request")
        ans = input(f"Approve upgrade request from {name}: '{detail}'? (y/n) ")
        decision = "approved" if ans.lower() == "y" else "denied"
        save_decision({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "alias": name,
            "request": detail,
            "decision": decision,
        })
        if decision == "approved":
            snapshot_config(name)
            plan = f"Implement: {detail}"
            planner.add_plan(name, plan)
            if input(f"Implement plan for {name}? (y/n) ").lower() == "y":
                impl.store_entry(name, plan)
            else:
                remaining.append(req)
        else:
            remaining.append(req)
    save_requests(remaining)


def main():
    if not verify_user():
        return
    dashboard()


if __name__ == "__main__":
    main()
