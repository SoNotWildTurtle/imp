from pathlib import Path
import json
import subprocess
import sys
try:
    import pyotp
except ImportError:
    pyotp = None

BASE_DIR = Path(__file__).resolve().parents[1]
GI_FILE = BASE_DIR / "config" / "imp-general-intelligences.json"
REQUEST_FILE = BASE_DIR / "logs" / "imp-gi-requests.json"
SNAP_FILE = BASE_DIR / "logs" / "imp-gi-snapshots.json"
LOCK_FILE = BASE_DIR / "logs" / "imp-lockout-log.json"
USER_SECRET = "C3MAB55AJKUAF3LTLGJFO33NPKCDHYWL"
USER_NAME = "Alexander Raymond Graham (Minc)"

def test_management_dashboard():
    GI_FILE.write_text(json.dumps([{"name": "dashgi", "modules": []}], indent=4))
    REQUEST_FILE.write_text(json.dumps([{"name": "dashgi", "request": "upgrade"}], indent=4))
    SNAP_FILE.write_text(json.dumps([{"name": "dashgi", "snapshot": "state"}], indent=4))
    if pyotp is None:
        print("\u26a0\ufe0f pyotp not available. Skipping GI management dashboard test.")
        return
    if LOCK_FILE.exists():
        LOCK_FILE.unlink()
    script = BASE_DIR / "interaction" / "imp-gi-management-dashboard.py"
    totp = pyotp.TOTP(USER_SECRET)
    otp = totp.now()
    result = subprocess.run([
        sys.executable, str(script)
    ], input=f"{USER_NAME}\n{otp}\nOpenSesame\n1\n2\n3\nq\n", text=True, capture_output=True)
    assert "dashgi" in result.stdout

if __name__ == "__main__":
    test_management_dashboard()
