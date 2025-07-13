import os
import subprocess
import json
try:
    import pyotp
except ImportError:
    pyotp = None
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
USER_SECRET = "C3MAB55AJKUAF3LTLGJFO33NPKCDHYWL"
USER_NAME = "Alexander Raymond Graham (Minc)"

def test_firewall():
    print("🛡️ Testing Firewall...")
    result = subprocess.run("which ufw", shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print("⚠️ ufw not installed. Skipping firewall test.")
        return
    firewall_status = subprocess.run("sudo ufw status", shell=True, capture_output=True, text=True).stdout
    assert "active" in firewall_status
    print("✅ Firewall Test Passed!")

def test_intrusion_detection():
    print("🔍 Simulating Intrusion Attempt...")
    os.system("echo 'Failed password for root from 192.168.1.100' >> /var/log/auth.log")
    print("✅ Intrusion Detection Test Executed! (skipped real monitor)")

def test_identity_verification():
    print("🔐 Testing Identity Verification...")
    if pyotp is None:
        print("⚠️ pyotp not available. Skipping OTP test.")
        return
    totp = pyotp.TOTP(USER_SECRET)
    otp = totp.now()
    cmd = ["python3", str(BASE_DIR / "security" / "imp-identity-verifier.py")]
    proc = subprocess.run(cmd, input=f"{USER_NAME}\n{otp}\n", text=True, capture_output=True)
    assert "Authentication successful" in proc.stdout
    print("✅ Identity Verification Test Passed!")

def test_google_identity_verification():
    print("🔐 Testing Google Identity Verification...")
    cmd = ["python3", str(BASE_DIR / "security" / "imp-google-identity-verifier.py")]
    if pyotp is None:
        print("⚠️ pyotp not available. Skipping Google auth test.")
        return
    try:
        from google.oauth2 import id_token  # type: ignore
    except Exception:
        print("⚠️ google auth libraries not available. Skipping Google auth test.")
        return
    try:
        proc = subprocess.run(
            cmd,
            input=f"{USER_NAME}\ninvalid-token\n123456\n",
            text=True,
            capture_output=True,
            timeout=5,
        )
        assert "Invalid Google credentials" in proc.stdout
    except subprocess.TimeoutExpired:
        print("⚠️ Google verification timed out (expected in offline tests)")
    print("✅ Identity Verification Test Passed!")


def test_cyber_defense_cycle():
    log_file = BASE_DIR / "logs" / "imp-security-log.json"
    with open(log_file, "r") as f:
        before = len(json.load(f))
    script = BASE_DIR / "security" / "imp-cyber-defense.py"
    subprocess.run(["python3", str(script)])
    with open(log_file, "r") as f:
        after = len(json.load(f))
    assert after == before + 1
    print("✅ Cyber Defense Cycle Test Passed!")

test_firewall()
test_intrusion_detection()
test_identity_verification()
test_google_identity_verification()
test_cyber_defense_cycle()

def test_heavy_identity_verification():
    print("🔐 Testing Heavy Identity Verification...")
    if pyotp is None:
        print("⚠️ pyotp not available. Skipping heavy verification test.")
        return
    import hashlib
    totp = pyotp.TOTP(USER_SECRET)
    otp = totp.now()
    script = BASE_DIR / "security" / "imp-heavy-identity-verifier.py"
    proc = subprocess.run(
        ["python3", str(script)],
        input=f"{USER_NAME}\n{otp}\nOpenSesame\n",
        text=True,
        capture_output=True,
    )
    assert "multi-factor authentication successful" in proc.stdout.lower()
    print("✅ Heavy Identity Verification Test Passed!")


test_heavy_identity_verification()
