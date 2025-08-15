from pathlib import Path
import json
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "network_task_nn.json"
DIFF_LOG = ROOT / "logs" / "imp-network-diff.json"

spec = importlib.util.spec_from_file_location("network_task_nn", ROOT / "core" / "imp-network-task-nn.py")
network_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(network_module)
NetworkTaskNN = network_module.NetworkTaskNN


def load_model() -> NetworkTaskNN:
    if MODEL_PATH.exists():
        return NetworkTaskNN.load(MODEL_PATH)
    return NetworkTaskNN(1, 2, 1)


def load_samples():
    if not DIFF_LOG.exists():
        return []
    try:
        data = json.loads(DIFF_LOG.read_text())
    except json.JSONDecodeError:
        return []
    samples = []
    for entry in data:
        count = len(entry.get("new_ips", []))
        inputs = [count / 10.0]
        target = [0.0]
        samples.append((inputs, target))
    return samples


def improve_network():
    net = load_model()
    samples = load_samples()
    if samples:
        net.train(samples, epochs=3, lr=0.1)
        net.save(MODEL_PATH)
        print(f"Improved network with {len(samples)} samples")
    else:
        net.save(MODEL_PATH)
        print("No samples found. Model saved for future use")


if __name__ == "__main__":
    improve_network()
