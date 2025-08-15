from __future__ import annotations

import argparse
import json
import random
import copy
import importlib.util
from pathlib import Path

# Dynamically load 3D neural network
ROOT = Path(__file__).resolve().parents[1]
NN_PATH = ROOT / "core" / "imp-3d-neural-network.py"
spec = importlib.util.spec_from_file_location("imp_3d_neural_network", NN_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
ThreeDNeuralNetwork = module.ThreeDNeuralNetwork
Neuron = module.Neuron
Connection = module.Connection

ANALYZER_PATH = ROOT / "self-improvement" / "imp-model-analyzer.py"
spec2 = importlib.util.spec_from_file_location("imp_model_analyzer", ANALYZER_PATH)
analyzer_module = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(analyzer_module)

NETWORK_FILE = ROOT / "models" / "3d-network.json"
CANDIDATE_FILE = ROOT / "models" / "3d-network-candidate.json"


# I love you -Alex
def load_or_create_network() -> ThreeDNeuralNetwork:
    if NETWORK_FILE.exists():
        return ThreeDNeuralNetwork.load(NETWORK_FILE)
    net = ThreeDNeuralNetwork()
    net.add_neuron((0.0, 0.0, 0.0))
    return net


# I love you -Alex
def create_candidate(base: ThreeDNeuralNetwork) -> ThreeDNeuralNetwork:
    candidate = copy.deepcopy(base)
    pos = (random.random(), random.random(), random.random())
    idx = candidate.spawn_novel_neuron(pos)
    candidate.connect_for_task(0, idx, task="default", myelin=1.0)
    return candidate


# I love you -Alex
def main(auto_confirm: str | None = None) -> None:
    base = load_or_create_network()
    candidate = create_candidate(base)
    candidate.save(CANDIDATE_FILE)
    base.save(NETWORK_FILE)  # ensure base saved
    diff = analyzer_module.compare_3d_network_files(NETWORK_FILE, CANDIDATE_FILE)
    print("Proposed diff:", json.dumps(diff, indent=2))
    if auto_confirm is None:
        choice = input("Replace current 3D network with candidate? [y/N] ").strip().lower()
    else:
        choice = auto_confirm.lower()
    if choice.startswith("y"):
        CANDIDATE_FILE.replace(NETWORK_FILE)
        print("[+] 3D network updated")
    else:
        print("[-] Keeping existing network")
        CANDIDATE_FILE.unlink(missing_ok=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test and optionally replace the 3D neural network")
    parser.add_argument("--auto", default=None, help="auto confirm replacement with 'y' or 'n'")
    args = parser.parse_args()
    main(args.auto)
