import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXEC_SCRIPT = ROOT / 'core' / 'imp-execute.py'
MODULES = [
    ROOT / 'core' / 'imp-learning-memory.py',
    ROOT / 'core' / 'imp-strategy-generator.py',
    ROOT / 'self-improvement' / 'imp-code-updater.py',
    ROOT / 'security' / 'imp-security-optimizer.py',
    ROOT / 'expansion' / 'imp-cluster-manager.py'
]

PID_FILE = ROOT / 'logs' / 'imp-pids.json'

pids = []
# start core executor
proc = subprocess.Popen([sys.executable, str(EXEC_SCRIPT)])
pids.append(proc.pid)

for module in MODULES:
    p = subprocess.Popen([sys.executable, str(module)])
    pids.append(p.pid)

import json
PID_FILE.write_text(json.dumps(pids))
print('IMP AI is now running.')

