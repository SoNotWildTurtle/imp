import json
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
SCRIPT = BASE_DIR / "gi_modules" / "imp-gi-personality.py"
LOG = BASE_DIR / "logs" / "imp-gi-personality.json"

def test_gi_personality():
    if LOG.exists():
        LOG.unlink()
    subprocess.run([sys.executable, str(SCRIPT), "MoodGI", "5"], check=True)
    subprocess.run([sys.executable, str(SCRIPT), "measure", "MoodGI"], check=True)
    with open(LOG, "r") as f:
        data = json.load(f)
    assert data[-1]["mood"] == 4
    print("✅ GI Personality Module Test Passed!")

if __name__ == "__main__":
    test_gi_personality()
