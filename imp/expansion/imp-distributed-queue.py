from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE_FILE = ROOT / 'logs' / 'imp-distributed-queue.json'


def _load_queue() -> list[dict]:
    if QUEUE_FILE.exists():
        try:
            with open(QUEUE_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []


def _save_queue(queue: list[dict]) -> None:
    with open(QUEUE_FILE, 'w') as f:
        json.dump(queue, f, indent=4)


def add_task(command: str) -> None:
    """Add a new task to the distributed queue."""
    queue = _load_queue()
    queue.append({'command': command, 'node': None, 'status': 'pending'})
    _save_queue(queue)


def assign_tasks(nodes: list[str]) -> dict[str, list[str]]:
    """Assign pending tasks round-robin across nodes."""
    queue = _load_queue()
    pending = [t for t in queue if t['status'] == 'pending']
    if not pending or not nodes:
        return {}
    assignments: dict[str, list[str]] = {}
    for i, task in enumerate(pending):
        node = nodes[i % len(nodes)]
        task['node'] = node
        task['status'] = 'assigned'
        assignments.setdefault(node, []).append(task['command'])
    _save_queue(queue)
    return assignments


def get_assigned(node: str) -> list[str]:
    """Retrieve tasks assigned to a specific node."""
    queue = _load_queue()
    tasks = [t['command'] for t in queue if t['node'] == node and t['status'] == 'assigned']
    return tasks


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='IMP Distributed Queue')
    parser.add_argument('--add', help='Add a task command')
    parser.add_argument('--assign', action='store_true', help='Assign tasks to nodes from config')
    parser.add_argument('--node', help='Get tasks assigned to a node')
    args = parser.parse_args()

    if args.add:
        add_task(args.add)
        print('Task added')
    elif args.assign:
        config_path = ROOT / 'config' / 'imp-cluster-nodes.json'
        nodes = []
        if config_path.exists():
            with open(config_path, 'r') as f:
                nodes = json.load(f)
        assignments = assign_tasks(nodes)
        print(json.dumps(assignments, indent=4))
    elif args.node:
        print(get_assigned(args.node))
