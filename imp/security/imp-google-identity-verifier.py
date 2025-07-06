import os
import json
import time
import pyotp
from google.oauth2 import id_token
from google.auth.transport import requests

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[1]
PERMISSIONS_FILE = str(BASE_DIR / "config" / "imp-user-permissions.json")
GOOGLE_CREDENTIAL_FILE = str(BASE_DIR / "config" / "imp-google-credentials.json")
SECRET_FILE = str(BASE_DIR / "config" / "imp-user-secrets.json")
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


def verify_google_user():
    username = input("Enter your name: ")
    trusted_users = [u["name"] for u in load_json(PERMISSIONS_FILE).get("trusted_users", [])]
    if username not in trusted_users:
        print("🚫 Access denied: unrecognized user")
        log_event("Unrecognized user", username)
        return False

    clients = load_json(GOOGLE_CREDENTIAL_FILE)
    client_id = clients.get(username)
    if not client_id:
        print("🚫 No Google client configured for this user")
        log_event("Missing Google client", username)
        return False

    token = input("Enter your Google ID token: ")
    try:
        id_info = id_token.verify_oauth2_token(token, requests.Request(), client_id)
    except Exception:
        print("🚫 Invalid Google credentials")
        log_event("Failed Google credential verification", username)
        return False

    secrets = load_json(SECRET_FILE)
    secret = secrets.get(username)
    if not secret:
        print("🚫 No OTP secret configured")
        log_event("Missing OTP secret", username)
        return False

    otp = input("Enter your OTP code: ")
    totp = pyotp.TOTP(secret)
    if totp.verify(otp):
        print("✅ Google authentication successful")
        log_event("Successful Google auth", username)
        return True
    else:
        print("🚫 Invalid OTP")
        log_event("Failed OTP auth", username)
        return False


if __name__ == "__main__":
    verify_google_user()
