from pathlib import Path
import json
import time
import sys

BASE_DIR = Path(__file__).resolve().parents[1]
RISK_FILE = BASE_DIR / "logs" / "imp-gi-risks.json"
INSIGHTS_FILE = BASE_DIR / "logs" / "imp-conversation-insights.json"


def load_risks():
    if not RISK_FILE.exists():
        return []
    with open(RISK_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_risks(data):
    with open(RISK_FILE, "w") as f:
        json.dump(data, f, indent=4)


def latest_keywords() -> list[str]:
    if not INSIGHTS_FILE.exists():
        return []
    try:
        with open(INSIGHTS_FILE, "r") as f:
            data = json.load(f)
            if data:
                return [w for w, _ in data[-1].get("top_words", [])]
    except json.JSONDecodeError:
        pass
    return []


def add_risk(name: str, risk: str):
    data = load_risks()
    data.append({
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "name": name,
        "risk": risk,
    })
    save_risks(data)
    print(f"[+] Risk logged for {name}")


def update_from_conversation(name: str):
    words = latest_keywords()
    if not words:
        print("[!] No conversation insights available")
        return
    add_risk(name, "Risks mentioned: " + ", ".join(words))


def list_risks(name: str | None = None):
    data = load_risks()
    if name:
        data = [d for d in data if d.get("name") == name]
    for d in data:
        print(f"{d['timestamp']} [{d['name']}] {d['risk']}")


def clear_risks(name: str | None = None):
    data = load_risks()
    if name:
        data = [d for d in data if d.get("name") != name]
    else:
        data = []
    save_risks(data)
    target = name if name else "all"
    print(f"[+] Risks cleared for {target}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 imp-gi-risk-analyzer.py <name> <risk> | list [<name>] | clear [<name>] | update <name>")
    elif sys.argv[1] == "list":
        name = sys.argv[2] if len(sys.argv) > 2 else None
        list_risks(name)
    elif sys.argv[1] == "clear":
        name = sys.argv[2] if len(sys.argv) > 2 else None
        clear_risks(name)
    elif sys.argv[1] == "update":
        if len(sys.argv) < 3:
            print("Usage: python3 imp-gi-risk-analyzer.py update <name>")
        else:
            update_from_conversation(sys.argv[2])
    else:
        if len(sys.argv) < 3:
            print("Usage: python3 imp-gi-risk-analyzer.py <name> <risk>")
        else:
            add_risk(sys.argv[1], " ".join(sys.argv[2:]))
