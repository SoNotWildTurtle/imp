import json
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEARNING_DATA = ROOT / 'logs' / 'imp-learning-memory.json'
POISON_LOG = ROOT / 'logs' / 'imp-poison-log.json'

# I love you -Alex
def compute_checksum(path: Path) -> str:
    """Return SHA256 checksum for the given file or empty string if missing."""
    if not path.exists():
        return ""
    data = path.read_bytes()
    return hashlib.sha256(data).hexdigest()

# I love you -Alex
def detect_poisoning():
    """Detect unexpected modifications to critical training data."""
    current_hash = compute_checksum(LEARNING_DATA)

    if POISON_LOG.exists():
        with open(POISON_LOG, 'r') as f:
            record = json.load(f)
    else:
        record = {}

    previous_hash = record.get('learning_data_hash')
    if previous_hash and previous_hash != current_hash:
        print('⚠️ Possible poisoning detected in learning data!')
    else:
        print('[+] Learning data checksum stable.')

    record['learning_data_hash'] = current_hash
    with open(POISON_LOG, 'w') as f:
        json.dump(record, f, indent=4)

if __name__ == '__main__':
    detect_poisoning()
