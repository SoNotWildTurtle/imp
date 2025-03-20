import os
import json
import subprocess
import time

LOG_ANALYSIS_FILE = "/root/imp/logs/imp-log-analysis.json"

def analyze_logs():
    print("📊 Analyzing system logs for anomalies...")

    anomalies = {}

    # Detect excessive failed login attempts
    failed_logins = subprocess.run("grep 'Failed password' /var/log/auth.log | wc -l", shell=True, capture_output=True, text=True).stdout.strip()
    if int(failed_logins) > 10:
        anomalies["Excessive Failed Logins"] = failed_logins

    # Detect unexpected user privilege escalation
    sudo_attempts = subprocess.run("grep 'sudo' /var/log/auth.log | wc -l", shell=True, capture_output=True, text=True).stdout.strip()
    if int(sudo_attempts) > 5:
        anomalies["Suspicious Privilege Escalation"] = sudo_attempts

    if anomalies:
        with open(LOG_ANALYSIS_FILE, "w") as f:
            json.dump(anomalies, f, indent=4)

        print(f"⚠️ Detected anomalies: {anomalies}")

while True:
    analyze_logs()
    time.sleep(3600)  # Runs every hour
