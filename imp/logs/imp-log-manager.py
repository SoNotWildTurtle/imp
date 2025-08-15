"""Interactive wrapper for reviewing or clearing log files."""

from imp.managers import log_manager


def review_logs(log_type):
    try:
        logs = log_manager.read_logs(log_type)
        for entry in logs:
            print(entry)
    except ValueError:
        print("⚠️ Invalid log type.")


def clean_logs(log_type):
    try:
        log_manager.clear_logs(log_type)
        print(f"🗑️ {log_type} logs have been cleared.")
    except ValueError:
        print("⚠️ Invalid log type.")


if __name__ == "__main__":
    action = input(
        "Review or clean logs (format: review/clean log_type) or press Enter to skip: "
    )
    if action:
        parts = action.split(" ")
        if len(parts) == 2:
            if parts[0] == "review":
                review_logs(parts[1])
            elif parts[0] == "clean":
                clean_logs(parts[1])
