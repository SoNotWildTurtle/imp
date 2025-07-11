from pathlib import Path
import subprocess
import json

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'security' / 'imp-authenticator.py'
CONFIG = ROOT / 'config' / 'imp-credentials.json'

with open(CONFIG) as f:
    data = json.load(f)
user = data['users'][0]['username']

print('Testing Authentication...')
subprocess.run(f"python3 {SCRIPT} -u {user} -p demo", shell=True, check=False)
subprocess.run(f"python3 {SCRIPT} -g invalidtoken", shell=True, check=False)
subprocess.run(f"python3 {SCRIPT} --google-auto", shell=True, check=False)
print('Authentication Test Executed!')
