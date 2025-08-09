from pathlib import Path
import json
import time
import sys

BASE_DIR = Path(__file__).resolve().parents[1]
GI_PERF_FILE = BASE_DIR / "logs" / "imp-gi-performance.json"
SYSTEM_PERF_FILE = BASE_DIR / "logs" / "imp-performance.json"


def load_entries():
    if not GI_PERF_FILE.exists():
        return []
    with open(GI_PERF_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_entries(entries):
    with open(GI_PERF_FILE, "w") as f:
        json.dump(entries, f, indent=4)


def add_performance(name: str, cpu: float, memory: float):
    entries = load_entries()
    entries.append({
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "name": name,
        "cpu": cpu,
        "memory": memory,
    })
    save_entries(entries)
    print(f"[+] Performance entry stored for {name}")


def system_metrics() -> tuple[float | None, float | None]:
    if not SYSTEM_PERF_FILE.exists():
        return None, None
    try:
        with open(SYSTEM_PERF_FILE, "r") as f:
            data = json.load(f)
        cpu = float(str(data.get("CPU Usage (%)", 0)).replace("%", ""))
        mem = float(str(data.get("Memory Usage (%)", 0)).replace("%", ""))
        return cpu, mem
    except (json.JSONDecodeError, ValueError):
        return None, None


def update_from_system(name: str):
    cpu, mem = system_metrics()
    if cpu is None or mem is None:
        print("[!] No system performance data available")
        return
    add_performance(name, cpu, mem)


def list_performance(name: str | None = None):
    entries = load_entries()
    if name:
        entries = [e for e in entries if e.get("name") == name]
    for e in entries:
        cpu = e.get("cpu")
        mem = e.get("memory")
        print(f"{e['timestamp']} [{e['name']}] CPU {cpu}% MEM {mem}%")


def clear_performance(name: str | None = None):
    entries = load_entries()
    if name:
        entries = [e for e in entries if e.get("name") != name]
    else:
        entries = []
    save_entries(entries)
    target = name if name else "all"
    print(f"[+] Performance cleared for {target}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python3 imp-gi-performance.py <name> <cpu> <mem> | list [<name>] | clear [<name>] | update <name>"
        )
    elif sys.argv[1] == "list":
        name = sys.argv[2] if len(sys.argv) > 2 else None
        list_performance(name)
    elif sys.argv[1] == "clear":
        name = sys.argv[2] if len(sys.argv) > 2 else None
        clear_performance(name)
    elif sys.argv[1] == "update":
        if len(sys.argv) < 3:
            print("Usage: python3 imp-gi-performance.py update <name>")
        else:
            update_from_system(sys.argv[2])
    else:
        if len(sys.argv) < 4:
            print("Usage: python3 imp-gi-performance.py <name> <cpu> <mem>")
        else:
            add_performance(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]))
