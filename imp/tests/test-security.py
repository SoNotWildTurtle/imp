import os
import subprocess
import pyotp

USER_SECRET = "C3MAB55AJKUAF3LTLGJFO33NPKCDHYWL"
USER_NAME = "Alexander Raymond Graham (Minc)"

def test_firewall():
    print("🛡️ Testing Firewall...")
    firewall_status = subprocess.run("sudo ufw status", shell=True, capture_output=True, text=True).stdout
    assert "active" in firewall_status
    print("✅ Firewall Test Passed!")

def test_intrusion_detection():
    print("🔍 Simulating Intrusion Attempt...")
    os.system("echo 'Failed password for root from 192.168.1.100' >> /var/log/auth.log")
    os.system("python3 /root/imp/security/imp-threat-monitor.py")
    print("✅ Intrusion Detection Test Executed! Check logs manually.")

def test_identity_verification():
    print("🔐 Testing Identity Verification...")
    totp = pyotp.TOTP(USER_SECRET)
    otp = totp.now()
    cmd = ["python3", "/root/imp/security/imp-identity-verifier.py"]
    proc = subprocess.run(cmd, input=f"{USER_NAME}\n{otp}\n", text=True, capture_output=True)
    assert "Authentication successful" in proc.stdout
    print("✅ Identity Verification Test Passed!")

test_firewall()
test_intrusion_detection()
test_identity_verification()
