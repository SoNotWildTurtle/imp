import sys
from pathlib import Path
import json
import subprocess
try:
    import pyotp
except ImportError:
    pyotp = None

BASE_DIR = Path(__file__).resolve().parents[1]
PLAN_FILE = BASE_DIR / "logs" / "imp-gi-evolution-plans.json"
COMM_LOG = BASE_DIR / "logs" / "imp-gi-comm-log.json"
ALIAS_FILE = BASE_DIR / "config" / "imp-gi-aliases.json"
LOCK_FILE = BASE_DIR / "logs" / "imp-lockout-log.json"
USER_SECRET = "C3MAB55AJKUAF3LTLGJFO33NPKCDHYWL"
USER_NAME = "Alexander Raymond Graham (Minc)"


def test_planner():
    with open(ALIAS_FILE, "w") as f:
        json.dump({"plan-alias": "PlanGI"}, f)
    COMM_LOG.write_text(json.dumps([
        {"timestamp": "t", "alias": "plan-alias", "evolution_request": "update modules"}
    ], indent=4))
    if PLAN_FILE.exists():
        PLAN_FILE.unlink()
    if pyotp is None:
        print("⚠️ pyotp not available. Skipping evolution planner test.")
        return
    if LOCK_FILE.exists():
        LOCK_FILE.unlink()
    script = BASE_DIR / "interaction" / "imp-gi-evolution-planner.py"
    totp = pyotp.TOTP(USER_SECRET)
    otp = totp.now()
    subprocess.run([sys.executable, str(script)], input=f"{USER_NAME}\n{otp}\nOpenSesame\n", text=True)
    assert PLAN_FILE.exists()
    with open(PLAN_FILE, "r") as f:
        data = json.load(f)
    assert "plan-alias" in data.get("plans", {})
    print("✅ GI Evolution Planner Test Passed!")


test_planner()
