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
LOCKOUT_FILE = str(BASE_DIR / "logs" / "imp-lockout-log.json")
LOCKOUT_TIME = 300
MAX_ATTEMPTS = 3


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


def load_lockouts():
    if not os.path.exists(LOCKOUT_FILE):
        return {}
    with open(LOCKOUT_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def save_lockouts(data):
    with open(LOCKOUT_FILE, "w") as f:
        json.dump(data, f, indent=4)


def register_failure(username: str):
    data = load_lockouts()
    entry = data.get(username, {"count": 0, "last": 0})
    now = time.time()
    if now - entry.get("last", 0) > LOCKOUT_TIME:
        entry = {"count": 1, "last": now}
    else:
        entry["count"] += 1
        entry["last"] = now
    data[username] = entry
    save_lockouts(data)


def clear_lockout(username: str):
    data = load_lockouts()
    if username in data:
        del data[username]
        save_lockouts(data)


def is_locked(username: str) -> bool:
    data = load_lockouts()
    entry = data.get(username)
    if not entry:
        return False
    now = time.time()
    if entry["count"] >= MAX_ATTEMPTS and now - entry["last"] <= LOCKOUT_TIME:
        return True
    if now - entry["last"] > LOCKOUT_TIME:
        clear_lockout(username)
    return False


def verify_user():
    username = input("Enter your name: ")
    if is_locked(username):
        print("🚫 Account locked due to repeated failures. Try again later.")
        log_event("Locked out", username)
        return False
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
        register_failure(username)
        return False

    passphrase = input("Enter your passphrase: ")
    hashed = hashlib.sha256(passphrase.encode()).hexdigest()
    if hashed != hash_pass:
        print("🚫 Invalid passphrase")
        log_event("Invalid passphrase", username)
        register_failure(username)
        return False

    clear_lockout(username)
    print("✅ Multi-factor authentication successful")
    log_event("Successful multi-factor auth", username)
    return True


if __name__ == "__main__":
    verify_user()
