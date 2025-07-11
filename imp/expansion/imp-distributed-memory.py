from pathlib import Path
import json
import time

ROOT = Path(__file__).resolve().parents[1]
MEM_FILE = ROOT / 'logs' / 'imp-distributed-memory.json'


def _load_memory() -> dict:
    if MEM_FILE.exists():
        try:
            with open(MEM_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}


def _save_memory(mem: dict) -> None:
    with open(MEM_FILE, 'w') as f:
        json.dump(mem, f, indent=4)


def store_fact(key: str, value: str) -> None:
    """Store a fact in the distributed memory."""
    mem = _load_memory()
    mem[key] = {'value': value, 'timestamp': time.time()}
    _save_memory(mem)


def retrieve_fact(key: str):
    """Retrieve a fact from distributed memory."""
    mem = _load_memory()
    return mem.get(key)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='IMP Distributed Memory')
    parser.add_argument('--set', nargs=2, metavar=('KEY', 'VALUE'))
    parser.add_argument('--get', metavar='KEY')
    args = parser.parse_args()

    if args.set:
        store_fact(args.set[0], args.set[1])
        print('Fact stored')
    elif args.get:
        print(retrieve_fact(args.get))
