from pathlib import Path
import json
import sys

BASE_DIR = Path(__file__).resolve().parents[1]
HISTORY_FILE = BASE_DIR / "logs" / "imp-chat-history.json"


def load_history():
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def print_entries(entries):
    for entry in entries:
        ts = entry.get("timestamp", "")
        role = entry.get("role", "")
        msg = entry.get("message", "")
        print(f"{ts} {role}: {msg}")


def main():
    args = sys.argv[1:]
    history = load_history()
    if not history:
        print("No chat history available.")
        return

    if args and args[0] == "search" and len(args) > 1:
        keyword = args[1].lower()
        history = [h for h in history if keyword in h.get("message", "").lower()]
    elif args and args[0] == "clear":
        HISTORY_FILE.write_text("[]")
        print("Chat history cleared.")
        return

    limit = None
    if args and args[0].isdigit():
        limit = int(args[0])
    if limit:
        history = history[-limit:]
    print_entries(history)


if __name__ == "__main__":
    main()
