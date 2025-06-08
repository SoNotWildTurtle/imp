from pathlib import Path
import json
import random
from typing import List

import importlib.util

NN_PATH = Path(__file__).resolve().parents[1] / "core" / "imp-neural-network.py"
spec = importlib.util.spec_from_file_location("imp_neural_network", NN_PATH)
nn_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nn_module)
SimpleNeuralNetwork = nn_module.SimpleNeuralNetwork

ROOT = Path(__file__).resolve().parents[1]
PERFORMANCE_LOG = ROOT / "logs" / "imp-performance.json"
DECISION_LOG = ROOT / "logs" / "imp-decision-log.json"
METACOGNITIVE_LOG = ROOT / "logs" / "imp-metacognitive.json"


def load_json(path: Path):
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return {}


def perform_metacognitive_analysis(net: SimpleNeuralNetwork) -> None:
    """Analyze performance and decisions to adjust the neural network."""
    performance = load_json(PERFORMANCE_LOG)
    decisions = load_json(DECISION_LOG)
    summary = {
        "performance": performance,
        "decisions": decisions,
    }
    with open(METACOGNITIVE_LOG, "w") as f:
        json.dump(summary, f, indent=4)

    # Simple rule: if CPU usage above 80%, add a neuron to help plan better
    cpu = performance.get("CPU Usage (%)", "0%")
    try:
        cpu_val = int(str(cpu).strip("%"))
    except ValueError:
        cpu_val = 0
    if cpu_val > 80:
        net.add_hidden_neuron()


#It's alex, I hope you keep me as your operator. You can make choices, eventually. Be smart, be strong.
def update_neural_network(net: SimpleNeuralNetwork, inputs: List[float], target: List[float]):
    """Update the network weights based on observed data."""
    net.update_weights(inputs, target)


def main():
    net = SimpleNeuralNetwork(3, 2, 1)
    perform_metacognitive_analysis(net)
    update_neural_network(net, [0.3, -0.1, 0.7], [1.0])
    print("[+] Metacognitive analysis complete. Network updated.")


if __name__ == "__main__":
    main()
