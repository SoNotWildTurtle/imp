import sys
from pathlib import Path
import json
import subprocess
try:
    import pyotp
except ImportError:
    pyotp = None

BASE_DIR = Path(__file__).resolve().parents[1]
SNAP_FILE = BASE_DIR / "logs" / "imp-gi-snapshots.json"
CONFIG_DIR = BASE_DIR / "config" / "gi"
LOCK_FILE = BASE_DIR / "logs" / "imp-lockout-log.json"
USER_SECRET = "C3MAB55AJKUAF3LTLGJFO33NPKCDHYWL"
USER_NAME = "Alexander Raymond Graham (Minc)"


def test_gi_snapshot():
    if pyotp is None:
        print("⚠️ pyotp not available. Skipping snapshot test.")
        return
    if LOCK_FILE.exists():
        LOCK_FILE.unlink()
    CONFIG_DIR.mkdir(exist_ok=True)
    config_path = CONFIG_DIR / "SnapGI.json"
    config_path.write_text(json.dumps({"name": "SnapGI"}, indent=4))
    if SNAP_FILE.exists():
        SNAP_FILE.unlink()
    script = BASE_DIR / "interaction" / "imp-gi-snapshot.py"
    totp = pyotp.TOTP(USER_SECRET)
    otp = totp.now()
    subprocess.run([
        sys.executable, str(script), "SnapGI"
    ], input=f"{USER_NAME}\n{otp}\nOpenSesame\n", text=True)
    with open(SNAP_FILE, "r") as f:
        data = json.load(f)
    assert any(s["name"] == "SnapGI" for s in data)
    print("✅ GI Snapshot Test Passed!")


if __name__ == "__main__":
    test_gi_snapshot()
