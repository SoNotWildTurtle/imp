"""Temporal threat analysis for automatic countermeasures."""

import json
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
THREAT_LOG = BASE_DIR / "logs" / "imp-threat-log.json"
COUNTER_LOG = BASE_DIR / "logs" / "imp-ai-countermeasures.json"


def load_json(path, default):
    if path.exists():
        try:
            with open(path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return default
    return default


def analyze_threats():
    threats = load_json(THREAT_LOG, {})
    history = load_json(COUNTER_LOG, [])
    now = datetime.utcnow()

    if not isinstance(threats, dict) or not threats:
        print("✅ No threats detected.")
        return

    for name, detail in threats.items():
        recent = [e for e in history if e.get("threat") == name]
        action = "Deploy countermeasures"
        if recent:
            last_time = datetime.fromisoformat(recent[-1]["timestamp"])
            if now - last_time < timedelta(hours=1):
                action = "Escalate defenses"
        history.append(
            {
                "timestamp": now.isoformat(),
                "threat": name,
                "detail": detail,
                "action": action,
            }
        )
        print(f"🛡️ {action} for {name}")

    with open(COUNTER_LOG, "w") as f:
        json.dump(history, f, indent=4)


if __name__ == "__main__":
    analyze_threats()
