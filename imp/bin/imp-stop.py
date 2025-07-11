import json
import os
import signal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PID_FILE = ROOT / 'logs' / 'imp-pids.json'

if PID_FILE.exists():
    with open(PID_FILE, 'r') as f:
        try:
            pids = json.load(f)
        except Exception:
            pids = []
    for pid in pids:
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError:
            pass
    PID_FILE.unlink()
    print('IMP AI has been stopped.')
else:
    print('No running IMP processes found.')

