import sys
import json
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
LOG_FILE = BASE_DIR / "logs" / "imp-module-info.json"
SCRIPT = BASE_DIR / "self-improvement" / "imp-module-explorer.py"

def test_module_explorer():
    if LOG_FILE.exists():
        with open(LOG_FILE, 'r') as f:
            try:
                before = len(json.load(f))
            except json.JSONDecodeError:
                before = 0
    else:
        before = 0
    subprocess.run([sys.executable, str(SCRIPT)], check=True)
    with open(LOG_FILE, 'r') as f:
        after = len(json.load(f))
    assert after == before + 1
    print("✅ Module Explorer Test Passed!")


test_module_explorer()
