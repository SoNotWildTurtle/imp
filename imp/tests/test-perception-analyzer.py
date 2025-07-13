from pathlib import Path
import json
import subprocess

BASE_DIR = Path(__file__).resolve().parents[1]
LOG_FILE = BASE_DIR / "logs" / "imp-perception-log.json"


def test_perception_analyzer():
    if LOG_FILE.exists():
        with open(LOG_FILE, 'r') as f:
            before = len(json.load(f))
    else:
        before = 0
    subprocess.run(["python3", str(BASE_DIR / "interaction" / "imp-perception-analyzer.py")])
    with open(LOG_FILE, 'r') as f:
        after = len(json.load(f))
    assert after == before + 1
    print("✅ Perception Analyzer Test Passed!")


test_perception_analyzer()
