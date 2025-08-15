from pathlib import Path
import json
import time
import sys

BASE_DIR = Path(__file__).resolve().parents[1]
SAFETY_FILE = BASE_DIR / "logs" / "imp-gi-safety.json"
INSIGHTS_FILE = BASE_DIR / "logs" / "imp-conversation-insights.json"


def load_guidelines():
    if not SAFETY_FILE.exists():
        return []
    with open(SAFETY_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_guidelines(entries):
    SAFETY_FILE.parent.mkdir(exist_ok=True)
    with open(SAFETY_FILE, "w") as f:
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


def store_guideline(name: str, guideline: str):
    entries = load_guidelines()
    entries.append({
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "name": name,
        "guideline": guideline,
    })
    save_guidelines(entries)
    print(f"[+] Guideline stored for {name}")


def update_from_conversation(name: str):
    words = latest_keywords()
    if not words:
        print("[!] No conversation insights available")
        return
    text = "Guidelines based on conversation: " + ", ".join(words)
    store_guideline(name, text)


def list_guidelines(name: str | None = None):
    entries = load_guidelines()
    if name:
        entries = [e for e in entries if e.get("name") == name]
    for e in entries:
        print(f"{e['timestamp']} [{e['name']}] {e['guideline']}")


def clear_guidelines(name: str | None = None):
    entries = load_guidelines()
    if name:
        entries = [e for e in entries if e.get("name") != name]
    else:
        entries = []
    save_guidelines(entries)
    target = name if name else "all"
    print(f"[+] Safety guidelines cleared for {target}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python3 imp-gi-safety.py <name> <guideline> | list [<name>] | clear [<name>] | update <name>"
        )
    elif sys.argv[1] == "list":
        name = sys.argv[2] if len(sys.argv) > 2 else None
        list_guidelines(name)
    elif sys.argv[1] == "clear":
        name = sys.argv[2] if len(sys.argv) > 2 else None
        clear_guidelines(name)
    elif sys.argv[1] == "update":
        if len(sys.argv) < 3:
            print("Usage: python3 imp-gi-safety.py update <name>")
        else:
            update_from_conversation(sys.argv[2])
    else:
        if len(sys.argv) < 3:
            print("Usage: python3 imp-gi-safety.py <name> <guideline>")
        else:
            store_guideline(sys.argv[1], " ".join(sys.argv[2:]))
