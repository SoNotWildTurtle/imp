from pathlib import Path
import json
import time
import sys

BASE_DIR = Path(__file__).resolve().parents[1]
SKILL_FILE = BASE_DIR / "logs" / "imp-gi-skills.json"
INSIGHTS_FILE = BASE_DIR / "logs" / "imp-conversation-insights.json"


def load_skills():
    if not SKILL_FILE.exists():
        return []
    with open(SKILL_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_skills(data):
    with open(SKILL_FILE, "w") as f:
        json.dump(data, f, indent=4)


def add_skill(name: str, skill: str):
    data = load_skills()
    data.append({
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "name": name,
        "skill": skill,
    })
    save_skills(data)
    print(f"[+] Skill recorded for {name}")


def latest_keywords() -> list[str]:
    if not INSIGHTS_FILE.exists():
        return []
    try:
        with open(INSIGHTS_FILE, "r") as f:
            data = json.load(f)
            if data:
                return [w for w, _ in data[-1].get("top_words", [])]
    except json.JSONDecodeError:
        pass
    return []


def update_from_conversation(name: str):
    words = latest_keywords()
    if not words:
        print("[!] No conversation insights available")
        return
    for w in words:
        add_skill(name, w)


def list_skills(name: str | None = None):
    data = load_skills()
    if name:
        data = [d for d in data if d.get("name") == name]
    for d in data:
        print(f"{d['timestamp']} [{d['name']}] {d['skill']}")


def clear_skills(name: str | None = None):
    data = load_skills()
    if name:
        data = [d for d in data if d.get("name") != name]
    else:
        data = []
    save_skills(data)
    target = name if name else "all"
    print(f"[+] Skills cleared for {target}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python3 imp-gi-skill-tracker.py <name> <skill> | list [<name>] | clear [<name>] | update <name>"
        )
    elif sys.argv[1] == "list":
        name = sys.argv[2] if len(sys.argv) > 2 else None
        list_skills(name)
    elif sys.argv[1] == "clear":
        name = sys.argv[2] if len(sys.argv) > 2 else None
        clear_skills(name)
    elif sys.argv[1] == "update":
        if len(sys.argv) < 3:
            print("Usage: python3 imp-gi-skill-tracker.py update <name>")
        else:
            update_from_conversation(sys.argv[2])
    else:
        if len(sys.argv) < 3:
            print("Usage: python3 imp-gi-skill-tracker.py <name> <skill>")
        else:
            add_skill(sys.argv[1], " ".join(sys.argv[2:]))
