import json
import hashlib
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER_FILE = ROOT / "logs" / "imp-blockchain-ledger.json"
CODE_DIR = ROOT


def snapshot_code() -> dict:
    files = [p for p in CODE_DIR.glob("**/*.py") if "__pycache__" not in str(p)]
    result = {}
    for path in files:
        try:
            content = path.read_bytes()
            result[str(path.relative_to(ROOT))] = hashlib.sha256(content).hexdigest()
        except Exception:
            pass
    return result


def load_ledger() -> list:
    if LEDGER_FILE.exists():
        with open(LEDGER_FILE, "r") as f:
            return json.load(f)
    return []


def save_ledger(entries: list) -> None:
    with open(LEDGER_FILE, "w") as f:
        json.dump(entries, f, indent=4)


def add_block() -> dict:
    ledger = load_ledger()
    prev_hash = ledger[-1]["block_hash"] if ledger else ""
    files = snapshot_code()
    block_data = json.dumps({"prev_hash": prev_hash, "files": files}, sort_keys=True)
    block_hash = hashlib.sha256(block_data.encode()).hexdigest()
    entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "prev_hash": prev_hash,
        "block_hash": block_hash,
        "files": files,
    }
    ledger.append(entry)
    save_ledger(ledger)
    return entry


def verify_chain() -> bool:
    ledger = load_ledger()
    prev_hash = ""
    for entry in ledger:
        data = json.dumps({"prev_hash": prev_hash, "files": entry["files"]}, sort_keys=True)
        if hashlib.sha256(data.encode()).hexdigest() != entry["block_hash"]:
            return False
        prev_hash = entry["block_hash"]
    return True


if __name__ == "__main__":
    add_block()
    print("Ledger valid:", verify_chain())
