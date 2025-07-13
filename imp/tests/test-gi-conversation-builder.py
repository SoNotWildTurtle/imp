from pathlib import Path
import json
import subprocess
try:
    import pyotp
except ImportError:
    pyotp = None

BASE_DIR = Path(__file__).resolve().parents[1]
PROFILE_FILE = BASE_DIR / "config" / "imp-general-intelligences.json"
LOCK_FILE = BASE_DIR / "logs" / "imp-lockout-log.json"
USER_SECRET = "C3MAB55AJKUAF3LTLGJFO33NPKCDHYWL"


def test_conversation_profile_creation():
    if pyotp is None:
        print("⚠️ pyotp not available. Skipping conversation builder test.")
        return
    if LOCK_FILE.exists():
        LOCK_FILE.unlink()
    if PROFILE_FILE.exists():
        with open(PROFILE_FILE, 'r') as f:
            before = len(json.load(f))
    else:
        before = 0
    script = BASE_DIR / "interaction" / "imp-gi-conversation-builder.py"
    totp = pyotp.TOTP(USER_SECRET)
    otp = totp.now()
    input_data = (
        "Alexander Raymond Graham (Minc)\n"
        f"{otp}\n"
        "OpenSesame\n"
        "ConvoGI\nLearning AI\nanalysis,security\nhelpful,friendly\nformal\nAI dev\n8\nvisual\ncloud\n9\n"
    )
    subprocess.run(["python3", str(script)], input=input_data, text=True, capture_output=True)
    with open(PROFILE_FILE, 'r') as f:
        profiles = json.load(f)
        after = len(profiles)
    assert after == before + 1
    last = profiles[-1]
    assert last.get('name') == 'ConvoGI'
    GOALS_FILE = BASE_DIR / 'logs' / 'imp-gi-goals.json'
    with open(GOALS_FILE, 'r') as g:
        goals = json.load(g)
    assert any(e['status'] == 'complete' for e in goals if 'conversation-driven' in e['goal'])
    print("✅ GI Conversation Builder Test Passed!")


test_conversation_profile_creation()
