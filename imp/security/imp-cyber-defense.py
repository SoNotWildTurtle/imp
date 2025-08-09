from pathlib import Path
import json
import time

BASE_DIR = Path(__file__).resolve().parents[1]
SECURITY_LOG = BASE_DIR / "logs" / "imp-security-log.json"


def load_log():
    if SECURITY_LOG.exists():
        with open(SECURITY_LOG, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def log_defense(event: str):
    logs = load_log()
    logs.append({
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "event": event,
    })
    with open(SECURITY_LOG, "w") as f:
        json.dump(logs, f, indent=4)


def run_defense_cycle():
    print("🛡️ Running cyber defense cycle...")
    log_defense("Defense cycle executed")


if __name__ == "__main__":
    run_defense_cycle()
