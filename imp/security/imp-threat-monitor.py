import subprocess
import json
from pathlib import Path

THREAT_LOG = Path(__file__).resolve().parents[1] / "logs" / "imp-threat-log.json"

def detect_intrusions():
    print("Scanning system logs for threats...")

    # Check for brute-force SSH attacks
    ssh_attempts = subprocess.run("grep 'Failed password' /var/log/auth.log | wc -l", shell=True, capture_output=True, text=True).stdout.strip()
    suspicious_processes = subprocess.run("ps aux | grep -E 'nc|nmap|hydra|medusa|john|sqlmap' | grep -v grep | wc -l", shell=True, capture_output=True, text=True).stdout.strip()

    threats = {}

    if int(ssh_attempts) > 10:
        threats["SSH Brute Force"] = f"{ssh_attempts} failed attempts detected"

    if int(suspicious_processes) > 0:
        threats["Suspicious Processes"] = f"{suspicious_processes} known attack tools running"

    if threats:
        with open(THREAT_LOG, "w") as f:
            json.dump(threats, f, indent=4)

        print(f"THREAT DETECTED: {threats}")

if __name__ == "__main__":
    THREAT_LOG.parent.mkdir(parents=True, exist_ok=True)
    detect_intrusions()
