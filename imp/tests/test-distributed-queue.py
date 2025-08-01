from pathlib import Path
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / 'expansion' / 'imp-distributed-queue.py'
LOG = ROOT / 'logs' / 'imp-distributed-queue.json'

spec = importlib.util.spec_from_file_location('dq', MODULE)
dq = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dq)

print('Testing Distributed Queue...')
LOG.write_text('[]')

# add task
dq.add_task('echo hello')
assert json.loads(LOG.read_text())[0]['command'] == 'echo hello'

# assign to node
assign = dq.assign_tasks(['localhost'])
assert 'localhost' in assign

print('Distributed Queue Test Passed!')
