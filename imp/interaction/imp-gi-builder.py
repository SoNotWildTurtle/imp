from pathlib import Path
import json
import time
import importlib.util
import sys

BASE_DIR = Path(__file__).resolve().parents[1]
HEAVY_VERIFIER = BASE_DIR / "security" / "imp-heavy-identity-verifier.py"
spec = importlib.util.spec_from_file_location("heavy", HEAVY_VERIFIER)
heavy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(heavy)
verify_user = heavy.verify_user
sys.path.append(str(BASE_DIR / "core"))
from imp_gi_goal_updater import update_goal_status
spec_pa = importlib.util.spec_from_file_location(
    "perception", BASE_DIR / "interaction" / "imp-perception-analyzer.py"
)
perception = importlib.util.module_from_spec(spec_pa)
spec_pa.loader.exec_module(perception)
spec_exp = importlib.util.spec_from_file_location(
    "experience", BASE_DIR / "self-improvement" / "imp-gi-experience.py"
)
experience = importlib.util.module_from_spec(spec_exp)
spec_exp.loader.exec_module(experience)
PROFILE_FILE = BASE_DIR / "config" / "imp-general-intelligences.json"
MODULES_DIR = BASE_DIR / "gi_modules"


def list_available_modules():
    modules = [p.name for p in MODULES_DIR.glob("imp-gi-*.py")]
    return sorted(modules)


def choose_modules(defaults):
    modules = list_available_modules()
    print("Available modules:")
    for i, m in enumerate(modules, 1):
        mark = " (default)" if m in defaults else ""
        print(f"{i}. {m}{mark}")
    selection = input(
        "Enter module numbers to include (comma separated) or press Enter for defaults: "
    ).strip()
    if not selection:
        return defaults
    chosen = []
    for part in selection.split(','):
        try:
            idx = int(part.strip()) - 1
            if 0 <= idx < len(modules):
                chosen.append(modules[idx])
        except ValueError:
            continue
    return chosen or defaults


def load_profiles():
    if not PROFILE_FILE.exists():
        return []
    with open(PROFILE_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_profiles(profiles):
    with open(PROFILE_FILE, "w") as f:
        json.dump(profiles, f, indent=4)


def create_profile():
    if not verify_user():
        return
    print("📊", experience.summarize_experience())
    name = input("Intelligence name: ").strip()
    existing = [p.get("name") for p in load_profiles()]
    if name in existing:
        print("🚫 A profile with this name already exists.")
        return
    description = input("Short description: ").strip()
    skills = [s.strip() for s in input("Key skills (comma separated): ").split(',') if s.strip()]
    traits = [t.strip() for t in input("Personality traits (comma separated): ").split(',') if t.strip()]
    convo_style = input("What type of conversational personality do you want her to have? ").strip()
    focus_area = input("Primary domain of expertise: ").strip()
    autonomy = input("How autonomous should she be (1-10)? ").strip()
    learning_style = input("Preferred learning style: ").strip()
    environment = input("Deployment environment (cloud/local/hybrid): ").strip()
    security_level = input("Desired security level (1-10): ").strip()
    safety_guidelines = input("Any safety guidelines or restrictions? ").strip()
    dashboard_port = input("Conversation dashboard port (e.g., 5000): ").strip()
    built_in = [
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
    ]
    modules = choose_modules(built_in)

    profile = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "name": name,
        "description": description,
        "skills": skills,
        "personality": traits,
        "conversation_style": convo_style,
        "focus_area": focus_area,
        "autonomy": autonomy,
        "learning_style": learning_style,
        "environment": environment,
        "security_level": security_level,
        "safety_guidelines": safety_guidelines,
        "dashboard_port": dashboard_port,
        "gender": "female",
        "modules": modules,
    }
    analysis = perception.analyze_perception()
    if analysis:
        profile["suggested_personality"] = analysis.get("suggested_personality")

    profiles = load_profiles()
    profiles.append(profile)
    save_profiles(profiles)
    experience.update_experience()
    update_goal_status("environment and security level")
    update_goal_status("safety guidelines")
    update_goal_status("perception-based personality")
    update_goal_status("Integrate GI build workflow")
    print(f"[+] Created intelligence profile for {name}")


if __name__ == "__main__":
    create_profile()
