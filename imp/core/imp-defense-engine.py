from pathlib import Path
import json
import importlib.util
import subprocess

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / 'models' / 'defense_nn.json'
AUDIT_LOG = ROOT / 'logs' / 'imp-network-audit.json'
DEFENSE_SCRIPT = ROOT / 'security' / 'imp-automated-defense.py'

spec = importlib.util.spec_from_file_location('defense_nn', ROOT / 'core' / 'imp-defense-nn.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
DefenseNN = module.DefenseNN


def load_model() -> DefenseNN:
    if MODEL_PATH.exists():
        return DefenseNN.load(MODEL_PATH)
    return DefenseNN(1, 2, 1)


def suspicious_count() -> int:
    if not AUDIT_LOG.exists():
        return 0
    try:
        data = json.loads(AUDIT_LOG.read_text())
    except json.JSONDecodeError:
        return 0
    return len(data)


def run_defense_cycle() -> None:
    model = load_model()
    count = suspicious_count()
    output = model.forward([count / 10.0])[0]
    print(f'[INFO] Defense model output: {output:.3f}')
    if output > 0.5:
        subprocess.run(['python3', str(DEFENSE_SCRIPT)])
    else:
        print('[INFO] No defense action required.')


if __name__ == '__main__':
    run_defense_cycle()
