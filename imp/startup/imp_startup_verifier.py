from datetime import datetime
from pathlib import Path
import importlib
import importlib.util
import json

BASE_DIR = Path(__file__).resolve().parents[1]
LOG_FILE = BASE_DIR / "logs" / "imp-startup-verification.json"

def _check_import(name):
    importlib.import_module(name)


def _check_file(path):
    if not path.exists():
        raise FileNotFoundError(path)


def _check_import_file(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)


def _append_log(entry):
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = []
    data.append(entry)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def run():
    steps = [
        ("pyotp dependency", lambda: _check_import("pyotp")),
        ("google auth dependency", lambda: _check_import("google.oauth2")),
        (
            "personality config present",
            lambda: _check_file(BASE_DIR / "config" / "imp-personality.json"),
        ),
        (
            "intelligence registry present",
            lambda: _check_file(BASE_DIR / "config" / "imp-general-intelligences.json"),
        ),
        (
            "config manager loads",
            lambda: _check_import_file(BASE_DIR / "managers" / "config_manager.py"),
        ),
        (
            "goal manager loads",
            lambda: _check_import_file(BASE_DIR / "managers" / "goal_manager.py"),
        ),
        (
            "log manager loads",
            lambda: _check_import_file(BASE_DIR / "managers" / "log_manager.py"),
        ),
        (
            "heavy identity verifier loads",
            lambda: _check_import_file(BASE_DIR / "security" / "imp-heavy-identity-verifier.py"),
        ),
        (
            "google identity verifier loads",
            lambda: _check_import_file(BASE_DIR / "security" / "imp-google-identity-verifier.py"),
        ),
        (
            "terminal interface loads",
            lambda: _check_import_file(BASE_DIR / "interaction" / "imp-terminal.py"),
        ),
    ]

    results = []
    for desc, func in steps:
        status = "ok"
        detail = ""
        try:
            func()
        except Exception as exc:  # pylint: disable=broad-except
            status = "error"
            detail = str(exc)
        _append_log(
            {
                "step": desc,
                "status": status,
                "detail": detail,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )
        print(f"{desc}: {status}")
        results.append((desc, status, detail))
    return results


if __name__ == "__main__":
    run()
