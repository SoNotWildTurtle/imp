import sys
from pathlib import Path
import json
import subprocess
try:
    import pyotp
except ImportError:
    pyotp = None

BASE_DIR = Path(__file__).resolve().parents[1]
ALIAS_FILE = BASE_DIR / "config" / "imp-gi-aliases.json"
COMM_LOG = BASE_DIR / "logs" / "imp-gi-comm-log.json"
LOCK_FILE = BASE_DIR / "logs" / "imp-lockout-log.json"
USER_SECRET = "C3MAB55AJKUAF3LTLGJFO33NPKCDHYWL"
USER_NAME = "Alexander Raymond Graham (Minc)"


def test_checkin():
    with open(ALIAS_FILE, "w") as f:
        json.dump({"test-alias": "TestGI"}, f)
    if COMM_LOG.exists():
        COMM_LOG.unlink()
    script = BASE_DIR / "interaction" / "imp-gi-communicator.py"
    subprocess.run([
        sys.executable, str(script), "checkin", "test-alias", "hello"
    ])
    with open(COMM_LOG, "r") as f:
        logs = json.load(f)
    assert logs and logs[-1]["alias"] == "test-alias"
    print("✅ GI Communicator Check-in Test Passed!")


def test_evolution_request():
    if pyotp is None:
        print("⚠️ pyotp not available. Skipping evolution request test.")
        return
    if LOCK_FILE.exists():
        LOCK_FILE.unlink()
    with open(ALIAS_FILE, "w") as f:
        json.dump({"evo-alias": "EvoGI"}, f)
    script = BASE_DIR / "interaction" / "imp-gi-communicator.py"
    totp = pyotp.TOTP(USER_SECRET)
    otp = totp.now()
    subprocess.run([
        sys.executable, str(script), "request-evolution", "evo-alias", "upgrade"
    ], input=f"{USER_NAME}\n{otp}\nOpenSesame\n", text=True)
    with open(COMM_LOG, "r") as f:
        logs = json.load(f)
    assert any(e.get("evolution_request") == "upgrade" for e in logs)
    print("✅ GI Communicator Evolution Request Test Passed!")


test_checkin()

test_evolution_request()
