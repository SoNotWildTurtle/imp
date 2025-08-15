from __future__ import annotations

"""Web dashboard for cooperative GI creation and download."""

from pathlib import Path
import json
import importlib.util
import os
import sys

try:
    from flask import Flask, request, send_file, redirect, render_template_string
except ModuleNotFoundError:  # pragma: no cover - dependency missing
    Flask = None  # type: ignore

BASE_DIR = Path(__file__).resolve().parents[1]
PROFILE_FILE = BASE_DIR / "config" / "imp-general-intelligences.json"
CONFIG_DIR = BASE_DIR / "config" / "gi"

spec = importlib.util.spec_from_file_location(
    "packager", BASE_DIR / "interaction" / "imp-gi-packager.py"
)
packager = importlib.util.module_from_spec(spec)
spec.loader.exec_module(packager)  # type: ignore

BUILT_IN = [
    "imp-gi-memory.py",
    "imp-gi-task-manager.py",
    "imp-gi-self-evolver.py",
    "imp-gi-knowledge.py",
    "imp-gi-skill-tracker.py",
    "imp-gi-performance.py",
    "imp-gi-safety.py",
    "imp-gi-risk-analyzer.py",
    "imp-gi-planner.py",
    "imp-gi-comm-log.py",
    "imp-gi-implementation-log.py",
    "imp-gi-request.py",
    "imp-gi-feedback.py",
    "imp-gi-personality.py",
]


def create_app():
    if Flask is None:  # pragma: no cover - flask missing
        raise SystemExit("Flask not installed")
    app = Flask(__name__)

    @app.route("/", methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            if not name:
                return redirect("/")
            profile = {"name": name, "modules": BUILT_IN}
            profiles = []
            if PROFILE_FILE.exists():
                try:
                    profiles = json.loads(PROFILE_FILE.read_text())
                except json.JSONDecodeError:
                    pass
            profiles.append(profile)
            PROFILE_FILE.write_text(json.dumps(profiles, indent=4))
            CONFIG_DIR.mkdir(exist_ok=True)
            cfg_path = CONFIG_DIR / f"{name}.json"
            cfg_path.write_text(json.dumps(profile, indent=4))
            archive = packager.package_gi(cfg_path)
            return send_file(archive, as_attachment=True)
        return render_template_string(
            """
            <h1>Create Your General Intelligence</h1>
            <form method="post">
                <input name="name" placeholder="Name" />
                <button type="submit">Create</button>
            </form>
            """
        )

    return app


def main() -> None:
    port_str = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("GI_DASHBOARD_PORT", "5000")
    try:
        port = int(port_str)
    except ValueError:
        port = 5000
    print(f"[i] Conversation dashboard running on port {port}")
    create_app().run(port=port)


if __name__ == "__main__":
    main()
