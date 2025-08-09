from pathlib import Path
import json
import time
import sys

BASE_DIR = Path(__file__).resolve().parents[1]
SUGGEST_FILE = BASE_DIR / "logs" / "imp-gi-evolution-suggestions.json"
INSIGHTS_FILE = BASE_DIR / "logs" / "imp-conversation-insights.json"
PERCEPTION_FILE = BASE_DIR / "logs" / "imp-perception-log.json"


def load_suggestions():
    if not SUGGEST_FILE.exists():
        return []
    with open(SUGGEST_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_suggestions(data):
    with open(SUGGEST_FILE, "w") as f:
        json.dump(data, f, indent=4)


def suggest_evolution(name: str, suggestion: str):
    data = load_suggestions()
    data.append({
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "name": name,
        "suggestion": suggestion,
    })
    save_suggestions(data)
    print(f"[+] Evolution suggestion logged for {name}")


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


def latest_personality() -> str:
    if not PERCEPTION_FILE.exists():
        return ""
    try:
        with open(PERCEPTION_FILE, "r") as f:
            data = json.load(f)
            if data:
                return data[-1].get("suggested_personality", "")
    except json.JSONDecodeError:
        pass
    return ""


def update_from_conversation(name: str):
    words = latest_keywords()
    personality = latest_personality()
    if not words and not personality:
        print("[!] No conversation insights available")
        return
    detail = "Enhance GI"
    if words:
        detail += " for " + ", ".join(words)
    if personality:
        detail += f" with {personality} personality"
    suggest_evolution(name, detail)


def list_suggestions(name: str | None = None):
    data = load_suggestions()
    if name:
        data = [d for d in data if d.get("name") == name]
    for d in data:
        print(f"{d['timestamp']} [{d['name']}] {d['suggestion']}")


def clear_suggestions(name: str | None = None):
    data = load_suggestions()
    if name:
        data = [d for d in data if d.get("name") != name]
    else:
        data = []
    save_suggestions(data)
    target = name if name else "all"
    print(f"[+] Suggestions cleared for {target}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 imp-gi-self-evolver.py <name> <suggestion> | list [<name>] | clear [<name>] | update <name>")
    elif sys.argv[1] == "list":
        name = sys.argv[2] if len(sys.argv) > 2 else None
        list_suggestions(name)
    elif sys.argv[1] == "clear":
        name = sys.argv[2] if len(sys.argv) > 2 else None
        clear_suggestions(name)
    elif sys.argv[1] == "update":
        if len(sys.argv) < 3:
            print("Usage: python3 imp-gi-self-evolver.py update <name>")
        else:
            update_from_conversation(sys.argv[2])
    else:
        if len(sys.argv) < 3:
            print("Usage: python3 imp-gi-self-evolver.py <name> <suggestion>")
        else:
            suggest_evolution(sys.argv[1], " ".join(sys.argv[2:]))

