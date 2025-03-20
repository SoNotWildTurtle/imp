import os
import json
import time

STATUS_FILE = "/root/imp/logs/imp-status.json"

def log_status():
    system_status = {
        "CPU Usage (%)": os.popen("grep 'cpu ' /proc/stat").read().strip(),
        "Memory Usage (%)": os.popen("free -m").read().strip(),
        "Uptime": os.popen("uptime -p").read().strip(),
    }

    with open(STATUS_FILE, "w") as f:
        json.dump(system_status, f, indent=4)

    print("[+] System status logged.")

while True:
    log_status()
    time.sleep(600)
