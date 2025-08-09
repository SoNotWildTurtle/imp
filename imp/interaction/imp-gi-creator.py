from pathlib import Path
import json
import time
import importlib.util
import sys

HEAVY_VERIFIER = Path(__file__).resolve().parents[1] / "security" / "imp-heavy-identity-verifier.py"
spec = importlib.util.spec_from_file_location("heavy", HEAVY_VERIFIER)
heavy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(heavy)
verify_user = heavy.verify_user
sys.path.append(str(Path(__file__).resolve().parents[1] / "core"))
from imp_gi_goal_updater import update_goal_status

BASE_DIR = Path(__file__).resolve().parents[1]
PROFILE_FILE = BASE_DIR / "config" / "imp-general-intelligences.json"
CONFIG_DIR = BASE_DIR / "config" / "gi"
BUILD_LOG = BASE_DIR / "logs" / "imp-gi-build-log.json"


def load_profiles():
    if PROFILE_FILE.exists():
        with open(PROFILE_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def save_log(entry):
    logs = []
    if BUILD_LOG.exists():
        with open(BUILD_LOG, "r") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
    logs.append(entry)
    with open(BUILD_LOG, "w") as f:
        json.dump(logs, f, indent=4)


def build_intelligence():
    if not verify_user():
        return
    profiles = load_profiles()
    if not profiles:
        print("No profiles available. Run the GI builder first.")
        return
    for i, p in enumerate(profiles, 1):
        print(f"{i}. {p['name']}: {p.get('description','')}")
    choice = input("Select profile number: ").strip()
    try:
        idx = int(choice) - 1
        profile = profiles[idx]
    except Exception:
        print("Invalid selection")
        return

    CONFIG_DIR.mkdir(exist_ok=True)
    config_path = CONFIG_DIR / f"{profile['name']}.json"
    config = {
        "name": profile["name"],
        "description": profile.get("description", ""),
        "skills": profile.get("skills", []),
        "personality": profile.get("personality", []),
        "conversation_style": profile.get("conversation_style", ""),
        "focus_area": profile.get("focus_area", ""),
        "autonomy": profile.get("autonomy", ""),
        "learning_style": profile.get("learning_style", ""),
        "environment": profile.get("environment", ""),
        "security_level": profile.get("security_level", ""),
        "safety_guidelines": profile.get("safety_guidelines", ""),
        "suggested_personality": profile.get("suggested_personality", ""),
        "dashboard_port": profile.get("dashboard_port", ""),
        "modules": profile.get(
            "modules",
            [
                "imp-gi-memory.py",
                "imp-gi-task-manager.py",
                "imp-gi-self-evolver.py",
                "imp-gi-knowledge.py",
                "imp-gi-skill-tracker.py",
                "imp-gi-performance.py",
                "imp-gi-safety.py",
                "imp-gi-risk-analyzer.py",
                "imp-gi-planner.py",
                "imp-gi-comm-log.py",
                "imp-gi-implementation-log.py",
                "imp-gi-request.py",
            ],
        ),
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    with open(config_path, "w") as f:
        json.dump(config, f, indent=4)
    save_log({"timestamp": config["created"], "profile": profile["name"]})
    update_goal_status("Create GI creator utility")
    update_goal_status("Save generated configs")
    update_goal_status("Log builds")
    update_goal_status("Provide automated tests")
    update_goal_status("Integrate GI build workflow")
    print(f"[+] Built intelligence config at {config_path}")


if __name__ == "__main__":
    build_intelligence()
