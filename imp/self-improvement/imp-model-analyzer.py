from pathlib import Path
import importlib.util
import json
import time
import math
from typing import List

# Dynamically load the minimal neural network implementation
ROOT = Path(__file__).resolve().parents[1]
NN_PATH = ROOT / "core" / "imp-neural-network.py"
spec = importlib.util.spec_from_file_location("imp_neural_network", NN_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
SimpleNeuralNetwork = module.SimpleNeuralNetwork

NN3D_PATH = ROOT / "core" / "imp-3d-neural-network.py"
spec3d = importlib.util.spec_from_file_location("imp_3d_network", NN3D_PATH)
module3d = importlib.util.module_from_spec(spec3d)
spec3d.loader.exec_module(module3d)
ThreeDNeuralNetwork = module3d.ThreeDNeuralNetwork

ANALYSIS_LOG = ROOT / "logs" / "imp-model-analysis.json"


def _mean_abs_diff(mat_a: List[List[float]], mat_b: List[List[float]]) -> float:
    total = 0.0
    count = 0
    for i in range(min(len(mat_a), len(mat_b))):
        row_a = mat_a[i]
        row_b = mat_b[i]
        for j in range(min(len(row_a), len(row_b))):
            total += abs(row_a[j] - row_b[j])
            count += 1
    return total / count if count else 0.0


def compare_models(model_a: SimpleNeuralNetwork, model_b: SimpleNeuralNetwork) -> dict:
    """Return basic spatial diff statistics between two networks."""
    diff = {
        "input_size_diff": model_b.input_size - model_a.input_size,
        "hidden_size_diff": model_b.hidden_size - model_a.hidden_size,
        "output_size_diff": model_b.output_size - model_a.output_size,
        "w1_diff": _mean_abs_diff(model_a.w1, model_b.w1),
        "w2_diff": _mean_abs_diff(model_a.w2, model_b.w2),
    }
    return diff


def compare_model_files(path_a: Path, path_b: Path) -> dict:
    """Load two model snapshots and record their differences."""
    model_a = SimpleNeuralNetwork.load(path_a)
    model_b = SimpleNeuralNetwork.load(path_b)
    diff = compare_models(model_a, model_b)
    entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "model_a": str(path_a),
        "model_b": str(path_b),
        "diff": diff,
    }
    if ANALYSIS_LOG.exists():
        with open(ANALYSIS_LOG, "r") as f:
            data = json.load(f)
    else:
        data = []
    data.append(entry)
    with open(ANALYSIS_LOG, "w") as f:
        json.dump(data, f, indent=4)
    return diff


# I love you -Alex
def _mean_positional_diff(neurons_a, neurons_b) -> float:
    total = 0.0
    count = 0
    for a, b in zip(neurons_a, neurons_b):
        dist = math.sqrt(
            (a.position[0] - b.position[0]) ** 2 +
            (a.position[1] - b.position[1]) ** 2 +
            (a.position[2] - b.position[2]) ** 2
        )
        total += dist
        count += 1
    return total / count if count else 0.0


# I love you -Alex
def compare_3d_networks(net_a: ThreeDNeuralNetwork, net_b: ThreeDNeuralNetwork) -> dict:
    diff = {
        "neuron_count_diff": len(net_b.neurons) - len(net_a.neurons),
        "connection_count_diff": len(net_b.connections) - len(net_a.connections),
        "avg_position_diff": _mean_positional_diff(net_a.neurons, net_b.neurons),
        "new_types": list({n.neuron_type for n in net_b.neurons} - {n.neuron_type for n in net_a.neurons}),
    }
    return diff


# I love you -Alex
def compare_3d_network_files(path_a: Path, path_b: Path) -> dict:
    net_a = ThreeDNeuralNetwork.load(path_a)
    net_b = ThreeDNeuralNetwork.load(path_b)
    diff = compare_3d_networks(net_a, net_b)
    entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "model_a": str(path_a),
        "model_b": str(path_b),
        "diff": diff,
    }
    if ANALYSIS_LOG.exists():
        with open(ANALYSIS_LOG, "r") as f:
            data = json.load(f)
    else:
        data = []
    data.append(entry)
    with open(ANALYSIS_LOG, "w") as f:
        json.dump(data, f, indent=4)
    return diff


def temporal_analysis(paths: List[Path]) -> List[dict]:
    """Analyze sequential model snapshots for changes over time."""
    results = []
    for i in range(1, len(paths)):
        diff = compare_model_files(paths[i-1], paths[i])
        results.append(diff)
    return results


if __name__ == "__main__":
    # Example usage
    m1 = SimpleNeuralNetwork(2, 2, 1)
    m2 = SimpleNeuralNetwork(2, 3, 1)
    tmp1 = ROOT / "model_a.json"
    tmp2 = ROOT / "model_b.json"
    m1.save(tmp1)
    m2.save(tmp2)
    print(compare_model_files(tmp1, tmp2))
    tmp1.unlink()
    tmp2.unlink()
