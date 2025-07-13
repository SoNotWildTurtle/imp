from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "self-improvement" / "imp-blockchain-ledger.py"
spec = importlib.util.spec_from_file_location("ledger", MODULE_PATH)
ledger = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ledger)
LEDGER_FILE = ROOT / "logs" / "imp-blockchain-ledger.json"


def test_blockchain_ledger():
    print("Running Blockchain Ledger...")
    ledger.add_block()
    assert LEDGER_FILE.exists()
    assert ledger.verify_chain(), "Blockchain verification failed"
    print("Blockchain Ledger Test Passed!")


test_blockchain_ledger()
