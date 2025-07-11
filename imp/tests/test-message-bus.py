from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
BUS_FILE = ROOT / "logs" / "imp-message-queue.json"

MODULE_PATH = ROOT / "core" / "imp-message-bus.py"
spec = importlib.util.spec_from_file_location("imp_message_bus", MODULE_PATH)
bus = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bus)

print("Testing message bus...")

bus.send_message("test", "hello", priority="high")
bus.broadcast_message(["a", "b"], "hey", priority="low")
msgs = bus.receive_messages("test")
assert msgs and msgs[0]["text"] == "hello" and msgs[0]["priority"] == "high", "Message bus failed"

print("Message Bus Test Passed!")
