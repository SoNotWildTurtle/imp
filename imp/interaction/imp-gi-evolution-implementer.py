from pathlib import Path
import json
import time
import importlib.util

def sanitize(name: str) -> str:
    return "".join(c if c.isalnum() else "_" for c in name.lower())

BASE_DIR = Path(__file__).resolve().parents[1]
PLAN_FILE = BASE_DIR / "logs" / "imp-gi-evolution-plans.json"
IMPL_LOG = BASE_DIR / "logs" / "imp-gi-implementation-log.json"
VERIFIER = BASE_DIR / "security" / "imp-heavy-identity-verifier.py"
CONFIG_DIR = BASE_DIR / "config" / "gi"
CUSTOM_DIR = BASE_DIR / "gi_modules" / "custom"

spec = importlib.util.spec_from_file_location("heavy", VERIFIER)
heavy = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(heavy)
    verify_user = heavy.verify_user
except Exception:
    def verify_user():
        print("⚠️ Verification unavailable.")
        return False


def load_plans():
    if PLAN_FILE.exists():
        with open(PLAN_FILE, "r") as f:
            try:
                return json.load(f).get("plans", {})
            except json.JSONDecodeError:
                return {}
    return {}


def save_impl(entry):
    data = []
    if IMPL_LOG.exists():
        with open(IMPL_LOG, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    data.append(entry)
    with open(IMPL_LOG, "w") as f:
        json.dump(data, f, indent=4)


def push_functionality(alias: str, request: str):
    CUSTOM_DIR.mkdir(exist_ok=True)
    mod_name = f"{alias}_{sanitize(request)}.py"
    mod_path = CUSTOM_DIR / mod_name
    if not mod_path.exists():
        with open(mod_path, "w") as f:
            f.write(
                "def run():\n"
                f"    print('Placeholder for {request}')\n"
            )
    config_path = CONFIG_DIR / f"{alias}.json"
    if config_path.exists():
        with open(config_path, "r") as f:
            try:
                config = json.load(f)
            except json.JSONDecodeError:
                config = {}
    else:
        config = {}
    modules = config.get("modules", [])
    rel_path = f"custom/{mod_name}"
    if rel_path not in modules:
        modules.append(rel_path)
    config["modules"] = modules
    with open(config_path, "w") as f:
        json.dump(config, f, indent=4)


def implement_plans():
    plans = load_plans()
    if not plans:
        print("No evolution plans to implement.")
        return
    for alias, requests in plans.items():
        for req in requests:
            approve = input(f"Approve evolution request from {alias}: '{req}'? (y/n) ")
            if approve.lower() != 'y':
                continue
            plan = f"Implement feature: {req}"
            approve_plan = input(f"Approve development plan '{plan}'? (y/n) ")
            if approve_plan.lower() != 'y':
                continue
            save_impl({
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "alias": alias,
                "request": req,
                "plan": plan,
                "status": "implemented"
            })
            push_functionality(alias, req)
            print(f"[+] Implemented and pushed plan for {alias}")


def main():
    if not verify_user():
        return
    implement_plans()


if __name__ == "__main__":
    main()
