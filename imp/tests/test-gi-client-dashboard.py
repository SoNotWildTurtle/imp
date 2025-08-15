import sys
from pathlib import Path
import json
import subprocess
try:
    import pyotp
except ImportError:
    pyotp = None

BASE_DIR = Path(__file__).resolve().parents[1]
REQUEST_FILE = BASE_DIR / "logs" / "imp-gi-requests.json"
COMM_LOG = BASE_DIR / "logs" / "imp-gi-comm-log.json"
LOCK_FILE = BASE_DIR / "logs" / "imp-lockout-log.json"
USER_SECRET = "C3MAB55AJKUAF3LTLGJFO33NPKCDHYWL"
USER_NAME = "Alexander Raymond Graham (Minc)"

def test_client_dashboard():
    REQUEST_FILE.write_text(json.dumps([
        {"timestamp": "2024-01-01 00:00:00", "name": "dash-alias", "request": "new feature"}
    ], indent=4))
    if COMM_LOG.exists():
        COMM_LOG.unlink()
    if pyotp is None:
        print("⚠️ pyotp not available. Skipping client dashboard test.")
        return
    if LOCK_FILE.exists():
        LOCK_FILE.unlink()
    script = BASE_DIR / "interaction" / "imp-gi-client-dashboard.py"
    totp = pyotp.TOTP(USER_SECRET)
    otp = totp.now()
    result = subprocess.run([
        sys.executable, str(script)
    ], input=f"{USER_NAME}\n{otp}\nOpenSesame\ny\n", text=True, capture_output=True)
    assert "GI Client Dashboard" in result.stdout
    assert "All requests processed." in result.stdout
    assert COMM_LOG.exists()
    with open(COMM_LOG, "r") as f:
        data = json.load(f)
    assert any(e.get("evolution_request") == "new feature" for e in data)
    with open(REQUEST_FILE, "r") as f:
        remaining = json.load(f)
    assert remaining == []
    print("✅ GI Client Dashboard Test Passed!")

if __name__ == "__main__":
    test_client_dashboard()
