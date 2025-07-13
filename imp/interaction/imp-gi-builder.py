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
PROFILE_FILE = BASE_DIR / "config" / "imp-general-intelligences.json"


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
    name = input("Intelligence name: ").strip()
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
        "gender": "female",
    }
    analysis = perception.analyze_perception()
    if analysis:
        profile["suggested_personality"] = analysis.get("suggested_personality")

    profiles = load_profiles()
    profiles.append(profile)
    save_profiles(profiles)
    update_goal_status("environment and security level")
    update_goal_status("safety guidelines")
    update_goal_status("perception-based personality")
    update_goal_status("Integrate GI build workflow")
    print(f"[+] Created intelligence profile for {name}")


if __name__ == "__main__":
    create_profile()
