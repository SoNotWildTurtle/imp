from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parent.parent
LOG = ROOT / "logs" / "imp-sandbox-log.json"
SCRIPT = ROOT / "self-improvement" / "imp-debug-sandbox.py"


def test_debug_sandbox():
    print("Testing debug sandbox...")
    if LOG.exists():
        LOG.unlink()
    subprocess.run(["python3", str(SCRIPT)], check=True)
    data = json.loads(LOG.read_text())
    assert data["after_neurons"] >= data["before_neurons"]
    print("Debug sandbox test passed!")
