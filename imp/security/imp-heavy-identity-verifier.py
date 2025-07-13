import os
import json
import time
import hashlib
import pyotp
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
PERMISSIONS_FILE = str(BASE_DIR / "config" / "imp-user-permissions.json")
SECRET_FILE = str(BASE_DIR / "config" / "imp-user-secrets.json")
PASSPHRASE_FILE = str(BASE_DIR / "config" / "imp-user-passphrases.json")
SECURITY_LOG = str(BASE_DIR / "logs" / "imp-security-log.json")


def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)


def log_event(event, user):
    logs = []
    if os.path.exists(SECURITY_LOG):
        with open(SECURITY_LOG, "r") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
    logs.append({
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "event": event,
        "user": user
    })
    with open(SECURITY_LOG, "w") as f:
        json.dump(logs, f, indent=4)


def verify_user():
    username = input("Enter your name: ")
    trusted = [u["name"] for u in load_json(PERMISSIONS_FILE).get("trusted_users", [])]
    if username not in trusted:
        print("🚫 Access denied: unrecognized user")
        log_event("Unrecognized user", username)
        return False

    secrets = load_json(SECRET_FILE)
    passphrases = load_json(PASSPHRASE_FILE)
    secret = secrets.get(username)
    hash_pass = passphrases.get(username)
    if not secret or not hash_pass:
        print("🚫 Credentials not configured for this user")
        log_event("Missing credentials", username)
        return False

    otp = input("Enter your OTP code: ")
    totp = pyotp.TOTP(secret)
    if not totp.verify(otp):
        print("🚫 Invalid OTP")
        log_event("Invalid OTP", username)
        return False

    passphrase = input("Enter your passphrase: ")
    hashed = hashlib.sha256(passphrase.encode()).hexdigest()
    if hashed != hash_pass:
        print("🚫 Invalid passphrase")
        log_event("Invalid passphrase", username)
        return False

    print("✅ Multi-factor authentication successful")
    log_event("Successful multi-factor auth", username)
    return True


if __name__ == "__main__":
    verify_user()
