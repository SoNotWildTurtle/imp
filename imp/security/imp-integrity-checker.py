import os
import hashlib
import json
import time

INTEGRITY_LOG = "/root/imp/logs/imp-integrity-log.json"
WATCHED_FILES = [
    "/etc/passwd",
    "/etc/shadow",
    "/etc/ssh/sshd_config",
    "/etc/sudoers"
]

def calculate_file_hash(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def check_integrity():
    print("🔍 Running system integrity check...")

    integrity_status = {}

    for file in WATCHED_FILES:
        file_hash = calculate_file_hash(file)
        if file_hash:
            integrity_status[file] = file_hash

    with open(INTEGRITY_LOG, "w") as f:
        json.dump(integrity_status, f, indent=4)

    print("[+] Integrity check completed.")

while True:
    check_integrity()
    time.sleep(3600)  # Runs every hour
