from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "core" / "imp-3d-neural-network.py"

spec = importlib.util.spec_from_file_location("imp_3d_neural_network", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_optimal_path():
    print("Testing Optimal Path...")
    net = module.ThreeDNeuralNetwork()
    a = net.add_neuron((0, 0, 0))
    b = net.add_neuron((1, 0, 0))
    c = net.add_neuron((2, 0, 0))
    d = net.add_neuron((0, 1, 0))
    net.connect_for_task(a, b, task="default", myelin=1.0)
    net.connect_for_task(b, c, task="default", myelin=1.0)
    net.connect_for_task(a, d, task="default", myelin=1.0)
    net.connect_for_task(d, c, task="default", myelin=3.0)
    path = net.find_optimal_path(a, c)
    assert path == [a, d, c]
    print("Optimal Path Test Passed!")

if __name__ == "__main__":
    test_optimal_path()
