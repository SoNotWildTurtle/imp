from pathlib import Path
import subprocess
import json
import time

BASE_DIR = Path(__file__).resolve().parents[1]
UPDATE_LOG = BASE_DIR / "logs" / "imp-update-log.json"


def log_update(status: str):
    log_entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "status": status,
    }
    logs = []
    if UPDATE_LOG.exists():
        with open(UPDATE_LOG, "r") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
    logs.append(log_entry)
    with open(UPDATE_LOG, "w") as f:
        json.dump(logs, f, indent=4)


def perform_upgrade():
    repo = str(BASE_DIR)
    subprocess.run(["git", "-C", repo, "fetch", "origin", "main"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    result = subprocess.run(["git", "-C", repo, "rev-list", "--count", "HEAD..origin/main"], capture_output=True, text=True)
    status = "Already up to date"
    if result.returncode == 0 and result.stdout.strip() != "0":
        subprocess.run(["git", "-C", repo, "pull", "origin", "main"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        status = "Updated from remote"
    log_update(status)
    print(f"[+] Self-upgrade check: {status}")


if __name__ == "__main__":
    perform_upgrade()
