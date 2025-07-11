from pathlib import Path
import json
import time

ROOT = Path(__file__).resolve().parents[1]
QUEUE_FILE = ROOT / "logs" / "imp-message-queue.json"
MAX_QUEUE_SIZE = 1000


def send_message(channel: str, text: str, priority: str = "normal") -> None:
    """Append a message to the queue with an optional priority."""
    queue = []
    if QUEUE_FILE.exists():
        with open(QUEUE_FILE, "r") as f:
            try:
                queue = json.load(f)
            except json.JSONDecodeError:
                queue = []
    queue.append({
        "channel": channel,
        "text": text,
        "priority": priority,
        "time": int(time.time()),
    })
    if len(queue) > MAX_QUEUE_SIZE:
        queue = queue[-MAX_QUEUE_SIZE:]
    with open(QUEUE_FILE, "w") as f:
        json.dump(queue, f, indent=4)


def receive_messages(channel: str):
    """Retrieve and remove all messages for the given channel, sorted by priority."""
    queue = []
    if QUEUE_FILE.exists():
        with open(QUEUE_FILE, "r") as f:
            try:
                queue = json.load(f)
            except json.JSONDecodeError:
                queue = []
    messages = [m for m in queue if m.get("channel") == channel]
    messages.sort(key=lambda m: (m.get("priority") != "high", m.get("time")))
    queue = [m for m in queue if m.get("channel") != channel]
    with open(QUEUE_FILE, "w") as f:
        json.dump(queue, f, indent=4)
    return messages


def broadcast_message(channels, text: str, priority: str = "normal") -> None:
    """Send the same message to multiple channels."""
    for channel in channels:
        send_message(channel, text, priority)


if __name__ == "__main__":
    send_message("test", "Hello world")
    broadcast_message(["a", "b"], "Hi all", priority="high")
    print(receive_messages("test"))
