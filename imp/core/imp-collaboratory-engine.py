"""Engine that uses CollaboratoryNN for collaborative network decisions."""

from pathlib import Path
from typing import List
import importlib.util

ROOT = Path(__file__).resolve().parent
NN_PATH = ROOT / "imp-collaboratory-nn.py"
spec = importlib.util.spec_from_file_location("collab_nn", NN_PATH)
collab_nn = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collab_nn)
CollaboratoryNN = collab_nn.CollaboratoryNN

MODEL_PATH = ROOT.parents[0] / "logs" / "collaboratory_nn.json"


def run_collaboration(inputs: List[float]) -> float:
    """Run the collaboratory network on provided inputs."""
    if MODEL_PATH.exists():
        net = CollaboratoryNN.load(MODEL_PATH)
    else:
        net = CollaboratoryNN(len(inputs), 4, 1)
    out = net.forward(inputs)[0]
    net.save(MODEL_PATH)
    return out


if __name__ == "__main__":
    print(run_collaboration([0.0, 0.0]))
