from pathlib import Path
import json
import subprocess

BASE_DIR = Path(__file__).resolve().parents[1]
INSIGHTS_FILE = BASE_DIR / "logs" / "imp-conversation-insights.json"


def test_conversation_analyzer():
    if INSIGHTS_FILE.exists():
        with open(INSIGHTS_FILE, 'r') as f:
            before = len(json.load(f))
    else:
        before = 0
    subprocess.run(["python3", str(BASE_DIR / "interaction" / "imp-conversation-analyzer.py")])
    with open(INSIGHTS_FILE, 'r') as f:
        after = len(json.load(f))
    assert after == before + 1
    print("✅ Conversation Analyzer Test Passed!")


test_conversation_analyzer()
