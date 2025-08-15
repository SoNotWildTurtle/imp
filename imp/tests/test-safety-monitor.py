import json
import json
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
CONSENT_FILE = BASE_DIR / "config" / "imp-consent.json"
LOG_FILE = BASE_DIR / "logs" / "imp-safety-log.json"


def test_safety_monitor():
    CONSENT_FILE.write_text(json.dumps({"safety_monitor": True}, indent=4))
    if LOG_FILE.exists():
        before = len(json.load(open(LOG_FILE)))
    else:
        before = 0
    subprocess.run([sys.executable, str(BASE_DIR / "security" / "imp-safety-monitor.py"), "--event", "test"], check=True)
    after = len(json.load(open(LOG_FILE)))
    assert after == before + 1
    logs = json.load(open(LOG_FILE))
    with open(LOG_FILE, "w") as f:
        json.dump(logs[:before], f, indent=4)
    CONSENT_FILE.write_text(json.dumps({"safety_monitor": False}, indent=4))
    print("✅ Safety Monitor Test Passed!")


test_safety_monitor()
