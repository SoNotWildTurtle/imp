from pathlib import Path
import subprocess
import json
import importlib.util
import time

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'security' / 'imp-authenticator.py'
CONFIG = ROOT / 'config' / 'imp-credentials.json'

with open(CONFIG) as f:
    data = json.load(f)
user = data['users'][0]['username']

print('Testing Authentication...')
subprocess.run(f"python3 {SCRIPT} -u {user} -p demo", shell=True, check=False)
subprocess.run(f"python3 {SCRIPT} -g invalidtoken", shell=True, check=False)
subprocess.run(f"python3 {SCRIPT} --google-auto --google-email test@example.com", shell=True, check=False)
spec = importlib.util.spec_from_file_location('imp_auth', SCRIPT)
imp_auth = importlib.util.module_from_spec(spec)
spec.loader.exec_module(imp_auth)
assert imp_auth.idle_relog(time.time())
assert not imp_auth.idle_relog(time.time() - 301)
print('Authentication Test Executed!')
