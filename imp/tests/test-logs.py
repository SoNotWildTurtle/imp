import json
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

LOG_FILES = [
    os.path.join(BASE_DIR, "logs", "imp-activity-log.json"),
    os.path.join(BASE_DIR, "logs", "imp-security-log.json"),
    os.path.join(BASE_DIR, "logs", "imp-update-log.json"),
]

def test_logging_system():
    print("📝 Checking Logging System...")

    for log_file in LOG_FILES:
        with open(log_file, "r") as f:
            logs = json.load(f)
            assert len(logs) > 0, f"⚠️ Log file {log_file} is empty!"

    print("✅ Logging System Test Passed!")

test_logging_system()
