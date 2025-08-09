import sys
from pathlib import Path
import subprocess
try:
    import pyotp
except ImportError:
    pyotp = None

BASE_DIR = Path(__file__).resolve().parents[1]
SCRIPT = BASE_DIR / "interaction" / "imp-terminal.py"
USER_SECRET = "C3MAB55AJKUAF3LTLGJFO33NPKCDHYWL"
LOCK_FILE = BASE_DIR / "logs" / "imp-lockout-log.json"


def test_terminal_interface():
    if pyotp is None:
        print("⚠️ pyotp not available. Skipping terminal interface test.")
        return
    if LOCK_FILE.exists():
        LOCK_FILE.unlink()
    totp = pyotp.TOTP(USER_SECRET)
    otp = totp.now()
    result = subprocess.run([
        sys.executable, str(SCRIPT)
    ], input=f"Alexander Raymond Graham (Minc)\n{otp}\nOpenSesame\n10\n", text=True, capture_output=True)
    assert "Cimp Terminal Interface" in result.stdout
    assert "Type 10 or 'q' to quit." in result.stdout
    print("✅ Terminal Interface Test Passed!")


test_terminal_interface()
