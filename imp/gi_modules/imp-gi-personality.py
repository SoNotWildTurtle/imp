from pathlib import Path
import json
import time
import sys

BASE_DIR = Path(__file__).resolve().parents[1]
MOOD_FILE = BASE_DIR / "logs" / "imp-gi-personality.json"
BASELINE = 0
RESTING = BASELINE + 1

def load_entries():
    if MOOD_FILE.exists():
        try:
            with open(MOOD_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_entries(entries):
    with open(MOOD_FILE, "w") as f:
        json.dump(entries, f, indent=4)

def last_mood(entries, name):
    for e in reversed(entries):
        if e.get("name") == name:
            return e.get("mood")
    return None

def measure_mood(name: str):
    entries = load_entries()
    current = last_mood(entries, name)
    if current is None:
        mood = RESTING
    elif current > RESTING:
        mood = current - 1
    elif current < RESTING:
        mood = current + 1
    else:
        mood = current
    entries.append({
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "name": name,
        "mood": mood,
    })
    save_entries(entries)
    print(f"[+] {name}'s mood is {mood}")
    return mood

def set_mood(name: str, mood: int | str):
    entries = load_entries()
    mood = int(mood)
    entries.append({
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "name": name,
        "mood": mood,
    })
    save_entries(entries)
    print(f"[+] Mood for {name} set to {mood}")

def list_mood(name: str | None = None):
    entries = load_entries()
    if name:
        entries = [e for e in entries if e.get("name") == name]
    for e in entries:
        print(f"{e['timestamp']} [{e['name']}] {e['mood']}")

def clear_mood(name: str | None = None):
    entries = load_entries()
    if name:
        entries = [e for e in entries if e.get("name") != name]
    else:
        entries = []
    save_entries(entries)
    target = name if name else "all"
    print(f"[+] Mood cleared for {target}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 imp-gi-personality.py <name> <mood> | measure <name> | list [<name>] | clear [<name>]")
    elif sys.argv[1] == "list":
        name = sys.argv[2] if len(sys.argv) > 2 else None
        list_mood(name)
    elif sys.argv[1] == "clear":
        name = sys.argv[2] if len(sys.argv) > 2 else None
        clear_mood(name)
    elif sys.argv[1] in ("measure", "update"):
        if len(sys.argv) < 3:
            print("Usage: python3 imp-gi-personality.py measure <name>")
        else:
            measure_mood(sys.argv[2])
    else:
        if len(sys.argv) < 3:
            print("Usage: python3 imp-gi-personality.py <name> <mood>")
        else:
            set_mood(sys.argv[1], sys.argv[2])
