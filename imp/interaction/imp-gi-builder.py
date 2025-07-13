from pathlib import Path
import json
import time
import importlib.util

HEAVY_VERIFIER = Path(__file__).resolve().parents[1] / "security" / "imp-heavy-identity-verifier.py"
spec = importlib.util.spec_from_file_location("heavy", HEAVY_VERIFIER)
heavy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(heavy)
verify_user = heavy.verify_user

BASE_DIR = Path(__file__).resolve().parents[1]
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
        "gender": "female",
    }

    profiles = load_profiles()
    profiles.append(profile)
    save_profiles(profiles)
    print(f"[+] Created intelligence profile for {name}")


if __name__ == "__main__":
    create_profile()
