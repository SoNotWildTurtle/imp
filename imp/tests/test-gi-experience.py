import sys
from pathlib import Path
import json
import subprocess

BASE_DIR = Path(__file__).resolve().parents[1]
PROFILE_FILE = BASE_DIR / "config" / "imp-general-intelligences.json"
EXP_FILE = BASE_DIR / "logs" / "imp-gi-experience.json"
INSIGHTS_FILE = BASE_DIR / "logs" / "imp-conversation-insights.json"


def test_experience_update():
    profiles = [
        {"name": "A", "skills": ["analysis", "planning"], "personality": ["kind"]},
        {"name": "B", "skills": ["planning", "security"], "personality": ["kind", "smart"]},
    ]
    with open(PROFILE_FILE, "w") as f:
        json.dump(profiles, f)
    with open(INSIGHTS_FILE, "w") as f:
        json.dump([{"timestamp": "now", "top_words": [["analysis", 3], ["code", 2]]}], f)
    script = BASE_DIR / "self-improvement" / "imp-gi-experience.py"
    subprocess.run([sys.executable, str(script)], check=True)
    with open(EXP_FILE, "r") as f:
        data = json.load(f)
    assert data["stats"]["count"] == 2
    assert data["stats"]["skills"]["planning"] == 2
    assert data["stats"]["keywords"]["analysis"] == 3
    print("✅ GI Experience Trainer Test Passed!")


test_experience_update()
