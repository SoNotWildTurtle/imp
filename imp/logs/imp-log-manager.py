import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG_FILES = {
    "activity": ROOT / "logs" / "imp-activity-log.json",
    "security": ROOT / "logs" / "imp-security-log.json",
    "updates": ROOT / "logs" / "imp-update-log.json",
    "decisions": ROOT / "logs" / "imp-decision-log.json",
    "performance": ROOT / "logs" / "imp-performance.json",
    "integrity": ROOT / "logs" / "imp-integrity-log.json"
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

if __name__ == "__main__":
    action = input("Review or clean logs (format: review/clean log_type) or press Enter to skip: ")
    if action:
        parts = action.split(" ")
        if len(parts) == 2:
            if parts[0] == "review":
                review_logs(parts[1])
            elif parts[0] == "clean":
                clean_logs(parts[1])
