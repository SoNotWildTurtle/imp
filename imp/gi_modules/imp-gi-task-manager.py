from pathlib import Path
import json
import time
import sys

BASE_DIR = Path(__file__).resolve().parents[1]
TASK_FILE = BASE_DIR / "logs" / "imp-gi-task-log.json"
INSIGHTS_FILE = BASE_DIR / "logs" / "imp-conversation-insights.json"
PERCEPTION_FILE = BASE_DIR / "logs" / "imp-perception-log.json"


def load_tasks():
    if not TASK_FILE.exists():
        return []
    with open(TASK_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


def add_task(name: str, task: str):
    tasks = load_tasks()
    tasks.append({
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "name": name,
        "task": task,
    })
    save_tasks(tasks)
    print(f"[+] Task recorded for {name}")


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
    pieces = []
    if personality:
        pieces.append(f"personality {personality}")
    if words:
        pieces.append("keywords " + ", ".join(words))
    add_task(name, "Adjust GI using " + " and ".join(pieces))


def list_tasks(name: str | None = None):
    tasks = load_tasks()
    if name:
        tasks = [t for t in tasks if t.get("name") == name]
    for t in tasks:
        print(f"{t['timestamp']} [{t['name']}] {t['task']}")


def clear_tasks(name: str | None = None):
    tasks = load_tasks()
    if name:
        tasks = [t for t in tasks if t.get("name") != name]
    else:
        tasks = []
    save_tasks(tasks)
    target = name if name else "all"
    print(f"[+] Tasks cleared for {target}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 imp-gi-task-manager.py <name> <task> | list [<name>] | clear [<name>] | update <name>")
    elif sys.argv[1] == "list":
        name = sys.argv[2] if len(sys.argv) > 2 else None
        list_tasks(name)
    elif sys.argv[1] == "clear":
        name = sys.argv[2] if len(sys.argv) > 2 else None
        clear_tasks(name)
    elif sys.argv[1] == "update":
        if len(sys.argv) < 3:
            print("Usage: python3 imp-gi-task-manager.py update <name>")
        else:
            update_from_conversation(sys.argv[2])
    else:
        if len(sys.argv) < 3:
            print("Usage: python3 imp-gi-task-manager.py <name> <task>")
        else:
            add_task(sys.argv[1], " ".join(sys.argv[2:]))

