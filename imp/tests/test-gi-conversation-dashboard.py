import json
import importlib.util
import os
from pathlib import Path

try:
    import flask  # noqa: F401
except ModuleNotFoundError:  # pragma: no cover - dependency missing
    print("⚠️ Flask not available. Skipping GI Conversation Dashboard Test.")
    raise SystemExit(0)

BASE_DIR = Path(__file__).resolve().parents[1]
PROFILE_FILE = BASE_DIR / "config" / "imp-general-intelligences.json"
CONFIG_DIR = BASE_DIR / "config" / "gi"


def test_gi_conversation_dashboard():
    spec = importlib.util.spec_from_file_location(
        "dashboard", BASE_DIR / "interaction" / "imp-gi-conversation-dashboard.py"
    )
    dashboard = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dashboard)

    existing = []
    if PROFILE_FILE.exists():
        with open(PROFILE_FILE, "r") as f:
            try:
                existing = json.load(f)
            except json.JSONDecodeError:
                pass

    app = dashboard.create_app()
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    resp = client.post("/", data={"name": "DashGI"})
    assert resp.status_code == 200
    cfg = CONFIG_DIR / "DashGI.json"
    pkg = BASE_DIR / "DashGI_package.zip"
    assert cfg.exists()
    assert pkg.exists()
    cfg.unlink(missing_ok=True)
    pkg.unlink(missing_ok=True)
    # clean up in case filenames were normalized on disk
    alt_cfg = CONFIG_DIR / "dashgi.json"
    alt_pkg = BASE_DIR / "dashgi_package.zip"
    if alt_cfg.exists():
        alt_cfg.unlink()
    if alt_pkg.exists():
        alt_pkg.unlink()
    with open(PROFILE_FILE, "w") as f:
        json.dump(existing, f)
    print("✅ GI Conversation Dashboard Test Passed!")


test_gi_conversation_dashboard()
