from pathlib import Path
import json
import importlib.util
import subprocess

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / 'models' / 'network_task_nn.json'
DIFF_LOG = ROOT / 'logs' / 'imp-network-diff.json'
AUDITOR = ROOT / 'security' / 'imp-network-auditor.py'

spec = importlib.util.spec_from_file_location('network_task_nn', ROOT / 'core' / 'imp-network-task-nn.py')
network_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(network_module)
NetworkTaskNN = network_module.NetworkTaskNN


def load_model() -> NetworkTaskNN:
    if MODEL_PATH.exists():
        return NetworkTaskNN.load(MODEL_PATH)
    return NetworkTaskNN(1, 2, 1)


def latest_ip_count() -> int:
    if not DIFF_LOG.exists():
        return 0
    try:
        entries = json.loads(DIFF_LOG.read_text())
    except json.JSONDecodeError:
        return 0
    if not entries:
        return 0
    return len(entries[-1].get('new_ips', []))


def run_network_tasks() -> None:
    """Decide whether to run network auditing based on diff log data."""
    model = load_model()
    count = latest_ip_count()
    output = model.forward([count / 10.0])[0]
    print(f'[INFO] Network task model output: {output:.3f}')
    if output > 0.5:
        subprocess.run(['python3', str(AUDITOR)])
    else:
        print('[INFO] No network action required.')


if __name__ == '__main__':
    run_network_tasks()
