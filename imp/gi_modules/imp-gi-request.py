from pathlib import Path
import json
import time
import sys

BASE_DIR = Path(__file__).resolve().parents[1]
REQUEST_FILE = BASE_DIR / "logs" / "imp-gi-requests.json"
INSIGHTS_FILE = BASE_DIR / "logs" / "imp-conversation-insights.json"
CONFIG_DIR = BASE_DIR / "config" / "gi"


def load_requests():
    if not REQUEST_FILE.exists():
        return []
    with open(REQUEST_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_requests(entries):
    with open(REQUEST_FILE, "w") as f:
        json.dump(entries, f, indent=4)


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


def update_from_conversation(name: str):
    words = latest_keywords()
    if not words:
        print("[!] No conversation insights available")
        return
    detail = "Request based on keywords: " + ", ".join(words)
    log_request(name, detail)


def log_request(name: str, request: str):
    entries = load_requests()
    entries.append({
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "name": name,
        "request": request,
    })
    save_requests(entries)
    print(f"[+] Request logged for {name}")
    port = get_port(name)
    if port:
        print(f"[i] Await confirmation from Cimp on port {port}")


def list_requests(name: str | None = None):
    entries = load_requests()
    if name:
        entries = [e for e in entries if e.get("name") == name]
    for e in entries:
        print(f"{e['timestamp']} [{e['name']}] {e['request']}")


def clear_requests(name: str | None = None):
    entries = load_requests()
    if name:
        entries = [e for e in entries if e.get("name") != name]
    else:
        entries = []
    save_requests(entries)
    target = name if name else "all"
    print(f"[+] Requests cleared for {target}")


def get_port(name: str) -> str | None:
    cfg = CONFIG_DIR / f"{name}.json"
    if cfg.exists():
        try:
            with open(cfg, "r") as f:
                data = json.load(f)
                return data.get("dashboard_port")
        except json.JSONDecodeError:
            return None
    return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 imp-gi-request.py <name> <request> | list [<name>] | clear [<name>] | update <name>")
    elif sys.argv[1] == "list":
        name = sys.argv[2] if len(sys.argv) > 2 else None
        list_requests(name)
    elif sys.argv[1] == "clear":
        name = sys.argv[2] if len(sys.argv) > 2 else None
        clear_requests(name)
    elif sys.argv[1] == "update":
        if len(sys.argv) < 3:
            print("Usage: python3 imp-gi-request.py update <name>")
        else:
            update_from_conversation(sys.argv[2])
    else:
        if len(sys.argv) < 3:
            print("Usage: python3 imp-gi-request.py <name> <request>")
        else:
            log_request(sys.argv[1], " ".join(sys.argv[2:]))
