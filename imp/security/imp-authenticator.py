import argparse
import getpass
import hashlib
import json
import os
import random
import time
from pathlib import Path

try:
    from google.oauth2 import id_token
    from google.auth.transport import requests as google_requests
    from google_auth_oauthlib.flow import InstalledAppFlow
except Exception:  # pragma: no cover - google-auth optional
    id_token = None
    google_requests = None
    InstalledAppFlow = None

try:
    from twilio.rest import Client
except Exception:  # pragma: no cover - twilio optional
    Client = None

ROOT = Path(__file__).resolve().parents[1]
CRED_FILE = ROOT / "config" / "imp-credentials.json"
LOG_FILE = ROOT / "logs" / "imp-auth-log.json"
OAUTH_FILE = ROOT / "config" / "imp-google-oauth.json"


def load_creds():
    if not CRED_FILE.exists():
        return []
    with open(CRED_FILE, "r") as f:
        data = json.load(f)
    return data.get("users", [])


def authenticate(username: str, password: str) -> bool:
    creds = load_creds()
    hashed = hashlib.sha256(password.encode()).hexdigest()
    for user in creds:
        if user.get("username") == username and user.get("password_hash") == hashed:
            return True
    return False


def record_attempt(username: str, success: bool) -> None:
    try:
        entries = []
        if LOG_FILE.exists():
            with open(LOG_FILE, "r") as f:
                entries = json.load(f)
    except Exception:
        entries = []
    entries.append({"user": username, "success": success})
    with open(LOG_FILE, "w") as f:
        json.dump(entries, f, indent=4)


def authenticate_google(token: str) -> bool:
    if id_token is None or google_requests is None:
        return False
    try:
        info = id_token.verify_oauth2_token(token, google_requests.Request())
        return bool(info.get("sub"))
    except Exception:
        return False


def authenticate_google_auto(email: str | None = None) -> bool:
    if InstalledAppFlow is None:
        return False
    if not OAUTH_FILE.exists():
        print("Missing OAuth client file")
        return False
    try:
        flow = InstalledAppFlow.from_client_secrets_file(
            str(OAUTH_FILE), scopes=["openid", "email"]
        )
        creds = flow.run_local_server(port=0)
        token = getattr(creds, "id_token", None)
        if token is None:
            return False
        if email and id_token and google_requests:
            try:
                info = id_token.verify_oauth2_token(token, google_requests.Request())
                if info.get("email") != email:
                    return False
            except Exception:
                return False
        return True
    except Exception:
        return False


def twilio_2fa(phone: str) -> bool:
    if Client is None:
        return False
    sid = os.getenv("TWILIO_ACCOUNT_SID")
    token = os.getenv("TWILIO_AUTH_TOKEN")
    from_num = os.getenv("TWILIO_FROM")
    if not (sid and token and from_num):
        return False
    client = Client(sid, token)
    code = f"{random.randint(100000, 999999)}"
    try:
        client.messages.create(to=phone, from_=from_num, body=f"Your IMP code: {code}")
    except Exception:
        return False
    entered = input("Enter verification code: ").strip()
    return entered == code


def idle_relog(last_active: float, phone: str | None = None, email: str | None = None) -> bool:
    if time.time() - last_active < 300:
        return True
    if not authenticate_google_auto(email):
        return False
    if phone and not twilio_2fa(phone):
        return False
    return True


def main():
    parser = argparse.ArgumentParser(description="IMP User Authentication")
    parser.add_argument("-u", "--username", help="Username")
    parser.add_argument("-p", "--password", help="Password")
    parser.add_argument("-g", "--google-token", help="Google ID token")
    parser.add_argument("--google-auto", action="store_true", help="Interactive Google OAuth")
    parser.add_argument("--google-email", help="Google account email")
    args = parser.parse_args()

    if args.google_token:
        ok = authenticate_google(args.google_token)
        record_attempt("google", ok)
        print("Authentication successful" if ok else "Authentication failed")
        return

    if args.google_auto:
        ok = authenticate_google_auto(args.google_email)
        record_attempt("google_auto", ok)
        print("Authentication successful" if ok else "Authentication failed")
        return

    user = args.username or input("Username: ")
    passwd = args.password or getpass.getpass("Password: ")

    ok = authenticate(user, passwd)
    record_attempt(user, ok)

    if ok:
        print("Authentication successful")
    else:
        print("Authentication failed")


if __name__ == "__main__":
    main()
