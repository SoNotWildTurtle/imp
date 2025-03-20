import os
import json
import time

LOG_FILES = {
    "activity": "/root/imp/logs/imp-activity-log.json",
    "security": "/root/imp/logs/imp-security-log.json",
    "updates": "/root/imp/logs/imp-update-log.json",
    "decisions": "/root/imp/logs/imp-decision-log.json",
    "performance": "/root/imp/logs/imp-performance.json",
    "integrity": "/root/imp/logs/imp-integrity-log.json"
}

def review_logs(log_type):
    if log_type not in LOG_FILES:
        print("⚠️ Invalid log type.")
        return

    with open(LOG_FILES[log_type], "r") as f:
        logs = json.load(f)
        for entry in logs:
            print(json.dumps(entry, indent=4))

def clean_logs(log_type):
    if log_type not in LOG_FILES:
        print("⚠️ Invalid log type.")
        return

    with open(LOG_FILES[log_type], "w") as f:
        json.dump([], f, indent=4)

    print(f"🗑️ {log_type} logs have been cleared.")

while True:
    action = input("Review or clean logs (format: review/clean log_type) or press Enter to skip: ")
    if action:
        parts = action.split(" ")
        if len(parts) == 2:
            if parts[0] == "review":
                review_logs(parts[1])
            elif parts[0] == "clean":
                clean_logs(parts[1])
    time.sleep(5)
