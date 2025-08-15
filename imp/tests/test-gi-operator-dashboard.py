from pathlib import Path
import json
import subprocess
import sys
try:
    import pyotp
except ImportError:
    pyotp = None

BASE_DIR = Path(__file__).resolve().parents[1]
REQUEST_FILE = BASE_DIR / "logs" / "imp-gi-requests.json"
DEC_LOG = BASE_DIR / "logs" / "imp-gi-upgrade-decisions.json"
SNAP_FILE = BASE_DIR / "logs" / "imp-gi-snapshots.json"
IMPL_LOG = BASE_DIR / "logs" / "imp-gi-implementation-log.json"
SKILL_FILE = BASE_DIR / "logs" / "imp-gi-skills.json"
ANALYSIS_LOG = BASE_DIR / "logs" / "imp-gi-evolution-analysis.json"
CONFIG_DIR = BASE_DIR / "config" / "gi"
LOCK_FILE = BASE_DIR / "logs" / "imp-lockout-log.json"
USER_SECRET = "C3MAB55AJKUAF3LTLGJFO33NPKCDHYWL"
USER_NAME = "Alexander Raymond Graham (Minc)"


def test_operator_dashboard():
    REQUEST_FILE.write_text(json.dumps([{"name": "dashgi", "request": "fix bug"}], indent=4))
    CONFIG_DIR.mkdir(exist_ok=True)
    (CONFIG_DIR / "dashgi.json").write_text(json.dumps({"name": "dashgi"}, indent=4))
    for f in [DEC_LOG, SNAP_FILE, IMPL_LOG, SKILL_FILE, ANALYSIS_LOG]:
        if f.exists():
            f.unlink()
    if pyotp is None:
        print("⚠️ pyotp not available. Skipping operator dashboard test.")
        return
    if LOCK_FILE.exists():
        LOCK_FILE.unlink()
    script = BASE_DIR / "interaction" / "imp-gi-operator-dashboard.py"
    totp = pyotp.TOTP(USER_SECRET)
    otp = totp.now()
    subprocess.run([
        sys.executable, str(script)
    ], input=f"{USER_NAME}\n{otp}\nOpenSesame\ny\ny\ny\ndashgi\n3\n", text=True)
    assert DEC_LOG.exists()
    with open(DEC_LOG, "r") as f:
        data = json.load(f)
    assert any(d["alias"] == "dashgi" for d in data)
    with open(SNAP_FILE, "r") as f:
        snap = json.load(f)
    assert any(s["name"] == "dashgi" for s in snap)
    with open(IMPL_LOG, "r") as f:
        impl = json.load(f)
    assert any(i["name"] == "dashgi" for i in impl)
    with open(SKILL_FILE, "r") as f:
        skills = json.load(f)
    assert any(s["name"] == "dashgi" and "fix bug" in s["skill"] for s in skills)
    with open(ANALYSIS_LOG, "r") as f:
        analysis = json.load(f)
    assert any(a["name"] == "dashgi" for a in analysis)
    MOOD_LOG = BASE_DIR / "logs" / "imp-gi-personality.json"
    with open(MOOD_LOG, "r") as f:
        moods = json.load(f)
    assert any(m["name"] == "dashgi" and m["mood"] == 3 for m in moods)
    print("✅ GI Operator Dashboard Test Passed!")


if __name__ == "__main__":
    test_operator_dashboard()
