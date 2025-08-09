import json
import importlib.util
os = __import__('os')

try:
    import flask  # noqa: F401
except ModuleNotFoundError:  # pragma: no cover - dependency missing
    print("⚠️ Flask not available. Skipping GI Web Dashboard Test.")
    raise SystemExit(0)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQUEST_FILE = os.path.join(BASE_DIR, 'logs', 'imp-gi-requests.json')
DECISION_FILE = os.path.join(BASE_DIR, 'logs', 'imp-gi-upgrade-decisions.json')

def test_gi_web_dashboard():
    spec = importlib.util.spec_from_file_location('dashboard', os.path.join(BASE_DIR, 'interaction', 'imp-gi-web-dashboard.py'))
    dashboard = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dashboard)
    with open(REQUEST_FILE, 'w') as f:
        json.dump([{ 'name': 'TestGI', 'request': 'new feature'}], f)
    with open(DECISION_FILE, 'w') as f:
        json.dump([], f)
    app = dashboard.create_app()
    client = app.test_client()
    resp = client.get('/requests')
    assert resp.status_code == 200
    assert 'new feature' in resp.get_data(as_text=True)
    resp = client.post('/requests', data={'index':'0','decision':'approve'}, follow_redirects=True)
    assert resp.status_code == 200
    with open(REQUEST_FILE, 'r') as f:
        assert json.load(f) == []
    with open(DECISION_FILE, 'r') as f:
        decisions = json.load(f)
        assert any(d.get('decision') == 'approve' for d in decisions)
    print('✅ GI Web Dashboard Test Passed!')

test_gi_web_dashboard()
