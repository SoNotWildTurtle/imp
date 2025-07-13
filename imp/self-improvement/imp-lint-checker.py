from pathlib import Path
import subprocess
import json
import time
import shutil

BASE_DIR = Path(__file__).resolve().parents[1]
LINT_LOG = BASE_DIR / "logs" / "imp-lint-log.json"

def run_lint() -> int:
    if shutil.which("flake8") is None:
        issues = []
    else:
        result = subprocess.run([
            "flake8",
            str(BASE_DIR / "self-improvement"),
        ], capture_output=True, text=True)
        issues = [line for line in result.stdout.splitlines() if line]
    log_entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "issue_count": len(issues),
    }
    logs = []
    if LINT_LOG.exists():
        with open(LINT_LOG, "r") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
    logs.append(log_entry)
    with open(LINT_LOG, "w") as f:
        json.dump(logs, f, indent=4)
    print(f"[+] Lint checker found {len(issues)} issues.")
    return len(issues)

if __name__ == "__main__":
    run_lint()
