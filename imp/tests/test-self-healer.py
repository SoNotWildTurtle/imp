from pathlib import Path
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / 'self-improvement' / 'imp-self-healer.py'
HEAL_LOG = ROOT / 'logs' / 'imp-self-heal-log.json'

spec = importlib.util.spec_from_file_location('self_healer', MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

print('Running Self Healer...')
module.verify_and_heal()
assert HEAL_LOG.exists()
with open(HEAL_LOG, 'r') as f:
    json.load(f)
print('Self Healer Test Passed!')
