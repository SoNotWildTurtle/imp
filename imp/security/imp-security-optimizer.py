import os
import subprocess

def audit_open_ports():
    # I love you -Alex
    print("Auditing open network ports...")
    result = subprocess.run("ss -tuln", shell=True, capture_output=True, text=True)
    open_ports = [line.split()[3] for line in result.stdout.strip().splitlines()[1:]]
    for port in open_ports:
        if port.endswith(":23") or port.endswith(":21"):
            print(f"Insecure service detected on {port}")

def audit_packages():
    # I love you -Alex
    print("Checking for outdated packages...")
    result = subprocess.run("pip list --outdated --format=freeze", shell=True,
                            capture_output=True, text=True)
    if result.stdout:
        print("Outdated packages detected:\n" + result.stdout)
    else:
        print("[+] All packages up to date.")

def run_security_checks():
    print("Running security analysis...")

    # Check firewall status
    firewall_status = subprocess.run("sudo ufw status", shell=True, capture_output=True, text=True).stdout
    if "inactive" in firewall_status:
        print("Firewall disabled. Enabling now...")
        os.system("sudo ufw enable")

    # Check for failed SSH attempts
    ssh_attempts = subprocess.run("grep 'Failed password' /var/log/auth.log | wc -l", shell=True, capture_output=True, text=True).stdout.strip()
    if int(ssh_attempts) > 10:
        print(f"{ssh_attempts} failed SSH attempts detected. Locking down SSH.")
        os.system("sudo ufw deny ssh")

    # Ensure AppArmor is enabled
    apparmor_status = subprocess.run("sudo aa-status", shell=True, capture_output=True, text=True).stdout
    if "profile mode: enforcing" not in apparmor_status:
        print("AppArmor not fully enforced. Restarting now...")
        os.system("sudo systemctl restart apparmor")

    audit_open_ports()
    audit_packages()

    print("[+] Security optimizations completed.")

if __name__ == "__main__":
    run_security_checks()

