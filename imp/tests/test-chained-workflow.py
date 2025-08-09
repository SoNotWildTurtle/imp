from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

ledger = load_module('ledger', ROOT / 'self-improvement' / 'imp-blockchain-ledger.py')
bug = load_module('bug', ROOT / 'self-improvement' / 'imp-bug-hunter.py')
auto_heal_mod = load_module('auto_heal', ROOT / 'self-improvement' / 'imp-auto-heal.py')


def test_chained_workflow():
    print('Running Chained Workflow Test...')
    ledger.add_block()
    bug.scan_repository()
    auto_heal_mod.healer.auto_verify_and_heal()
    assert ledger.verify_chain(), 'Ledger verification failed'
    print('Chained Workflow Test Passed!')


test_chained_workflow()
