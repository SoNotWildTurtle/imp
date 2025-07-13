from pathlib import Path
import json
import subprocess

BASE_DIR = Path(__file__).resolve().parents[1]
PROFILE_FILE = BASE_DIR / "config" / "imp-general-intelligences.json"


def test_gi_profile_creation():
    if PROFILE_FILE.exists():
        with open(PROFILE_FILE, "r") as f:
            before = len(json.load(f))
    else:
        before = 0
    script = BASE_DIR / "interaction" / "imp-gi-builder.py"
    subprocess.run([
        "python3",
        str(script)
    ], input="TestGI\nA test GI\nsecurity,data\ncaring,smart\nformal\n", text=True, capture_output=True)
    with open(PROFILE_FILE, "r") as f:
        after = len(json.load(f))
    assert after == before + 1
    print("✅ GI Builder Test Passed!")


test_gi_profile_creation()
