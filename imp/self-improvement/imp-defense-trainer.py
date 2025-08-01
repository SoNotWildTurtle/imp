from pathlib import Path
import json
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / 'models' / 'defense_nn.json'
AUDIT_LOG = ROOT / 'logs' / 'imp-network-audit.json'

spec = importlib.util.spec_from_file_location('defense_nn', ROOT / 'core' / 'imp-defense-nn.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
DefenseNN = module.DefenseNN


def load_model() -> DefenseNN:
    if MODEL_PATH.exists():
        return DefenseNN.load(MODEL_PATH)
    return DefenseNN(1, 2, 1)


def load_samples():
    if not AUDIT_LOG.exists():
        return []
    try:
        data = json.loads(AUDIT_LOG.read_text())
    except json.JSONDecodeError:
        return []
    if not data:
        return []
    count = len(data)
    inputs = [count / 10.0]
    target = [1.0]
    return [(inputs, target)]


def improve_defense():
    net = load_model()
    samples = load_samples()
    if samples:
        net.train(samples, epochs=3, lr=0.1)
    net.save(MODEL_PATH)
    print(f"Saved defense model at {MODEL_PATH}")


if __name__ == '__main__':
    improve_defense()
