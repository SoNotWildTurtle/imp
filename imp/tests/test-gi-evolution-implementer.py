from pathlib import Path
import json
import subprocess
try:
    import pyotp
except ImportError:
    pyotp = None

BASE_DIR = Path(__file__).resolve().parents[1]
PLAN_FILE = BASE_DIR / "logs" / "imp-gi-evolution-plans.json"
IMPL_LOG = BASE_DIR / "logs" / "imp-gi-implementation-log.json"
LOCK_FILE = BASE_DIR / "logs" / "imp-lockout-log.json"
USER_SECRET = "C3MAB55AJKUAF3LTLGJFO33NPKCDHYWL"
USER_NAME = "Alexander Raymond Graham (Minc)"


def test_implementer():
    PLAN_FILE.write_text(json.dumps({"plans": {"impl-alias": ["add module"]}}, indent=4))
    if IMPL_LOG.exists():
        IMPL_LOG.unlink()
    if pyotp is None:
        print("⚠️ pyotp not available. Skipping evolution implementer test.")
        return
    if LOCK_FILE.exists():
        LOCK_FILE.unlink()
    script = BASE_DIR / "interaction" / "imp-gi-evolution-implementer.py"
    totp = pyotp.TOTP(USER_SECRET)
    otp = totp.now()
    subprocess.run([
        "python3", str(script)
    ], input=f"{USER_NAME}\n{otp}\nOpenSesame\ny\ny\n", text=True)
    assert IMPL_LOG.exists()
    with open(IMPL_LOG, "r") as f:
        data = json.load(f)
    assert any(e["alias"] == "impl-alias" for e in data)
    print("✅ GI Evolution Implementer Test Passed!")


if __name__ == "__main__":
    test_implementer()
