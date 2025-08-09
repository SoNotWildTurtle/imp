from pathlib import Path
import json
import time

BASE_DIR = Path(__file__).resolve().parents[1]
SECURITY_LOG = BASE_DIR / "logs" / "imp-security-log.json"
METACOG_LOG = BASE_DIR / "logs" / "imp-metacognition-log.json"


def load_entries(path):
    if not path.exists():
        return []
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def analyze_security_impact():
    logs = load_entries(SECURITY_LOG)
    threats = sum(1 for e in logs if e.get("threat"))
    return (
        f"Detected {threats} recorded threats. "
        "These events could compromise user privacy or system integrity if left unchecked."
    )


def log_metacognition(text: str):
    entries = load_entries(METACOG_LOG)
    entries.append({
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "analysis": text,
    })
    with open(METACOG_LOG, "w") as f:
        json.dump(entries, f, indent=4)


def run_metacognition():
    analysis = analyze_security_impact()
    log_metacognition(analysis)
    print(f"[Metacognition] {analysis}")


if __name__ == "__main__":
    run_metacognition()
