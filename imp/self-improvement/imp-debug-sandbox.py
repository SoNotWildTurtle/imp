"""Run self-evolution experiments in a debug sandbox."""

import json
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NN_PATH = ROOT / "core" / "imp-3d-neural-network.py"
LOG_PATH = ROOT / "logs" / "imp-sandbox-log.json"

spec = importlib.util.spec_from_file_location("imp_3d_network", NN_PATH)
net_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(net_module)


def run_sandbox() -> None:
    """Evolve a copy of the 3D network and record the summary."""
    net = net_module.ThreeDNeuralNetwork()
    a = net.add_neuron((0, 0, 0))
    b = net.add_neuron((1, 0, 0))
    net.connect(a, b)
    evolved, summary = net.simulate_evolution()
    LOG_PATH.write_text(json.dumps(summary))
    print(json.dumps(summary))


if __name__ == "__main__":
    run_sandbox()
