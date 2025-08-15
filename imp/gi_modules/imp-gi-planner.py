from pathlib import Path
import json
import time
import sys

BASE_DIR = Path(__file__).resolve().parents[1]
PLAN_FILE = BASE_DIR / "logs" / "imp-gi-plans.json"
INSIGHTS_FILE = BASE_DIR / "logs" / "imp-conversation-insights.json"


def load_plans():
    if not PLAN_FILE.exists():
        return []
    with open(PLAN_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_plans(plans):
    with open(PLAN_FILE, "w") as f:
        json.dump(plans, f, indent=4)


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


def add_plan(name: str, plan: str):
    plans = load_plans()
    plans.append({
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "name": name,
        "plan": plan,
    })
    save_plans(plans)
    print(f"[+] Plan recorded for {name}")


def update_from_conversation(name: str):
    words = latest_keywords()
    if not words:
        print("[!] No conversation insights available")
        return
    add_plan(name, "Plan around: " + ", ".join(words))


def list_plans(name: str | None = None):
    plans = load_plans()
    if name:
        plans = [p for p in plans if p.get("name") == name]
    for p in plans:
        print(f"{p['timestamp']} [{p['name']}] {p['plan']}")


def clear_plans(name: str | None = None):
    plans = load_plans()
    if name:
        plans = [p for p in plans if p.get("name") != name]
    else:
        plans = []
    save_plans(plans)
    target = name if name else "all"
    print(f"[+] Plans cleared for {target}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 imp-gi-planner.py <name> <plan> | list [<name>] | clear [<name>] | update <name>")
    elif sys.argv[1] == "list":
        name = sys.argv[2] if len(sys.argv) > 2 else None
        list_plans(name)
    elif sys.argv[1] == "clear":
        name = sys.argv[2] if len(sys.argv) > 2 else None
        clear_plans(name)
    elif sys.argv[1] == "update":
        if len(sys.argv) < 3:
            print("Usage: python3 imp-gi-planner.py update <name>")
        else:
            update_from_conversation(sys.argv[2])
    else:
        if len(sys.argv) < 3:
            print("Usage: python3 imp-gi-planner.py <name> <plan>")
        else:
            add_plan(sys.argv[1], " ".join(sys.argv[2:]))
