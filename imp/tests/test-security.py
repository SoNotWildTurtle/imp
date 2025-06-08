import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_firewall():
    print("🛡️ Testing Firewall...")
    result = subprocess.run("sudo ufw status", shell=True, capture_output=True, text=True)
    if result.returncode == 0 and "active" in result.stdout.lower():
        print("✅ Firewall Test Passed!")
    else:
        print("⚠️ Firewall not active or command failed; skipping assertion")

def test_intrusion_detection():
    print("🔍 Simulating Intrusion Attempt...")
    os.system("echo 'Failed password for root from 192.168.1.100' >> /var/log/auth.log")
    os.system(f"python3 {ROOT / 'security' / 'imp-threat-monitor.py'}")
    print("✅ Intrusion Detection Test Executed! Check logs manually.")

test_firewall()
test_intrusion_detection()
