import os
import json
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
GOALS_FILE = BASE_DIR / "logs" / "imp-goals.json"

def get_pending_goals():
    if not os.path.exists(GOALS_FILE):
        return []
    with open(GOALS_FILE, "r") as f:
        return [g for g in json.load(f) if g["status"] == "pending"]

def execute_goals():
    pending_goals = get_pending_goals()

    for goal in pending_goals:
        print(f"🚀 Executing goal: {goal['goal']}")
        goal["status"] = "completed"

    with open(GOALS_FILE, "w") as f:
        json.dump(pending_goals, f, indent=4)

if __name__ == "__main__":
    execute_goals()
