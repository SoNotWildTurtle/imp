from pathlib import Path
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / 'self-improvement' / 'imp-self-healer.py'
HEAL_LOG = ROOT / 'logs' / 'imp-self-heal-log.json'
PATCH_DIR = ROOT / 'logs' / 'imp-update-patches'
LINT_LOG = ROOT / 'logs' / 'imp-lint-report.json'
LEDGER_PATH = ROOT / 'self-improvement' / 'imp-blockchain-ledger.py'
spec_ledger = importlib.util.spec_from_file_location('ledger', LEDGER_PATH)
ledger = importlib.util.module_from_spec(spec_ledger)
spec_ledger.loader.exec_module(ledger)

spec = importlib.util.spec_from_file_location('self_healer', MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

print('Running Self Healer...')
before = len(ledger.load_ledger())
module.verify_and_heal(mint=True)
after = len(ledger.load_ledger())
assert after == before + 1, 'Ledger block was not minted'
assert HEAL_LOG.exists()
assert PATCH_DIR.exists()
assert LINT_LOG.exists()
with open(HEAL_LOG, 'r') as f:
    json.load(f)
with open(LINT_LOG, 'r') as f:
    json.load(f)

# Ensure ChatGPT recovery helper exists and can create a file
assert hasattr(module, 'recover_with_chatgpt')
dummy_rel = 'temp/test_module.py'
dummy_path = ROOT / dummy_rel
if dummy_path.exists():
    dummy_path.unlink()
module.recover_with_chatgpt(dummy_rel, mode='offline')
assert dummy_path.exists()
dummy_path.unlink()
print('Self Healer Test Passed!')
