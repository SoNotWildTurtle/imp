from pathlib import Path
import json
import time

BASE_DIR = Path(__file__).resolve().parents[1]
PERFORMANCE_FILE = BASE_DIR / "logs" / "imp-performance.json"
NODE_HEALTH_FILE = BASE_DIR / "logs" / "imp-node-health.json"
HEALING_LOG = BASE_DIR / "logs" / "imp-healing-log.json"


def load_json(path):
    if not path.exists():
        return {}
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def log_action(action: str):
    logs = []
    if HEALING_LOG.exists():
        with open(HEALING_LOG, "r") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
    logs.append({
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "action": action,
    })
    with open(HEALING_LOG, "w") as f:
        json.dump(logs, f, indent=4)


def perform_self_healing():
    perf = load_json(PERFORMANCE_FILE)
    nodes = load_json(NODE_HEALTH_FILE)
    action = "System nominal"

    if perf:
        cpu = int(str(perf.get("CPU Usage (%)", "0")).replace("%", ""))
        if cpu > 90:
            action = "Restarted heavy processes"
    if nodes and any(status != "Online" for status in nodes.values()):
        action = "Attempted node restart"

    log_action(action)
    print(f"[+] Self-healing action: {action}")


if __name__ == "__main__":
    perform_self_healing()
