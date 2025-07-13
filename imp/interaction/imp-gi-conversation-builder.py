from pathlib import Path
import json
import time
import importlib.util
import sys

BASE_DIR = Path(__file__).resolve().parents[1]
CHATBOT_PATH = BASE_DIR / "interaction" / "imp-chatbot.py"
HEAVY_VERIFIER = BASE_DIR / "security" / "imp-heavy-identity-verifier.py"
PROFILE_FILE = BASE_DIR / "config" / "imp-general-intelligences.json"

spec = importlib.util.spec_from_file_location("chatbot", CHATBOT_PATH)
chatbot = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chatbot)

spec2 = importlib.util.spec_from_file_location("heavy", HEAVY_VERIFIER)
heavy = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(heavy)
verify_user = heavy.verify_user
sys.path.append(str(BASE_DIR / "core"))
from imp_gi_goal_updater import update_goal_status
spec_pa = importlib.util.spec_from_file_location(
    "perception", BASE_DIR / "interaction" / "imp-perception-analyzer.py"
)
perception = importlib.util.module_from_spec(spec_pa)
spec_pa.loader.exec_module(perception)


def load_profiles():
    if PROFILE_FILE.exists():
        with open(PROFILE_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def save_profiles(profiles):
    with open(PROFILE_FILE, "w") as f:
        json.dump(profiles, f, indent=4)


def ask(question: str) -> str:
    chatbot.append_history("imp", question)
    try:
        answer = input(f"{question}\n> ")
    except EOFError:
        answer = ""
    chatbot.append_history("user", answer)
    return answer.strip()


def build_via_conversation():
    if not verify_user():
        return
    name, _ = chatbot.load_personality()
    chatbot.append_history("imp", f"{name}: Let's design your new intelligence.")

    profiles = load_profiles()
    chosen_name = ask("What will you name this intelligence?")
    if any(p.get("name") == chosen_name for p in profiles):
        print("🚫 A profile with this name already exists.")
        return

    profile = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "name": chosen_name,
        "description": ask("Give a short description of her purpose:"),
        "skills": [s.strip() for s in ask("List key skills (comma separated):").split(',') if s.strip()],
        "personality": [t.strip() for t in ask("Desired personality traits (comma separated):").split(',') if t.strip()],
        "conversation_style": ask("Preferred conversational personality?"),
        "focus_area": ask("Primary focus area:"),
        "autonomy": ask("Desired autonomy level (1-10):"),
        "learning_style": ask("Preferred learning style:"),
        "environment": ask("Deployment environment (cloud/local/hybrid):"),
        "security_level": ask("Desired security level (1-10):"),
        "safety_guidelines": ask("Any safety guidelines or restrictions?"),
        "gender": "female",
    }
    analysis = perception.analyze_perception()
    if analysis:
        profile["suggested_personality"] = analysis.get("suggested_personality")

    profiles = load_profiles()
    profiles.append(profile)
    save_profiles(profiles)
    update_goal_status("conversation-driven GI builder")
    update_goal_status("safety guidelines")
    update_goal_status("perception-based personality")
    update_goal_status("Integrate GI build workflow")
    print(f"[+] Conversation profile created for {profile['name']}")


if __name__ == "__main__":
    build_via_conversation()
