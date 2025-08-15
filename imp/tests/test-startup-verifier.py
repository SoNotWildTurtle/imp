"""Test the startup verification utility."""
import sys
import subprocess
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
LOG_FILE = BASE_DIR / "logs" / "imp-startup-verification.json"
SCRIPT = BASE_DIR / "startup" / "imp_startup_verifier.py"


def test_startup_verifier_runs():
    LOG_FILE.write_text("[]", encoding="utf-8")
    subprocess.run([sys.executable, str(SCRIPT)], check=True)
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        logs = json.load(f)
    assert any(entry["step"] == "terminal interface loads" and entry["status"] == "ok" for entry in logs)


test_startup_verifier_runs()
print("✅ Startup Verifier Test Passed!")
