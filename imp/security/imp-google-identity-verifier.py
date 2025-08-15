import os
import json
import time
import random
try:
    from twilio.rest import Client
except Exception:
    Client = None
try:
    from google.oauth2 import id_token
    from google.auth.transport import requests
except Exception:
    id_token = None
    requests = None

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[1]
PERMISSIONS_FILE = str(BASE_DIR / "config" / "imp-user-permissions.json")
GOOGLE_CREDENTIAL_FILE = str(BASE_DIR / "config" / "imp-google-credentials.json")
PHONE_FILE = str(BASE_DIR / "config" / "imp-user-phones.json")
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


def send_sms_code(user: str):
    if Client is None:
        return None
    phones = load_json(PHONE_FILE)
    number = phones.get(user)
    if not number:
        return None
    sid = os.getenv("TWILIO_SID")
    token = os.getenv("TWILIO_AUTH_TOKEN")
    from_num = os.getenv("TWILIO_FROM_NUMBER")
    if not sid or not token or not from_num:
        return None
    code = f"{random.randint(0, 999999):06d}"
    try:
        client = Client(sid, token)
        client.messages.create(body=f"Your Cimp code is {code}", from_=from_num, to=number)
        return code
    except Exception:
        return None


def verify_google_user():
    username = input("Enter your name: ")
    if id_token is None or requests is None:
        print("⚠️ Required authentication libraries missing.")
        return False
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
        id_token.verify_oauth2_token(token, requests.Request(), client_id)
    except Exception:
        print("🚫 Invalid Google credentials")
        log_event("Failed Google credential verification", username)
        return False

    code = send_sms_code(username)
    if not code:
        print("⚠️ SMS delivery unavailable.")
        log_event("SMS unavailable", username)
        return False
    sms = input("Enter the SMS code: ")
    if sms.strip() != code:
        print("🚫 Invalid SMS code")
        log_event("Invalid SMS code", username)
        return False

    print("✅ Google authentication successful")
    log_event("Successful Google auth with SMS", username)
    return True


if __name__ == "__main__":
    verify_google_user()
