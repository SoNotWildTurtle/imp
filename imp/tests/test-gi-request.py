import sys
from pathlib import Path
import json
import subprocess

BASE_DIR = Path(__file__).resolve().parents[1]
LOG_FILE = BASE_DIR / "logs" / "imp-gi-requests.json"


def test_gi_request_module():
    script = BASE_DIR / "gi_modules" / "imp-gi-request.py"
    subprocess.run([sys.executable, str(script), "clear", "TestGI"], check=True)
    with open(LOG_FILE, "r") as f:
        try:
            before = len([e for e in json.load(f) if e.get("name") == "TestGI"])
        except json.JSONDecodeError:
            before = 0
    assert before == 0
    subprocess.run([sys.executable, str(script), "TestGI", "add", "feature"], check=True)
    with open(LOG_FILE, "r") as f:
        after = len([e for e in json.load(f) if e.get("name") == "TestGI"])
    assert after == before + 1
    subprocess.run([sys.executable, str(script), "clear", "TestGI"], check=True)
    with open(LOG_FILE, "r") as f:
        final = len([e for e in json.load(f) if e.get("name") == "TestGI"])
    assert final == 0
    print("✅ GI Request Module Test Passed!")


test_gi_request_module()
