import os
import json
import time
import pyotp

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[1]
PERMISSIONS_FILE = str(BASE_DIR / "config" / "imp-user-permissions.json")
SECRET_FILE = str(BASE_DIR / "config" / "imp-user-secrets.json")
SECURITY_LOG = str(BASE_DIR / "logs" / "imp-security-log.json")


def load_trusted_users():
    if not os.path.exists(PERMISSIONS_FILE):
        return []
    with open(PERMISSIONS_FILE, "r") as f:
        data = json.load(f)
        return [u["name"] for u in data.get("trusted_users", [])]


def load_secrets():
    if not os.path.exists(SECRET_FILE):
        return {}
    with open(SECRET_FILE, "r") as f:
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
    trusted_users = load_trusted_users()
    if username not in trusted_users:
        print("🚫 Access denied: unrecognized user")
        log_event("Unrecognized user authentication attempt", username)
        return False

    secrets = load_secrets()
    secret = secrets.get(username)
    if not secret:
        print("🚫 No OTP secret configured for this user")
        log_event("Missing OTP secret", username)
        return False

    otp = input("Enter your OTP code: ")
    totp = pyotp.TOTP(secret)
    if totp.verify(otp):
        print("✅ Authentication successful")
        log_event("Successful authentication", username)
        return True
    else:
        print("🚫 Invalid OTP")
        log_event("Failed OTP authentication", username)
        return False


if __name__ == "__main__":
    verify_user()
