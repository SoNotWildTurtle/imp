import sys
from pathlib import Path
import json
import subprocess
try:
    import pyotp
except ImportError:
    pyotp = None

BASE_DIR = Path(__file__).resolve().parents[1]
PROFILE_FILE = BASE_DIR / "config" / "imp-general-intelligences.json"
LOCK_FILE = BASE_DIR / "logs" / "imp-lockout-log.json"
USER_SECRET = "C3MAB55AJKUAF3LTLGJFO33NPKCDHYWL"


def test_gi_profile_creation():
    if pyotp is None:
        print("⚠️ pyotp not available. Skipping GI builder test.")
        return
    if LOCK_FILE.exists():
        LOCK_FILE.unlink()
    if PROFILE_FILE.exists():
        with open(PROFILE_FILE, "r") as f:
            before = len(json.load(f))
    else:
        before = 0
    script = BASE_DIR / "interaction" / "imp-gi-builder.py"
    totp = pyotp.TOTP(USER_SECRET)
    otp = totp.now()
    input_data = (
        "Alexander Raymond Graham (Minc)\n"  # user name
        f"{otp}\n"  # otp code
        "OpenSesame\n"  # passphrase
        "TestGI\nA test GI\nsecurity,data\ncaring,smart\nformal\ncybersecurity\n7\ncollaborative\ncloud\n8\nFollow best practices\n5001\n\n"
    )
    subprocess.run([
        sys.executable,
        str(script)
    ], input=input_data, text=True, capture_output=True)
    with open(PROFILE_FILE, "r") as f:
        profiles = json.load(f)
        after = len(profiles)
    assert after == before + 1
    last = profiles[-1]
    assert "environment" in last and "security_level" in last
    assert "safety_guidelines" in last and "suggested_personality" in last
    assert last.get("dashboard_port") == "5001"
    assert isinstance(last.get("modules"), list) and len(last["modules"]) >= 5
    GOALS_FILE = BASE_DIR / "logs" / "imp-gi-goals.json"
    with open(GOALS_FILE, "r") as g:
        goals = json.load(g)
    assert any(e["status"] == "complete" for e in goals if "environment" in e["goal"])
    print("✅ GI Builder Test Passed!")


test_gi_profile_creation()
