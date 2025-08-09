import sys
from pathlib import Path
import json
import subprocess

BASE_DIR = Path(__file__).resolve().parents[1]
LOG_FILE = BASE_DIR / "logs" / "imp-gi-skills.json"


def test_gi_skill_tracker():
    script = BASE_DIR / "gi_modules" / "imp-gi-skill-tracker.py"
    subprocess.run([sys.executable, str(script), "clear", "TestGI"], check=True)
    with open(LOG_FILE, "r") as f:
        try:
            before = len([e for e in json.load(f) if e.get("name") == "TestGI"])
        except json.JSONDecodeError:
            before = 0
    assert before == 0
    # update from conversation insights
    subprocess.run([sys.executable, str(script), "update", "TestGI"], check=True)
    with open(LOG_FILE, "r") as f:
        after = len([e for e in json.load(f) if e.get("name") == "TestGI"])
    assert after >= 0  # update might not add if no insights
    subprocess.run([sys.executable, str(script), "TestGI", "hacking"], check=True)
    with open(LOG_FILE, "r") as f:
        new_count = len([e for e in json.load(f) if e.get("name") == "TestGI"])
    assert new_count >= after + 1
    subprocess.run([sys.executable, str(script), "clear", "TestGI"], check=True)
    with open(LOG_FILE, "r") as f:
        final = len([e for e in json.load(f) if e.get("name") == "TestGI"])
    assert final == 0
    print("✅ GI Skill Tracker Test Passed!")


test_gi_skill_tracker()
