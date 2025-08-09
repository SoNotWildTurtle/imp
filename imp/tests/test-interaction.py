import sys
from pathlib import Path
import subprocess
import json

BASE_DIR = Path(__file__).resolve().parents[1]


def test_chatbot_response():
    script = BASE_DIR / "interaction" / "imp-chatbot.py"
    result = subprocess.run([sys.executable, str(script)], input="Hello\n", text=True, capture_output=True)
    assert "Cimp" in result.stdout
    print("✅ Chatbot Response Test Passed!")


def test_chat_history():
    history_file = BASE_DIR / "logs" / "imp-chat-history.json"
    with open(history_file, "r") as f:
        before = len(json.load(f))
    script = BASE_DIR / "interaction" / "imp-chatbot.py"
    subprocess.run([sys.executable, str(script)], input="Hello\nquit\n", text=True, capture_output=True)
    with open(history_file, "r") as f:
        after = len(json.load(f))
    assert after == before + 2
    print("✅ Chat History Test Passed!")


def test_self_upgrader_log():
    log_file = BASE_DIR / "logs" / "imp-update-log.json"
    with open(log_file, "r") as f:
        before = len(json.load(f))
    subprocess.run([sys.executable, str(BASE_DIR / "self-improvement" / "imp-self-upgrader.py")])
    with open(log_file, "r") as f:
        after = len(json.load(f))
    assert after == before + 1
    print("✅ Self Upgrader Log Test Passed!")


test_chatbot_response()

test_self_upgrader_log()

test_chat_history()
