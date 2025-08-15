"""Simple CLI to manage neural networks via the global manager."""

import argparse
from pathlib import Path
import importlib.util

CORE_DIR = Path(__file__).resolve().parent

def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

nm = _load("imp_neural_manager", CORE_DIR / "imp_neural_manager.py")
manager = nm.manager
SimpleNeuralNetwork = _load("imp_neural_network", CORE_DIR / "imp-neural-network.py").SimpleNeuralNetwork


def main() -> None:
    parser = argparse.ArgumentParser(description="NN manager interface")
    parser.add_argument("--list", action="store_true", help="List registered networks")
    parser.add_argument("--register-basic", action="store_true", help="Register a basic placeholder network")
    args = parser.parse_args()

    if args.register_basic:
        if "basic" not in manager.list():
            manager.register("basic", SimpleNeuralNetwork(2, 2, 1))

    if args.list:
        names = manager.list()
        if names:
            print("Registered networks: " + ", ".join(names))
        else:
            print("Registered networks: none")

if __name__ == "__main__":
    main()
