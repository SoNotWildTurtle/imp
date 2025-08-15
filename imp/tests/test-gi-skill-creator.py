from pathlib import Path
import json
import subprocess
import sys
try:
    import pyotp
except ImportError:
    pyotp = None

BASE_DIR = Path(__file__).resolve().parents[1]
SKILL_FILE = BASE_DIR / "logs" / "imp-gi-skills.json"
LOCK_FILE = BASE_DIR / "logs" / "imp-lockout-log.json"
USER_SECRET = "C3MAB55AJKUAF3LTLGJFO33NPKCDHYWL"
USER_NAME = "Alexander Raymond Graham (Minc)"


def test_skill_creator():
    if pyotp is None:
        print("\u26a0\ufe0f pyotp not available. Skipping skill creator test.")
        return
    if LOCK_FILE.exists():
        LOCK_FILE.unlink()
    if SKILL_FILE.exists():
        SKILL_FILE.unlink()
    script = BASE_DIR / "interaction" / "imp-gi-skill-creator.py"
    totp = pyotp.TOTP(USER_SECRET)
    otp = totp.now()
    subprocess.run([
        sys.executable, str(script)
    ], input=f"{USER_NAME}\n{otp}\nOpenSesame\nMyGI\nnetwork scanning\n", text=True)
    assert SKILL_FILE.exists()
    with open(SKILL_FILE, "r") as f:
        data = json.load(f)
    assert any(d["name"] == "MyGI" and "network scanning" in d["skill"] for d in data)
    print("\u2705 GI Skill Creator Test Passed!")


if __name__ == "__main__":
    test_skill_creator()
