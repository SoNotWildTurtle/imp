import sys
from pathlib import Path
import subprocess
import json

BASE_DIR = Path(__file__).resolve().parents[1]
LOG_FILE = BASE_DIR / "logs" / "imp-chat-history.json"
VIEWER = BASE_DIR / "interaction" / "imp-chat-history-viewer.py"


def test_chat_history_viewer():
    LOG_FILE.write_text(json.dumps([
        {"timestamp": "2025-01-01", "role": "user", "message": "hello"},
        {"timestamp": "2025-01-01", "role": "imp", "message": "hi"}
    ], indent=4))
    result = subprocess.run([sys.executable, str(VIEWER)], capture_output=True, text=True)
    assert "hello" in result.stdout and "imp" in result.stdout
    print("✅ Chat History Viewer Test Passed!")


if __name__ == "__main__":
    test_chat_history_viewer()
