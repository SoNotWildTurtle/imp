from pathlib import Path
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / 'expansion' / 'imp-distributed-memory.py'
LOG = ROOT / 'logs' / 'imp-distributed-memory.json'

spec = importlib.util.spec_from_file_location('dm', MODULE)
dm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dm)

print('Testing Distributed Memory...')
LOG.write_text('{}')

dm.store_fact('key1', 'value1')
assert json.loads(LOG.read_text())['key1']['value'] == 'value1'

fact = dm.retrieve_fact('key1')
assert fact['value'] == 'value1'

print('Distributed Memory Test Passed!')
