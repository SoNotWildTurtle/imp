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

MANAGER_PATH = ROOT / 'imp_neural_manager.py'
spec_mgr = importlib.util.spec_from_file_location('imp_neural_manager', MANAGER_PATH)
mgr_module = importlib.util.module_from_spec(spec_mgr)
spec_mgr.loader.exec_module(mgr_module)
neural_manager = mgr_module.manager

MODEL_PATH = ROOT.parents[0] / "logs" / "collaboratory_nn.json"


def load_model(input_len: int) -> CollaboratoryNN:
    def factory() -> CollaboratoryNN:
        if MODEL_PATH.exists():
            return CollaboratoryNN.load(MODEL_PATH)
        return CollaboratoryNN(input_len, 4, 1)
    return neural_manager.get_or_create('collaboratory', factory)


def run_collaboration(inputs: List[float]) -> float:
    """Run the collaboratory network on provided inputs."""
    net = load_model(len(inputs))
    out = net.forward(inputs)[0]
    net.save(MODEL_PATH)
    return out


if __name__ == "__main__":
    print(run_collaboration([0.0, 0.0]))
