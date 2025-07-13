from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parents[1]
GOALS_FILE = BASE_DIR / "logs" / "imp-gi-goals.json"


def update_goal_status(goal_substring: str, status: str = "complete") -> None:
    if not GOALS_FILE.exists():
        return
    try:
        with open(GOALS_FILE, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return
    changed = False
    for entry in data:
        if goal_substring.lower() in entry.get("goal", "").lower():
            if entry.get("status") != status:
                entry["status"] = status
                changed = True
    if changed:
        with open(GOALS_FILE, "w") as f:
            json.dump(data, f, indent=4)

