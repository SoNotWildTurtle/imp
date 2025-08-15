import sys
from pathlib import Path
import subprocess
try:
    import pyotp
except ImportError:
    pyotp = None

BASE_DIR = Path(__file__).resolve().parents[1]
SCRIPT = BASE_DIR / "interaction" / "imp-gi-builder-terminal.py"
USER_SECRET = "C3MAB55AJKUAF3LTLGJFO33NPKCDHYWL"
LOCK_FILE = BASE_DIR / "logs" / "imp-lockout-log.json"


def test_gi_builder_terminal():
    if pyotp is None:
        print("⚠️ pyotp not available. Skipping GI builder terminal test.")
        return
    if LOCK_FILE.exists():
        LOCK_FILE.unlink()
    totp = pyotp.TOTP(USER_SECRET)
    otp = totp.now()
    input_data = f"Alexander Raymond Graham (Minc)\n{otp}\nOpenSesame\n5\n"
    result = subprocess.run([
        sys.executable,
        str(SCRIPT)
    ], input=input_data, text=True, capture_output=True)
    assert "GI Creation Terminal" in result.stdout
    print("✅ GI Builder Terminal Test Passed!")


test_gi_builder_terminal()
