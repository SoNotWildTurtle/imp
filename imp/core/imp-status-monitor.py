import os
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS_FILE = ROOT / "logs" / "imp-status.json"

def log_status():
    system_status = {
        "CPU Usage (%)": os.popen("grep 'cpu ' /proc/stat").read().strip(),
        "Memory Usage (%)": os.popen("free -m").read().strip(),
        "Uptime": os.popen("uptime -p").read().strip(),
    }

    with open(STATUS_FILE, "w") as f:
        json.dump(system_status, f, indent=4)

    print("[+] System status logged.")

if __name__ == "__main__":
    log_status()
