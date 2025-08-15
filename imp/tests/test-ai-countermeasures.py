import json
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]


def test_countermeasure_logging():
    # write a sample threat
    threat_path = BASE_DIR / "logs" / "imp-threat-log.json"
    with open(threat_path, "w") as f:
        json.dump({"Hostile AI": "Unexpected behavior"}, f, indent=4)
    # clear countermeasure log
    cm_path = BASE_DIR / "logs" / "imp-ai-countermeasures.json"
    with open(cm_path, "w") as f:
        json.dump([], f)
    script = BASE_DIR / "security" / "imp-ai-countermeasures.py"
    subprocess.run([sys.executable, str(script)], check=True)
    with open(cm_path) as f:
        data = json.load(f)
    assert any(entry["threat"] == "Hostile AI" for entry in data)
    print("✅ Countermeasure logging test passed")


test_countermeasure_logging()
