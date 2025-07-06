import json

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
LOG_FILES = [
    BASE_DIR / "logs" / "imp-activity-log.json",
    BASE_DIR / "logs" / "imp-security-log.json",
    BASE_DIR / "logs" / "imp-update-log.json",
]

def test_logging_system():
    print("📝 Checking Logging System...")

    for log_file in LOG_FILES:
        with open(log_file, "r") as f:
            logs = json.load(f)
            assert len(logs) > 0, f"⚠️ Log file {log_file} is empty!"

    print("✅ Logging System Test Passed!")

test_logging_system()
