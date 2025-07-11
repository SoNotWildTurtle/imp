import os
import subprocess

def enforce_firewall():
    print("Checking firewall settings...")

    firewall_rules = [
        "sudo ufw default deny incoming",
        "sudo ufw allow ssh",
        "sudo ufw allow 443/tcp"
    ]

    for rule in firewall_rules:
        os.system(rule)

    # Ensure firewall is active
    firewall_status = subprocess.run("sudo ufw status", shell=True, capture_output=True, text=True).stdout
    if "inactive" in firewall_status:
        print("Firewall is disabled. Enabling it now...")
        os.system("sudo ufw enable")

    print("[+] Firewall rules enforced.")

if __name__ == "__main__":
    enforce_firewall()
