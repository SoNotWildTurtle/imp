from flask import Flask, request, redirect, url_for, render_template_string
from pathlib import Path
import json
import time

BASE_DIR = Path(__file__).resolve().parents[1]
PROFILE_FILE = BASE_DIR / "config" / "imp-general-intelligences.json"
REQUEST_FILE = BASE_DIR / "logs" / "imp-gi-requests.json"
DECISIONS_FILE = BASE_DIR / "logs" / "imp-gi-upgrade-decisions.json"
PERFORMANCE_FILE = BASE_DIR / "logs" / "imp-gi-performance.json"


def load_json(path):
    if path.exists():
        with open(path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        profiles = load_json(PROFILE_FILE)
        requests = load_json(REQUEST_FILE)
        perf = load_json(PERFORMANCE_FILE)
        req_counts = {}
        for r in requests:
            req_counts[r.get("name")] = req_counts.get(r.get("name"), 0) + 1
        perf_counts = {}
        for p in perf:
            perf_counts[p.get("name")] = perf_counts.get(p.get("name"), 0) + 1
        html = """
        <h1>GI Dashboard</h1>
        <ul>
        {% for p in profiles %}
          <li>{{p['name']}} - Requests: {{req_counts.get(p['name'],0)}} - Perf entries: {{perf_counts.get(p['name'],0)}}
          </li>
        {% endfor %}
        </ul>
        <p><a href="{{url_for('request_view')}}">View Requests</a></p>
        """
        return render_template_string(html, profiles=profiles, req_counts=req_counts, perf_counts=perf_counts)

    @app.route("/requests", methods=["GET", "POST"])
    def request_view():
        requests_list = load_json(REQUEST_FILE)
        if request.method == "POST":
            idx = int(request.form.get("index", -1))
            decision = request.form.get("decision")
            if 0 <= idx < len(requests_list) and decision in {"approve", "deny"}:
                entry = requests_list.pop(idx)
                decisions = load_json(DECISIONS_FILE)
                decisions.append({
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "name": entry.get("name"),
                    "request": entry.get("request"),
                    "decision": decision,
                })
                save_json(DECISIONS_FILE, decisions)
                save_json(REQUEST_FILE, requests_list)
            return redirect(url_for("request_view"))
        html = """
        <h1>Pending Requests</h1>
        <ul>
        {% for r in requests %}
          <li>{{loop.index0}}: {{r['name']}} - {{r['request']}}
            <form method='post' style='display:inline'>
              <input type='hidden' name='index' value='{{loop.index0}}'>
              <button name='decision' value='approve'>Approve</button>
              <button name='decision' value='deny'>Deny</button>
            </form>
          </li>
        {% endfor %}
        </ul>
        <p><a href="{{url_for('index')}}">Back</a></p>
        """
        return render_template_string(html, requests=requests_list)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
