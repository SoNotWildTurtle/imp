import sys
from pathlib import Path
import subprocess
import json

BASE_DIR = Path(__file__).resolve().parents[1]
META_LOG = BASE_DIR / "logs" / "imp-metacognition-log.json"


def test_metacognition_log():
    with open(META_LOG, "r") as f:
        before = len(json.load(f))
    subprocess.run([sys.executable, str(BASE_DIR / "self-improvement" / "imp-metacognition.py")])
    with open(META_LOG, "r") as f:
        after = len(json.load(f))
    assert after == before + 1
    print("✅ Metacognition Log Test Passed!")


test_metacognition_log()
