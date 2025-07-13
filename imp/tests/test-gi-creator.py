from pathlib import Path
import json
import subprocess

BASE_DIR = Path(__file__).resolve().parents[1]
PROFILE_FILE = BASE_DIR / "config" / "imp-general-intelligences.json"
CONFIG_DIR = BASE_DIR / "config" / "gi"
BUILD_LOG = BASE_DIR / "logs" / "imp-gi-build-log.json"


def ensure_profile():
    script = BASE_DIR / "interaction" / "imp-gi-builder.py"
    subprocess.run([
        "python3",
        str(script)
    ], input="CreatorGI\nCreator test\nnetwork,ai\ncurious,helpful\nchatty\nAI research\n5\nvisual\n", text=True, capture_output=True)


def test_gi_creation():
    ensure_profile()
    before_configs = len(list(CONFIG_DIR.glob("*.json")))
    script = BASE_DIR / "interaction" / "imp-gi-creator.py"
    subprocess.run(["python3", str(script)], input="1\n", text=True, capture_output=True)
    after_configs = len(list(CONFIG_DIR.glob("*.json")))
    with open(BUILD_LOG, "r") as f:
        logs = json.load(f)
    assert after_configs == before_configs + 1
    assert logs and logs[-1]["profile"]
    print("✅ GI Creator Test Passed!")


test_gi_creation()
