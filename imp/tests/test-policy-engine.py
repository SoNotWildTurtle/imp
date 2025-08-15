import json
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
POLICY_FILE = BASE_DIR / "config" / "policy-test.yaml"
LOG_FILE = BASE_DIR / "logs" / "imp-policy-changes.json"
SCRIPT = BASE_DIR / "security" / "imp-policy-engine.py"


def test_policy_engine():
    # reset log
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)
    # write initial policy
    POLICY_FILE.write_text("capabilities:\n  chat_local: request_only\n", encoding="utf-8")
    # grant capability
    subprocess.run([sys.executable, str(SCRIPT), "grant", "chat_local", "--policy", str(POLICY_FILE)], check=True)
    data = POLICY_FILE.read_text(encoding="utf-8")
    assert "granted" in data
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        entries = json.load(f)
    assert any(e.get("capability") == "chat_local" and e.get("new") == "granted" for e in entries)
    print("✅ Policy Engine Test Passed!")


test_policy_engine()
