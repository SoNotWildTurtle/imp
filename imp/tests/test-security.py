import os
import subprocess
import os.path

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def test_firewall():
    print("🛡️ Testing Firewall...")
    firewall_status = subprocess.run("sudo ufw status", shell=True, capture_output=True, text=True).stdout
    assert "active" in firewall_status
    print("✅ Firewall Test Passed!")

def test_intrusion_detection():
    print("🔍 Simulating Intrusion Attempt...")
    os.system("echo 'Failed password for root from 192.168.1.100' >> /var/log/auth.log")
    os.system(f"python3 {os.path.join(BASE_DIR, 'security', 'imp-threat-monitor.py')}")
    print("✅ Intrusion Detection Test Executed! Check logs manually.")

test_firewall()
test_intrusion_detection()
