import os
import json
from pathlib import Path
from typing import Optional

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

ROOT = Path(__file__).resolve().parents[1]
GOALS_FILE = ROOT / "logs" / "imp-goals.json"

def get_goals() -> list:
    """Load all goals from disk."""
    if not os.path.exists(GOALS_FILE):
        return []
    with open(GOALS_FILE, "r") as f:
        return json.load(f)

def get_pending_goals(term: Optional[str] = None):
    """Return pending goals optionally filtered by term."""
    goals = get_goals()
    pending = [g for g in goals if g.get("status") == "pending"]
    if term:
        pending = [g for g in pending if g.get("term") == term]
    pending.sort(key=lambda g: PRIORITY_ORDER.get(g.get("priority", "medium"), 1))
    return pending

def execute_goals(term: Optional[str] = None):
    """Execute pending goals sorted by priority."""
    goals = get_goals()
    pending = [g for g in goals if g.get("status") == "pending"]
    if term:
        pending = [g for g in pending if g.get("term") == term]
    pending.sort(key=lambda g: PRIORITY_ORDER.get(g.get("priority", "medium"), 1))

    for goal in pending:
        print(f"🚀 Executing goal: {goal['goal']}")
        goal["status"] = "completed"

    with open(GOALS_FILE, "w") as f:
        json.dump(goals, f, indent=4)

if __name__ == "__main__":
    choice = input("Execute short-term or long-term goals? [s/l/all]: ").strip().lower()
    if choice.startswith("s"):
        execute_goals("short-term")
    elif choice.startswith("l"):
        execute_goals("long-term")
    else:
        execute_goals()
