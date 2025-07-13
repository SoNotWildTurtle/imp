from pathlib import Path
import json
import subprocess

BASE_DIR = Path(__file__).resolve().parents[1]
LINT_LOG = BASE_DIR / "logs" / "imp-lint-log.json"

def test_lint_checker():
    if LINT_LOG.exists():
        with open(LINT_LOG, "r") as f:
            before = len(json.load(f))
    else:
        before = 0
    subprocess.run(["python3", str(BASE_DIR / "self-improvement" / "imp-lint-checker.py")])
    with open(LINT_LOG, "r") as f:
        after = len(json.load(f))
    assert after == before + 1
    print("✅ Lint Checker Test Passed!")


test_lint_checker()
