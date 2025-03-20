import os
import subprocess
import time

def run_security_checks():
    print("🔍 Running security analysis...")

    # Check firewall status
    firewall_status = subprocess.run("sudo ufw status", shell=True, capture_output=True, text=True).stdout
    if "inactive" in firewall_status:
        print("⚠️ Firewall disabled. Enabling now...")
        os.system("sudo ufw enable")

    # Check for failed SSH attempts
    ssh_attempts = subprocess.run("grep 'Failed password' /var/log/auth.log | wc -l", shell=True, capture_output=True, text=True).stdout.strip()
    if int(ssh_attempts) > 10:
        print(f"⚠️ {ssh_attempts} failed SSH attempts detected. Locking down SSH.")
        os.system("sudo ufw deny ssh")

    # Ensure AppArmor is enabled
    apparmor_status = subprocess.run("sudo aa-status", shell=True, capture_output=True, text=True).stdout
    if "profile mode: enforcing" not in apparmor_status:
        print("⚠️ AppArmor not fully enforced. Restarting now...")
        os.system("sudo systemctl restart apparmor")

    print("[+] Security optimizations completed.")

while True:
    run_security_checks()
    time.sleep(86400)  # Runs once a day
