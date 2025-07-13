from pathlib import Path
import json
import subprocess
try:
    import pyotp
except ImportError:
    pyotp = None

BASE_DIR = Path(__file__).resolve().parents[1]
PROFILE_FILE = BASE_DIR / "config" / "imp-general-intelligences.json"
CONFIG_DIR = BASE_DIR / "config" / "gi"
BUILD_LOG = BASE_DIR / "logs" / "imp-gi-build-log.json"
USER_SECRET = "C3MAB55AJKUAF3LTLGJFO33NPKCDHYWL"


def ensure_profile():
    if pyotp is None:
        print("⚠️ pyotp not available. Skipping GI creator test.")
        return False
    script = BASE_DIR / "interaction" / "imp-gi-builder.py"
    totp = pyotp.TOTP(USER_SECRET)
    otp = totp.now()
    input_data = (
        "Alexander Raymond Graham (Minc)\n"
        f"{otp}\n"
        "OpenSesame\n"
        "CreatorGI\nCreator test\nnetwork,ai\ncurious,helpful\nchatty\nAI research\n5\nvisual\n"
    )
    subprocess.run([
        "python3",
        str(script)
    ], input=input_data, text=True, capture_output=True)
    return True


def test_gi_creation():
    if not ensure_profile():
        return
    for f in CONFIG_DIR.glob("*.json"):
        f.unlink()
    before_configs = len(list(CONFIG_DIR.glob("*.json")))
    script = BASE_DIR / "interaction" / "imp-gi-creator.py"
    totp = pyotp.TOTP(USER_SECRET)
    otp = totp.now()
    input_data = (
        "Alexander Raymond Graham (Minc)\n"
        f"{otp}\n"
        "OpenSesame\n"
        "1\n"
    )
    subprocess.run(["python3", str(script)], input=input_data, text=True, capture_output=True)
    after_configs = len(list(CONFIG_DIR.glob("*.json")))
    with open(BUILD_LOG, "r") as f:
        logs = json.load(f)
    assert after_configs >= before_configs + 1
    assert logs and logs[-1]["profile"]
    print("✅ GI Creator Test Passed!")


test_gi_creation()
