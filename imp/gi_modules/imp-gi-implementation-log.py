from pathlib import Path
import json
import time
import sys

BASE_DIR = Path(__file__).resolve().parents[1]
IMPL_FILE = BASE_DIR / "logs" / "imp-gi-implementation-log.json"
INSIGHTS_FILE = BASE_DIR / "logs" / "imp-conversation-insights.json"


def load_entries():
    if not IMPL_FILE.exists():
        return []
    with open(IMPL_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_entries(entries):
    IMPL_FILE.parent.mkdir(exist_ok=True)
    with open(IMPL_FILE, "w") as f:
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


def store_entry(name: str, detail: str):
    entries = load_entries()
    entries.append({
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "name": name,
        "detail": detail,
    })
    save_entries(entries)
    print(f"[+] Implementation stored for {name}")


def update_from_conversation(name: str):
    words = latest_keywords()
    if not words:
        print("[!] No conversation insights available")
        return
    store_entry(name, "Conversation keywords: " + ", ".join(words))


def list_entries(name: str | None = None):
    entries = load_entries()
    if name:
        entries = [e for e in entries if e.get("name") == name]
    for e in entries:
        print(f"{e['timestamp']} [{e['name']}] {e['detail']}")


def clear_entries(name: str | None = None):
    entries = load_entries()
    if name:
        entries = [e for e in entries if e.get("name") != name]
    else:
        entries = []
    save_entries(entries)
    target = name if name else "all"
    print(f"[+] Implementation log cleared for {target}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python3 imp-gi-implementation-log.py <name> <detail> | list [<name>] | clear [<name>] | update <name>"
        )
    elif sys.argv[1] == "list":
        name = sys.argv[2] if len(sys.argv) > 2 else None
        list_entries(name)
    elif sys.argv[1] == "clear":
        name = sys.argv[2] if len(sys.argv) > 2 else None
        clear_entries(name)
    elif sys.argv[1] == "update":
        if len(sys.argv) < 3:
            print("Usage: python3 imp-gi-implementation-log.py update <name>")
        else:
            update_from_conversation(sys.argv[2])
    else:
        if len(sys.argv) < 3:
            print("Usage: python3 imp-gi-implementation-log.py <name> <detail>")
        else:
            store_entry(sys.argv[1], " ".join(sys.argv[2:]))
