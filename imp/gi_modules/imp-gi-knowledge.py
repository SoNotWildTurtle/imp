from pathlib import Path
import json
import time
import sys

BASE_DIR = Path(__file__).resolve().parents[1]
KNOWLEDGE_FILE = BASE_DIR / "logs" / "imp-gi-knowledge.json"
INSIGHTS_FILE = BASE_DIR / "logs" / "imp-conversation-insights.json"


def load_knowledge():
    if not KNOWLEDGE_FILE.exists():
        return []
    with open(KNOWLEDGE_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_knowledge(entries):
    with open(KNOWLEDGE_FILE, "w") as f:
        json.dump(entries, f, indent=4)


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
    store_knowledge(name, "conversation", ", ".join(words))


def store_knowledge(name: str, topic: str, detail: str):
    entries = load_knowledge()
    entries.append({
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "name": name,
        "topic": topic,
        "knowledge": detail,
    })
    save_knowledge(entries)
    print(f"[+] Knowledge stored for {name}")


def list_knowledge(name: str | None = None):
    entries = load_knowledge()
    if name:
        entries = [e for e in entries if e.get("name") == name]
    for e in entries:
        print(f"{e['timestamp']} [{e['name']}/{e['topic']}] {e['knowledge']}")


def clear_knowledge(name: str | None = None):
    entries = load_knowledge()
    if name:
        entries = [e for e in entries if e.get("name") != name]
    else:
        entries = []
    save_knowledge(entries)
    target = name if name else "all"
    print(f"[+] Knowledge cleared for {target}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 imp-gi-knowledge.py <name> <topic> <knowledge> | list [<name>] | clear [<name>] | update <name>")
    elif sys.argv[1] == "list":
        name = sys.argv[2] if len(sys.argv) > 2 else None
        list_knowledge(name)
    elif sys.argv[1] == "clear":
        name = sys.argv[2] if len(sys.argv) > 2 else None
        clear_knowledge(name)
    elif sys.argv[1] == "update":
        if len(sys.argv) < 3:
            print("Usage: python3 imp-gi-knowledge.py update <name>")
        else:
            update_from_conversation(sys.argv[2])
    else:
        if len(sys.argv) < 4:
            print("Usage: python3 imp-gi-knowledge.py <name> <topic> <knowledge>")
        else:
            store_knowledge(sys.argv[1], sys.argv[2], " ".join(sys.argv[3:]))
