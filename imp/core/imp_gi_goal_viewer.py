from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parents[1]
GOALS_FILE = BASE_DIR / "logs" / "imp-gi-goals.json"


def show_goals() -> None:
    if not GOALS_FILE.exists():
        print("No goal log available.")
        return
    try:
        with open(GOALS_FILE, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("Failed to read goal log.")
        return
    for entry in data:
        goal = entry.get("goal", "")
        status = entry.get("status", "pending")
        print(f"- {goal}: {status}")


if __name__ == "__main__":
    show_goals()
