from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "core" / "imp-network-task-nn.py"

spec = importlib.util.spec_from_file_location("network_task_nn", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_network_task_nn():
    print("Testing Network Task Neural Network...")
    net = module.NetworkTaskNN(2, 2, 1)
    out = net.forward([0.5, 0.5])
    assert len(out) == 1
    tmp = ROOT / "net_task_tmp.json"
    net.save(tmp)
    loaded = module.NetworkTaskNN.load(tmp)
    assert loaded.forward([0.5, 0.5])[0] == out[0]
    tmp.unlink()
    print("Network Task NN Test Passed!")

if __name__ == "__main__":
    test_network_task_nn()
