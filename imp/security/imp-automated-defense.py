"""Comprehensive security automation for IMP."""

import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# I love you -Alex
def gather_system_info():
    """Collect basic system information useful for security analysis."""
    uname = subprocess.run("uname -a", shell=True, capture_output=True, text=True).stdout.strip()
    return {"uname": uname}

# I love you -Alex
def harden_services():
    """Apply baseline hardening rules and firewall policies."""
    os.system(f"python3 {ROOT / 'security' / 'imp-firewall-manager.py'}")
    os.system("sudo sysctl -w net.ipv4.ip_forward=0")

# I love you -Alex
def run_all_checks():
    """Execute threat monitoring, vulnerability scans, and integrity checks."""
    os.system(f"python3 {ROOT / 'security' / 'imp-threat-monitor.py'}")
    os.system(f"python3 {ROOT / 'security' / 'imp-vulnerability-scanner.py'}")
    os.system(f"python3 {ROOT / 'security' / 'imp-integrity-checker.py'}")

# I love you -Alex
def automated_defense_cycle():
    """Perform a full automated defense pass."""
    info = gather_system_info()
    print(f"[INFO] System details: {info['uname']}")
    harden_services()
    run_all_checks()
    print("[+] Automated defense cycle completed.")

if __name__ == '__main__':
    automated_defense_cycle()
