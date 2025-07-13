from pathlib import Path
import json
import subprocess
try:
    import pyotp
except ImportError:
    pyotp = None

BASE_DIR = Path(__file__).resolve().parents[1]
PROFILE_FILE = BASE_DIR / "config" / "imp-general-intelligences.json"
USER_SECRET = "C3MAB55AJKUAF3LTLGJFO33NPKCDHYWL"
LOCK_FILE = BASE_DIR / "logs" / "imp-lockout-log.json"

def test_profile_listing():
    if pyotp is None:
        print("⚠️ pyotp not available. Skipping profile manager test.")
        return
    if LOCK_FILE.exists():
        LOCK_FILE.unlink()
    profiles = [
        {"name": "TestPM", "description": "Test"}
    ]
    with open(PROFILE_FILE, "w") as f:
        json.dump(profiles, f)
    script = BASE_DIR / "interaction" / "imp-gi-profile-manager.py"
    totp = pyotp.TOTP(USER_SECRET)
    otp = totp.now()
    result = subprocess.run([
        "python3", str(script), "list"
    ], input=f"Alexander Raymond Graham (Minc)\n{otp}\nOpenSesame\n", text=True, capture_output=True)
    assert "TestPM" in result.stdout
    print("✅ GI Profile Manager Test Passed!")

test_profile_listing()
