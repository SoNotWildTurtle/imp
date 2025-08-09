from pathlib import Path
import json
import time
import importlib.util
import sys
import re
from collections import Counter

BASE_DIR = Path(__file__).resolve().parents[1]
CHATBOT_PATH = BASE_DIR / "interaction" / "imp-chatbot.py"
HEAVY_VERIFIER = BASE_DIR / "security" / "imp-heavy-identity-verifier.py"
PROFILE_FILE = BASE_DIR / "config" / "imp-general-intelligences.json"
MODULES_DIR = BASE_DIR / "gi_modules"

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
spec_ca = importlib.util.spec_from_file_location(
    "conv", BASE_DIR / "interaction" / "imp-conversation-analyzer.py"
)
conv = importlib.util.module_from_spec(spec_ca)
spec_ca.loader.exec_module(conv)


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


def list_available_modules():
    return sorted([p.name for p in MODULES_DIR.glob("imp-gi-*.py")])


KEYWORD_MODULE_MAP = {
    "security": ["imp-gi-risk-analyzer.py", "imp-gi-safety.py"],
    "memory": ["imp-gi-memory.py"],
    "plan": ["imp-gi-planner.py"],
    "performance": ["imp-gi-performance.py"],
    "communication": ["imp-gi-comm-log.py"],
}


def suggest_modules_from_keywords(keywords):
    suggested = []
    for kw in keywords:
        low = kw.lower()
        for key, mods in KEYWORD_MODULE_MAP.items():
            if key in low:
                for m in mods:
                    if m not in suggested:
                        suggested.append(m)
    return suggested


def choose_modules(defaults):
    mods = list_available_modules()
    for i, m in enumerate(mods, 1):
        mark = " (default)" if m in defaults else ""
        print(f"{i}. {m}{mark}")
    sel = ask(
        "Enter module numbers to include (comma separated) or press Enter for defaults:"
    )
    if not sel:
        return defaults
    chosen = []
    for part in sel.split(','):
        try:
            idx = int(part.strip()) - 1
            if 0 <= idx < len(mods):
                chosen.append(mods[idx])
        except ValueError:
            continue
    return chosen or defaults


def ask(question: str) -> str:
    chatbot.append_history("imp", question)
    try:
        answer = input(f"{question}\n> ")
    except EOFError:
        answer = ""
    chatbot.append_history("user", answer)
    return answer.strip()


def gather_requirements():
    print("Describe what this intelligence should do. Type 'done' when finished.")
    messages = []
    while True:
        try:
            msg = input("You: ")
        except EOFError:
            break
        if not msg or msg.strip().lower() in {"done", "quit", "exit"}:
            break
        messages.append(msg)
        chatbot.append_history("user", msg)
        response = chatbot.generate_response(msg)
        print(response)
    text = " ".join(messages)
    words = re.findall(r"[a-zA-Z']{4,}", text.lower())
    counts = Counter(words)
    keywords = [w for w, _ in counts.most_common(5)]
    conv.run_analysis()
    return keywords


def build_via_conversation():
    if not verify_user():
        return
    name, _ = chatbot.load_personality()
    chatbot.append_history("imp", f"{name}: Let's design your new intelligence.")

    keywords = gather_requirements()
    suggested_modules = suggest_modules_from_keywords(keywords)
    profiles = load_profiles()
    chosen_name = ask("What will you name this intelligence?")
    if any(p.get("name") == chosen_name for p in profiles):
        print("🚫 A profile with this name already exists.")
        return

    profile = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "name": chosen_name,
        "description": ask("Give a short description of her purpose:"),
        "skills": None,
        "personality": [t.strip() for t in ask("Desired personality traits (comma separated):").split(',') if t.strip()],
        "conversation_style": ask("Preferred conversational personality?"),
        "focus_area": None,
        "autonomy": ask("Desired autonomy level (1-10):"),
        "learning_style": ask("Preferred learning style:"),
        "environment": ask("Deployment environment (cloud/local/hybrid):"),
        "security_level": ask("Desired security level (1-10):"),
        "safety_guidelines": ask("Any safety guidelines or restrictions?"),
        "dashboard_port": ask("Conversation dashboard port (e.g., 5000):"),
        "gender": "female",
        "modules": None,
    }
    skill_prompt = "List key skills (comma separated)"
    if keywords:
        skill_prompt += f" (suggestions: {', '.join(keywords[:3])})"
    skill_ans = ask(f"{skill_prompt}:")
    skills = [s.strip() for s in skill_ans.split(',') if s.strip()]
    if not skills and keywords:
        skills = keywords[:3]
    profile["skills"] = skills

    focus_prompt = "Primary focus area"
    if keywords:
        focus_prompt += f" (suggestion: {keywords[0]})"
    focus_ans = ask(f"{focus_prompt}:")
    profile["focus_area"] = focus_ans or (keywords[0] if keywords else "")

    base_defaults = [
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
    defaults = base_defaults + [m for m in suggested_modules if m not in base_defaults]
    profile["modules"] = choose_modules(defaults)
    if suggested_modules:
        profile["suggested_modules"] = suggested_modules
    if keywords:
        profile["conversation_keywords"] = keywords
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
