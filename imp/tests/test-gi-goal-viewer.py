from pathlib import Path
import subprocess
import json

BASE_DIR = Path(__file__).resolve().parents[1]
GOALS_FILE = BASE_DIR / "logs" / "imp-gi-goals.json"
VIEWER = BASE_DIR / "core" / "imp_gi_goal_viewer.py"


def test_goal_viewer():
    if not GOALS_FILE.exists():
        print("⚠️ Goal log missing. Skipping goal viewer test.")
        return
    with open(GOALS_FILE, "r") as f:
        try:
            goals = json.load(f)
        except json.JSONDecodeError:
            goals = []
    if not goals:
        print("⚠️ No goals recorded. Skipping goal viewer test.")
        return
    result = subprocess.run(["python3", str(VIEWER)], capture_output=True, text=True)
    output = result.stdout
    assert any(g["goal"] in output for g in goals)
    print("✅ GI Goal Viewer Test Passed!")


test_goal_viewer()
