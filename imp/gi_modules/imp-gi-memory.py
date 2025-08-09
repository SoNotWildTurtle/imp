from pathlib import Path
import json
import time
import sys

BASE_DIR = Path(__file__).resolve().parents[1]
MEMORY_FILE = BASE_DIR / "logs" / "imp-gi-memory.json"
INSIGHTS_FILE = BASE_DIR / "logs" / "imp-conversation-insights.json"


def load_memory():
    if not MEMORY_FILE.exists():
        return []
    with open(MEMORY_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_memory(entries):
    with open(MEMORY_FILE, "w") as f:
        json.dump(entries, f, indent=4)


def latest_keywords() -> list[str]:
    """Return the most recent conversation keywords if available."""
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
    """Store a memory entry summarizing recent conversation topics."""
    words = latest_keywords()
    if not words:
        print("[!] No conversation insights available")
        return
    detail = "Conversation keywords: " + ", ".join(words)
    store_memory(name, detail)


def store_memory(name: str, detail: str):
    entries = load_memory()
    entries.append({
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "name": name,
        "memory": detail,
    })
    save_memory(entries)
    print(f"[+] Memory stored for {name}")


def list_memory(name: str | None = None):
    entries = load_memory()
    if name:
        entries = [e for e in entries if e.get("name") == name]
    for e in entries:
        print(f"{e['timestamp']} [{e['name']}] {e['memory']}")


def clear_memory(name: str | None = None):
    entries = load_memory()
    if name:
        entries = [e for e in entries if e.get("name") != name]
    else:
        entries = []
    save_memory(entries)
    target = name if name else "all"
    print(f"[+] Memory cleared for {target}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 imp-gi-memory.py <name> <memory> | list [<name>] | clear [<name>] | update <name>")
    elif sys.argv[1] == "list":
        name = sys.argv[2] if len(sys.argv) > 2 else None
        list_memory(name)
    elif sys.argv[1] == "clear":
        name = sys.argv[2] if len(sys.argv) > 2 else None
        clear_memory(name)
    elif sys.argv[1] == "update":
        if len(sys.argv) < 3:
            print("Usage: python3 imp-gi-memory.py update <name>")
        else:
            update_from_conversation(sys.argv[2])
    else:
        if len(sys.argv) < 3:
            print("Usage: python3 imp-gi-memory.py <name> <memory>")
        else:
            store_memory(sys.argv[1], " ".join(sys.argv[2:]))

