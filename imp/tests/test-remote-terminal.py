import sys
import subprocess
import json
from pathlib import Path
try:
    import pyotp
except Exception:
    pyotp = None

BASE_DIR = Path(__file__).resolve().parents[1]
LOG_FILE = BASE_DIR / "logs" / "imp-remote-terminal.json"
USER_SECRET = "C3MAB55AJKUAF3LTLGJFO33NPKCDHYWL"
LOCK_FILE = BASE_DIR / "logs" / "imp-lockout-log.json"


def test_remote_terminal():
    if pyotp is None:
        print("⚠️ pyotp not available. Skipping remote terminal test.")
        return
    if LOCK_FILE.exists():
        LOCK_FILE.unlink()
    if LOG_FILE.exists():
        with open(LOG_FILE, "r") as f:
            before = len(json.load(f))
    else:
        before = 0
    script = BASE_DIR / "interaction" / "imp-remote-terminal.py"
    totp = pyotp.TOTP(USER_SECRET)
    otp = totp.now()
    input_data = (
        "Alexander Raymond Graham (Minc)\n"  # username
        f"{otp}\n"
        "OpenSesame\n"
    )
    subprocess.run([
        sys.executable,
        str(script),
        "--host",
        "example.com",
        "--user",
        "alex",
        "--dry-run",
    ], input=input_data, text=True, capture_output=True)
    with open(LOG_FILE, "r") as f:
        after = len(json.load(f))
    assert after == before + 1
    print("✅ Remote Terminal Test Passed!")


test_remote_terminal()
